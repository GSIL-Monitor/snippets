package main

import (
	"bytes"
	"encoding/gob"
	"io/ioutil"
	// "log"
	"time"
)

type Status struct {
	Status0 []time.Time
	Status1 []time.Time
}

type Store struct {
	Daily map[string](map[int64]Status)
}

func dumps(store Store) ([]byte, error) {
	var b bytes.Buffer
	enc := gob.NewEncoder(&b)
	err := enc.Encode(store)

	return b.Bytes(), err
}

func loads(data []byte, s *Store) error {

	var b bytes.Buffer

	b.Write(data)

	dec := gob.NewDecoder(&b)
	err := dec.Decode(s)

	return err
}

var store Store

func add(apple_id int64, status int) {

	v := store.Daily

	key := time.Now().Format("2006-01-02")
	if _, ok := v[key]; ok {
	} else {
		v[key] = make(map[int64]Status)
	}
	if status == 0 {
		m := v[key][apple_id]
		m.Status0 = append(m.Status0, time.Now())
		v[key][apple_id] = m
		return
	}
	m := v[key][apple_id]
	m.Status1 = append(m.Status1, time.Now())
	v[key][apple_id] = m
}

func get_today(apple_id int64) (int64, int64) {
	key := time.Now().Format("2006-01-02")

	if _, ok := store.Daily[key]; !ok {
		return 0, 0
	}
	today := store.Daily[key]

	if _, ok := today[apple_id]; ok {
		m := today[apple_id]
		return int64(len(m.Status0)), int64(len(m.Status1))
	}
	return 0, 0
}

func main() {
	var s Store

	store = Store{}
	store.Daily = make(map[string](map[int64]Status))

	// idfa := "3D9F26E4-4E5F-4346-93D4-ABFEA0234FB7"

	var b []byte

	b, err := ioutil.ReadFile("dump.gob")

	if err != nil {
		for i := 0; i < 1000000; i++ {
			add(123, 0)
		}

	} else {
		err = loads(b, &s)
		if err != nil {
			panic(err)
		}
	}

	b, err = dumps(store)
	// log.Printf("%+v\n", store)

	// log.Printf("%+v", b)

	// log.Printf("%+v", s)

	// s0, s1 := get_today(123)

	//log.Printf("%+v, %+v", s0, s1)
	err = ioutil.WriteFile("dump.gob", b, 0644)
	if err != nil {
		panic(err)
	}

}
