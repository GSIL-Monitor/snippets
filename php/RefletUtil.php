<?php
class Apf_Util_RefletUtil
{

    /**
     * 
     * @param string $className
     * @param array $constructArgs
     * @return object
     */
    public static function createObject($className, $constructArgs = array())
    {
        if(empty($constructArgs)) {
            return new $className();
        } elseif(count($constructArgs) == 1) {
            return new $className($constructArgs[0]);
        } elseif(count($constructArgs) == 2) {
            return new $className($constructArgs[0], $constructArgs[1]);
        } elseif(count($constructArgs) == 3) {
            return new $className($constructArgs[0], $constructArgs[1], $constructArgs[2]);
        } elseif(count($constructArgs) == 4) {
            return new $className($constructArgs[0], $constructArgs[1], $constructArgs[2], $constructArgs[3]);
        } else {
            $reflectionClass = new ReflectionClass($className);
            return $reflectionClass->newInstanceArgs($constructArgs);
        }
    }

    /**
     * 通过反射调用非公共方法
     * @param mixed $object
     *     对象或者类名，类名用于静态调用
     * @param string $method
     * @param array $args
     */
    public static function invokeNoPublicMethod($object, $method, $args)
    {
        $method = new ReflectionMethod($object, $method);
        $method->setAccessible(true);
        $invoke_obj = $object;
        if($method->isStatic()) {
            //static no need obj
            $invoke_obj = null;
        }
        return $method->invokeArgs($invoke_obj, $args);
    }

    public static function invokePublicMethod($object, $method, $args)
    {
        if(empty($args)) {
            return $object->$method();
        } else if(count($args) == 1) {
            return $object->$method($args[0]);
        } else if(count($args) == 2) {
            return $object->$method($args[0], $args[1]);
        } else if(count($args) == 3) {
            return $object->$method($args[0], $args[1], $args[2]);
        } else if(count($args) == 4) {
            return $object->$method($args[0], $args[1], $args[2], $args[3]);
        } else if(count($args) == 5) {
            return $object->$method($args[0], $args[1], $args[2], $args[3], $args[4]);
        } else if(count($args) == 6) {
            return $object->$method($args[0], $args[1], $args[2], $args[3], $args[4], $args[5]);
        } else {
            return call_user_func_array(array(
                    $object, 
                    $method 
            ), $args);
        }
    }

    /**
     * 通过反射设置非公共属性
     * @param object $object
     * @param array $properties
     */
    public static function forceSetProperties($object, $properties, $style = Apf_Util_BeanUtil::MAGIC_STYLE)
    {
        $noPublicProps = array();
        foreach($properties as $prop => $value) {
            $setName = self::getSetName($prop);
            if(is_callable($setName)) {
                $object->$setName($value);
            } else {
                $noPublicProps[$prop] = $value;
            }
        }
        if(! empty($noPublicProps)) {
            $reflectObj = new ReflectionObject($object);
            $allProperties = $reflectObj->getProperties();
            
            $relateAllProperties = array();
            foreach($allProperties as $refProp) {
                $refProp->setAccessible(true);
                $relateAllProperties[$refProp->getName()] = $refProp;
            }
            
            foreach($noPublicProps as $propName => $value) {
                
                if($style === Apf_Util_BeanUtil::MAGIC_STYLE) {
                    $phpPropName = Apf_Util_BeanUtil::convetPhpStyle($propName);
                    $javaPropName = Apf_Util_BeanUtil::convertJavaStyle($propName);
                    $refProp = isset($relateAllProperties[$phpPropName]) ? $relateAllProperties[$phpPropName] : $relateAllProperties[$javaPropName];
                } else {
                    $refProp = $relateAllProperties[$propName];
                }
                
                if($refProp) {
                    $refProp->setValue($object, $value);
                } else {
                    if(self::getLogger()->isWarnEnabled()) {
                        self::getLogger()->warns("no prop found $propName", get_class($object));
                    }
                }
            }
        }
    }

    public static function getAllProperties($object)
    {
        $reflectObj = new ReflectionObject($object);
        $allProperties = $reflectObj->getProperties();
        $rt = array();
        foreach($allProperties as $refProp) {
            $refProp->setAccessible(true);
            
            $rt[$refProp->getName()] = array(
                    Reflection::getModifierNames($refProp->getModifiers()), 
                    $refProp->getValue($object) 
            );
        }
        return $rt;
    }

    /**
     *
     * @param object $object
     * @param array $objectMap
     *     array('className'=>'objectName')
     */
    public static function likeSpringInitObject($object, $objectMap)
    {
        $initedProps = array();
        if(empty($objectMap)) {
            return;
        }
        if($object == null) {
            self::getLogger()->errorsAndThrowException("object may not be null");
        }
        foreach($objectMap as $className => $objectName) {
            if(empty($objectName)) {
                //小驼峰
                $objectName = self::getAutoObjectName($className);
            }
            
            if(isset($initedProps[$objectName])) {
                self::getLogger()->errorsAndThrowException("likeSpringInitObject found repeat object $objectName ");
            }
            
            $initedProps[$objectName] = Apf_Proxy_ProxyFactory::getInstance($className);
        }
        
        if(! empty($initedProps)) {
            self::forceSetProperties($object, $initedProps);
        }
    }

    private static function getLogger()
    {
        return Apf_Logger_LoggerFactory::getLogger(__CLASS__);
    }

    /**
     * input foo
     * output setFoo
     * @param string $name
     * @return string
     */
    public static function getSetName($name)
    {
        return 'set' . ucfirst($name);
    }

    /**
     * 类似spring自动注解，传入 Foo_Bar将返回bar
     * @param string $className
     */
    public static function getAutoObjectName($className)
    {
        $tmp = explode('_', $className);
        return lcfirst($tmp[count($tmp) - 1]);
    }
}