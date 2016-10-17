package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"strings"
	"time"
)

import (
	"github.com/ugorji/go/codec"
)

const APP_KEY = "0707"
const ZHANGYUE_URL = "http://59.151.93.147:9191/router"

type Advertiser struct {
	Id        int64
	Impl      string
	Timeout   int
	SharedKey string
	CallerId  string
}

type App struct {
	AdvertiserId int64          `codec:"ad_id"`
	Url          string         `codec:"url"`
	AppleId      int64          `codec:"apple_id"`
	IdfaType     int            `codec:"idfa_type"`
	IDFA         []string       `codec:"idfas,omitempty"`
	Result       map[string]int `codec:"result,omitempty"`
}

type Response struct {
	Code    int64                       `codec:"code"`
	Data    map[string](map[string]int) `codec:"data"`
	Message string                      `codec:"message"`
}

func SendRequestZhangyue(app App, ad Advertiser) []byte {

	u := new(url.URL)
	q := u.Query()
	q.Set("appKey", APP_KEY)
	q.Set("method", "idfa.filter")
	q.Set("format", "json")
	q.Set("v", "1.1")
	q.Set("idfas", strings.Join(app.IDFA, ","))
	_url := fmt.Sprintf("%s?%s", ZHANGYUE_URL, q.Encode())

	// fmt.Println(payload)
	req, err := http.NewRequest("GET", _url, nil)

	if err != nil {
		panic(err)
	}

	timeout := time.Second * time.Duration(ad.Timeout)
	client := &http.Client{
		Timeout: timeout,
	}

	log.Println("sending request to", _url)

	resp, err := client.Do(req)
	if err != nil {
		log.Println(err)
		return []byte("")
	}

	log.Println("status:", resp.StatusCode)
	defer resp.Body.Close()

	text, _ := ioutil.ReadAll(resp.Body)

	if resp.StatusCode != 200 {
		log.Println("status not 200:", resp.StatusCode)
		log.Println("response:", string(text))
		return []byte("")
	}

	return text
}

func HandleResponseZhangyue(text []byte) map[string]int {
	rv := make(map[string]int)
	var m Response

	// fmt.Println(string(text))

	err := codec.NewDecoderBytes(text, new(codec.JsonHandle)).Decode(&m)

	if err != nil {
		log.Println(err)
		log.Println(string(text))
	}

	if m.Code != 0 {
		log.Printf("response error: %+v", m)
		return rv
	}

	if _, ok := m.Data["idfas"]; ok {
		for k, v := range m.Data["idfas"] {
			log.Printf("%s: %d", k, v)
			rv[k] = v
		}
	}

	// fmt.Printf("%+v\n", rv)
	return rv
}

func main() {

	idfa := make([]string, 0)
	idfa = append(idfa, "881CCBCD-50F5-4A06-AB91-9D3CE7E2E70F")
	idfa = append(idfa, "89D423A6-92A2-4DD1-ADB6-40DA604E3304")

	app := App{
		AdvertiserId: 1,
		Url:          "",
		AppleId:      0,
		IdfaType:     1,
		IDFA:         idfa,
	}

	ad := Advertiser{
		Id:        0,
		Impl:      "",
		Timeout:   30,
		SharedKey: "",
		CallerId:  "",
	}

	payload := SendRequestZhangyue(app, ad)
	if len(payload) > 0 {
		log.Println(string(payload))
		result := HandleResponseZhangyue(payload)
		log.Println(result)
	}
}
