package main

import (
	"fmt"
	"github.com/Shopify/sarama"
	"log"
	"time"
)

const LOG_INFO int = 1
const LOG_WARNING int = 2
const LOG_ERROR int = 3

type LogEntry struct {
	Message string
	Level   int

	encoded []byte
	err     error
}

func (entry *LogEntry) ensureEncoded() {
	if entry.encoded == nil {
		now := time.Now()
		entry.encoded = []byte(
			fmt.Sprintf(
				"[%.26s (%-7s)] %+v",
				now, entry.getLevel(), entry.Message))
	}
}

func (entry *LogEntry) getLevel() string {
	rv := ""
	if entry.Level == LOG_INFO {
		return "INFO"
	}
	if entry.Level == LOG_WARNING {
		return "WARNING"
	}
	if entry.Level == LOG_ERROR {
		return "ERROR"
	}
	return rv
}

func (entry *LogEntry) Length() int {
	entry.ensureEncoded()
	return len(entry.encoded)
}

func (entry *LogEntry) Encode() ([]byte, error) {
	entry.ensureEncoded()
	return entry.encoded, entry.err
}

func main() {
	config := sarama.NewConfig()
	config.Producer.RequiredAcks = sarama.WaitForLocal
	config.Producer.Retry.Max = 10

	producer, err := sarama.NewAsyncProducer(
		[]string{"127.0.0.1:9092"}, config)

	if err != nil {
		log.Fatalln("Failed to start Sarama producer:", err)
	}

	go func() {
		for err := range producer.Errors() {
			log.Println("Failed to write log:", err)
		}
	}()

	kafkaLog := func(level int, message string) {
		entry := &LogEntry{
			Message: message,
			Level:   LOG_INFO,
		}
		producer.Input() <- &sarama.ProducerMessage{
			Topic: "test",
			Value: entry,
		}
	}

	for {
		kafkaLog(LOG_INFO, "test info")
		kafkaLog(LOG_WARNING, "test warning")
		time.Sleep(time.Second * 1)
	}

}
