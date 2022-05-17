package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"log"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		
		b, err := ioutil.ReadAll(r.Body)
		if err != nil {
			w.Write([]byte(fmt.Sprintf("Got error while reading body: %v", err)))
			return
		}
		fmt.Printf("Body length: %d Body: %q", len(b), b)
		w.Write([]byte(fmt.Sprintf("Body length: %d Body: %q", len(b), b)))
	})

	fmt.Printf("Server Starting at port 80") 
	if err := http.ListenAndServe(":80", nil) ; err != nil {
		log.Fatal(err)
	}
}
