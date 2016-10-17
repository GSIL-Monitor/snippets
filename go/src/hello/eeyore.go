package main

import (
	"bytes"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"strconv"
	"time"
)

import (
	"github.com/ugorji/go/codec"
)

type IdfaConfig struct {
	AdvertiserId          int64  `codec:"ad_id"`
	AppId                 int64  `codec:"app_id"`
	Enabled               bool   `codec:"is_enabled"`
	TemplateCode          string `codec:"template_code"`
	SharedKey             string `codec:"shared_key"`
	RequestContentType    string `codec:"req_content_type"`
	RequestHttpMethod     string `codec:"req_http_method"`
	RequestIDFALowerCaser bool   `codec:"req_idfa_lowercase"`
	RequestIDFAMaxNum     int    `codec:"req_idfa_maxnum"`
	RequestIDFANoHyphen   bool   `codec:"req_idfa_nohyphen"`
	ResponseIDFANoHyphen  bool   `codec:"res_idfa_nohyphen"`
	ResponseJSONFormat    string `codec:"res_json_format"`
	ExtendedField         string `codec:"ext_field"`
	Timestamp             int
}

type IdfaConfigResponse struct {
	Status string       `codec:"status"`
	Data   []IdfaConfig `codec:"data"`
}

type IDFAConfigLoader struct {
	BaseURL     string
	CacheExpiry int

	configByAdvertiserId map[int64]IdfaConfig
	configByAppId        map[int64]IdfaConfig
}

func (i *IDFAConfigLoader) Init() {
	i.configByAppId = make(map[int64]IdfaConfig)
	i.configByAdvertiserId = make(map[int64]IdfaConfig)
}

func (i *IDFAConfigLoader) GetConfigByAdvertiserId(
	advertiser_id int64) IdfaConfig {

	var ok bool
	var config IdfaConfig

	// get from in-memory cache
	if config, ok = i.configByAdvertiserId[advertiser_id]; ok {
		if int(time.Now().Unix())-config.Timestamp < i.CacheExpiry {
			return config
		}
	}

	var _url string
	var timeout time.Duration
	var text []byte
	var err error
	var rv IdfaConfig
	var httpCode int
	var data url.Values

	_url = i.BaseURL
	data = url.Values{}
	data.Set("ad_id", strconv.FormatInt(advertiser_id, 10))

	httpCode, text, _ = HttpRequest(
		"GET",   // method
		_url,    // url
		data,    // data
		timeout, // timeout
		"",      // content-type
	)

	if httpCode != 200 {
		return rv
	}

	var c *IdfaConfigResponse = &IdfaConfigResponse{}
	var h codec.JsonHandle
	var dec *codec.Decoder = codec.NewDecoderBytes(text, &h)
	err = dec.Decode(c)

	if err != nil {
		log.Println("HttpRequestGet():", err)
		return rv
	}

	log.Printf("%+v", c)

	// log.Printf("%+v", c)
	if len(c.Data) > 0 {
		rv = c.Data[0]
		if rv.Enabled {
			rv.Timestamp = int(time.Now().Unix())
			i.configByAdvertiserId[advertiser_id] = rv
		}
	}
	return rv
}

func HttpRequest(
	method string, _url string,
	data url.Values, timeout time.Duration,
	content_type string) (int, []byte, error) {

	var u *url.URL
	var q url.Values
	var err error

	if method == "GET" {
		u, err = url.Parse(_url)

		if err != nil {
			log.Println("HttpRequest():", err)
			return 0, []byte(""), err
		}

		if data != nil {
			q = u.Query()
			for k, v := range data {
				for _v := range v {
					q.Add(k, v[_v])
				}
			}
			u.RawQuery = q.Encode()

		}
		log.Println(u.String())
		return HttpRequestGet(u.String(), timeout, content_type)
	}

	return 0, []byte(""), err
}

func HttpRequestGet(
	url string, timeout time.Duration, content_type string) (int, []byte, error) {
	var req *http.Request
	var resp *http.Response
	var client *http.Client
	var text []byte
	var err error

	req, err = http.NewRequest("GET", url, nil)
	if len(content_type) > 0 {
		req.Header.Set("Content-Type", content_type)
	}

	client = &http.Client{
		Timeout: timeout,
	}

	resp, err = client.Do(req)
	if err != nil {
		log.Println("HttpRequestGet():", err)
		return 0, []byte(""), err
	}

	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		log.Println("HttpRequestGet() status not 200:", err)
		return resp.StatusCode, []byte(""), err
	}

	text, _ = ioutil.ReadAll(resp.Body)
	log.Println(string(text))
	return resp.StatusCode, text, err

}

func HttpRequestPost(
	_url string, timeout time.Duration,
	data url.Values, content_type string) (int, []byte, error) {
	return HttpRequestNonGet("POST", _url, data, timeout, content_type)
}

func HttpRequestNonGet(
	method string, _url string,
	data url.Values, timeout time.Duration,
	content_type string) (int, []byte, error) {

	var body *bytes.Buffer
	var req *http.Request
	var resp *http.Response
	var client *http.Client
	var err error

	if method != "GET" && method != "POST" {
		log.Printf("HttpRequestNonGet(): unsupported method %s", method)
		return 0, []byte(""), err
	}

	body = bytes.NewBuffer([]byte(data.Encode()))
	req, err = http.NewRequest(method, _url, body)

	if err != nil {
		log.Println("HttpRequestNonGet():", err)
		return 0, []byte(""), err
	}

	if len(content_type) > 0 {
		req.Header.Set("Content-Type", content_type)
	} else {
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	}

	client = &http.Client{
		Timeout: timeout,
	}

	log.Printf("sending %s request to %s", method, _url)

	resp, err = client.Do(req)
	if err != nil {
		log.Println("HttpRequestNonGet():", err)
		return 0, []byte(""), err
	}

	defer resp.Body.Close()
	text, _ := ioutil.ReadAll(resp.Body)

	return resp.StatusCode, text, err
}

func main() {
	// i = getIdfaConfigByAppId(1)
	// log.Printf("%+v", i)
	/*
			var data url.Values
					data = url.Values{}
					data.Set("hello", "world")
				var b []byte
				_, b, _ = HttpRequestNonGet(
					"POST", // method
					"http://127.0.0.1:4567/post", // url
					data,           // data
	time.Second*30, // timeout
					"",             // content-type
				)
				log.Printf("%+v", string(b))
	*/

	var l = IDFAConfigLoader{
		BaseURL:     "http://127.0.0.1:4567/ops_api/idfa/verify",
		CacheExpiry: 60,
	}
	l.Init()
	// var i IdfaConfig
	for {
		l.GetConfigByAdvertiserId(1)
		// log.Printf("%+v", i)
	}
}
