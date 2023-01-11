package internal

import (
	"encoding/json"
	"net/http"
	"os"
	"sync"
)

type SelectedTreesHandler struct {
	trees    []FrontendTree
	dataFile string
	mutex    sync.Mutex
}

func (s *SelectedTreesHandler) WithTrees(trees []FrontendTree) *SelectedTreesHandler {
	s.trees = trees
	return s
}

func (s *SelectedTreesHandler) WithDataFile(dataFile string) *SelectedTreesHandler {
	s.dataFile = dataFile
	return s
}

func (s *SelectedTreesHandler) IsSelected(id string) bool {
	var selected bool

	// Ensures that the list is not being updated
	s.mutex.Lock()
	for _, t := range s.trees {
		if t.TreeID == id {
			selected = true
			break
		}
	}
	s.mutex.Unlock()

	return selected
}

// This must create a pointer to the handler to allow for the list the be
// updated on the objects
func NewSelectedTreesHandler() *SelectedTreesHandler {
	return &SelectedTreesHandler{}
}

func (s *SelectedTreesHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		var tree FrontendTree
		err := json.NewDecoder(r.Body).Decode(&tree)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to parse JSON in the request body`))
			return
		}

		tree.Selected = true

		// Ensure that the list is not being read or updated in another thread
		s.mutex.Lock()
		s.trees = append(s.trees, tree)

		// Open file in write only mode and truncate it, create the file if it does
		// not exists, set it to read write for owner, group, and user
		f, err := os.OpenFile(s.dataFile, os.O_WRONLY|os.O_TRUNC|os.O_CREATE, 666)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to open or create data file`))
			return
		}

		err = json.NewEncoder(f).Encode(s.trees)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to encode selected trees data`))
			return
		}

		err = f.Close()
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to close selected trees file descriptor`))
			return
		}

		s.mutex.Unlock()

		w.WriteHeader(http.StatusCreated)

	case "GET":
		err := json.NewEncoder(w).Encode(s.trees)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to encode and send JSON`))
			return
		}

	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}
