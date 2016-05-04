package main

import (
  "fmt"
  "io/ioutil"
  "os"
  "github.com/ugorji/go/codec"
)

type Data struct {
  A int `codec:"a"`
  B map[string]string `codec:"b"`
  C []int `codec:"c"`
}

func main () {

  _b := make(map[string]string)
  _b["name"] = "你好"

  var v1 Data
  v1.A = 10
  v1.B =_b
  v1.C = []int{1, 2, 3}

  var b []byte = make([]byte, 0, 128)
  var jh codec.MsgpackHandle
  jh.RawToString = true
  var enc *codec.Encoder = codec.NewEncoderBytes(&b, &jh)
  enc.Encode(v1)

  filename := "/tmp/test.msgpack"
  ioutil.WriteFile(filename, b, 0644)
  fmt.Println("encoded data has been written to", filename)

  content, err := ioutil.ReadAll(os.Stdin)

  fmt.Println(string(content))

  var d Data
  var h codec.MsgpackHandle
  h.RawToString = true
  // set to true if don't want to decode bytes string from Python
  // h.RawToString = true

  var dec *codec.Decoder = codec.NewDecoderBytes(content, &h)
  e := dec.Decode(&d)

  if e != nil {
    fmt.Println(err)
  } else {
    fmt.Printf("decoded: %v\n", d)
  }

}
