<?php

/**
 * 此类用来动态代理各种对象，为了方便做缓存和性能调试
 * 要求代理的对象都是无状态的
 *
 */
class Apf_Proxy_Proxy
{

    private $proxyedObj;

    protected static $allowMethodes = array();

    /**
     * 单位秒，如果发现有方法执行时间超过还一定的阀值，会发送报警信息
     */
    const DEFAULT_WARN_TIMEOUT = 0.1;

    private static $inited = false;

    private static $logger;

    /**
     *
     * @var array
     */
    private static $memcacheClients;

    /**
     * @return the $proxyedObj
     */
    public function getProxyedObj()
    {
        return $this->proxyedObj;
    }

    /**
     * @param mixed $proxyedObj
     */
    public function setProxyedObj($proxyedObj)
    {
        $this->proxyedObj = $proxyedObj;
    }

    public function __construct($proxyedObj)
    {
        $this->proxyedObj = $proxyedObj;
        
        self::init();
    }

    protected static function init()
    {
        if(self::$inited) {
            return;
        }
        self::$logger = Apf_Logger_LoggerFactory::getLogger(__CLASS__);
        self::$allowMethodes = APF::get_instance()->get_config('allow_methodes', 'servicecache');
        
        self::$inited = true;
    }

    public function __call($funcName, $args)
    {
        $callback = array(
                $this->proxyedObj, 
                $funcName 
        );
        
        $showName = null;
        
        if(! is_callable($callback, false, $showName)) {
            Apf_Logger_LoggerFactory::getLogger(__CLASS__)->errorAndThrowException("class " . get_class($this->proxyedObj) . " $funcName is not callable");
        }
        
        $t1 = microtime(true);
        $cacheConfig = self::$allowMethodes[$showName];
        if(! empty($cacheConfig)) {
            //use cache
            $rt = $this->getMemcacheClient()->getNullAndSet($callback, $args, $cacheConfig['cachetime']);
        } else {
            $rt = call_user_func_array($callback, $args);
        }
        $usedTime = microtime(true) - $t1;
        if($usedTime > self::DEFAULT_WARN_TIMEOUT) {
            if(self::$logger->isWarnEnabled()) {
                self::$logger->warns("$showName execute time over " . self::DEFAULT_WARN_TIMEOUT . " s is $usedTime");
            }
        }
        if(APF::get_instance()->get_debugger()) {
            APF::get_instance()->debug("@@@@@ proxy $showName execute time $usedTime");
        }
        
        return $rt;
    }

    /**
     *
     * @return Apf_Cache_MemcacheClient:
     */
    private function getMemcacheClient()
    {
        $group = Apf_Const_Cache::MEMCACHE_GROUP_SERVICE;
        if(is_callable(array(
                $this->proxyedObj, 
                'getCacheGroup' 
        ))) {
            $group = $this->proxyedObj->getCacheGroup();
        }
        
        if(empty(self::$memcacheClients[$group])) {
            self::$memcacheClients[$group] = Apf_Cache_MemcacheClient::getInstance(Apf_Const_Cache::MEMCACHE_GROUP_SERVICE);
        }
        return self::$memcacheClients[$group];
    }
}