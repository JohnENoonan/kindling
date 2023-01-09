package internal

import (
	"encoding/json"
	"net/http"
	"sync"
)

type SelectedTreesHandler struct {
	trees []FrontendTree
	mutex sync.Mutex
}

func (s *SelectedTreesHandler) WithTrees(trees []FrontendTree) *SelectedTreesHandler {
	s.trees = trees
	return s
}

func (s SelectedTreesHandler) GetTrees() []FrontendTree {
	return s.trees
}

func (s *SelectedTreesHandler) UpdateTrees(tree FrontendTree) {
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

		s.mutex.Lock()
		s.trees = append(s.trees, tree)
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
