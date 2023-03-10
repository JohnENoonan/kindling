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
	var dataFilePath, selectedFilePath, biosFile string
	set := flag.NewFlagSet("", flag.ContinueOnError)
	set.StringVar(&dataFilePath, "data-file-path", "", "path to the data file")
	set.StringVar(&selectedFilePath, "selected-file-path", "", "path to the selected trees file")
	set.StringVar(&biosFile, "bios-file", "", "path to the bios file")
	err := set.Parse(os.Args[1:])
	if err != nil {
		log.Fatal(err)
	}

	if dataFilePath == "" {
		log.Fatal("--data-file-path is required")
	}

	if selectedFilePath == "" {
		log.Fatal("--selected-file-path is required")
	}

	if biosFile == "" {
		log.Fatal("--bios-file is required")
	}

	log.Println("Data is loading...")

	data, err := os.Open(dataFilePath)
	if err != nil {
		log.Fatal(err)
	}

	var trees []internal.BackendTree
	err = json.NewDecoder(data).Decode(&trees)
	if err != nil {
		log.Fatal(err)
	}

	// Close the file here otherwise it will stay open for the entire life time
	// of the server
	err = data.Close()
	if err != nil {
		log.Fatal(err)
	}

	selected, err := os.OpenFile(selectedFilePath, os.O_RDONLY|os.O_CREATE, 0666)
	if err != nil {
		log.Fatal(err)
	}

	info, err := selected.Stat()
	if err != nil {
		log.Fatal(err)
	}

	// This needs to be intialized here in the case that the file does not exist
	var selectedTrees []internal.FrontendTree

	// If the existing file is of size 0 do not try and parse as it is a new file
	if info.Size() != 0 {
		err = json.NewDecoder(selected).Decode(&selectedTrees)
		if err != nil {
			log.Fatal(err)
		}
	}

	// Close the file here otherwise it will stay open for the entire life time
	// of the server
	err = selected.Close()
	if err != nil {
		log.Fatal(err)
	}

	bios, err := os.Open(biosFile)
	if err != nil {
		log.Fatal(err)
	}

	var bioTable []internal.BioEntry
	err = json.NewDecoder(bios).Decode(&bioTable)
	if err != nil {
		log.Fatal(err)
	}

	// Close the file here otherwise it will stay open for the entire life time
	// of the server
	err = bios.Close()
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Data is loaded!")

	selectedTreesHandler := internal.NewSelectedTreesHandler().WithTrees(selectedTrees).WithDataFile(selectedFilePath)
	http.Handle("/selected-trees", selectedTreesHandler)

	allTreesHandler := internal.NewAllTreesHandler(selectedTreesHandler).WithTrees(trees).WithBios(internal.BioTable{Table: bioTable})
	http.Handle("/all-trees", allTreesHandler)

	randomTreeHandler := internal.NewRandomTreeHandler(&allTreesHandler)
	http.Handle("/random-tree", randomTreeHandler)

	log.Println("Server is now live at localhost:8090")
	http.ListenAndServe("127.0.0.1:8090", nil)
}
