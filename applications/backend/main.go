package main

import (
	"encoding/json"
	"flag"
	"log"
	"net/http"
	"os"

	"github.com/JohnENoonan/kindling/internal"
)

func main() {
	var dataFilePath string
	set := flag.NewFlagSet("", flag.ContinueOnError)
	set.StringVar(&dataFilePath, "data-file-path", "", "path to the data file")
	err := set.Parse(os.Args[1:])
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Data is loading...")

	data, err := os.Open(dataFilePath)
	if err != nil {
		log.Fatal(err)
	}
	defer data.Close()

	var trees []internal.BackendTree
	err = json.NewDecoder(data).Decode(&trees)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Data is loaded!")

	// TODO:Add data loading and saving internally (this will require another modifier)
	selectedTreesHandler := internal.NewSelectedTreesHandler()
	http.Handle("/selected-trees", selectedTreesHandler)

	allTreesHandler := internal.NewAllTreesHandler(selectedTreesHandler).WithTrees(trees)
	http.Handle("/all-trees", allTreesHandler)

	log.Println("Server is now live at localhost:8090")
	http.ListenAndServe(":8090", nil)
}
