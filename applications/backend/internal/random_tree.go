package internal

import (
	"encoding/json"
	"net/http"
)

type RandomTreeHandler struct {
	allTreesHandler *AllTreesHandler
}

func NewRandomTreeHandler(allTreesHandler *AllTreesHandler) RandomTreeHandler {
	return RandomTreeHandler{
		allTreesHandler: allTreesHandler, // need this to get a random tree from the list of all trees
	}
}

func (rt RandomTreeHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		randomTree, err := rt.allTreesHandler.RandomTree()
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(string(err.Error())))
			return
		}

		err = json.NewEncoder(w).Encode(randomTree)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to encode and send JSON`))
			return
		}

	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}
