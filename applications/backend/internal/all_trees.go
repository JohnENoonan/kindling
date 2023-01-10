package internal

import (
	"encoding/json"
	"math"
	"math/rand"
	"net/http"
	"strconv"
	"time"
)

const (
	earthRadiusMi = 3958 // radius of the earth in miles.
	earthRaidusKm = 6371 // radius of the earth in kilometers.
)

// Coord represents a geographic coordinate.
type coord struct {
	Lat float64
	Lon float64
}

type AllTreesHandler struct {
	trees                []BackendTree
	selectedTreesHandler *SelectedTreesHandler
	returnLimit          int
}

func (a AllTreesHandler) WithTrees(trees []BackendTree) AllTreesHandler {
	a.trees = trees
	return a
}

func (a AllTreesHandler) WithReturnLimit(returnLimit int) AllTreesHandler {
	a.returnLimit = returnLimit
	return a
}

func NewAllTreesHandler(selectedTreesHandler *SelectedTreesHandler) AllTreesHandler {
	return AllTreesHandler{
		returnLimit:          15,                   // default return limit
		selectedTreesHandler: selectedTreesHandler, // need this to check if the tree has been selected or not
	}
}

func (a AllTreesHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		var sourceLatitude, sourceLongitude, sourceRadius float64
		var err error
		query := r.URL.Query()

		sourceLatitude, err = strconv.ParseFloat(query.Get("latitude"), 64)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to convert "latitude"`))
			return
		}
		sourceLongitude, err = strconv.ParseFloat(query.Get("longitude"), 64)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to convert "longitude"`))
			return
		}
		sourceRadius, err = strconv.ParseFloat(query.Get("radius"), 64)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to convert "radius"`))
			return
		}

		sourceCoord := coord{Lat: sourceLatitude, Lon: sourceLongitude}

		var treesInRange []FrontendTree
		for _, t := range a.trees {
			mi, _ := distance(coord{Lat: t.Latitude, Lon: t.Longitude}, sourceCoord)

			if mi <= sourceRadius {
				ft := t.MakeFront(
					a.selectedTreesHandler.IsSelected(t.TreeID),
					"Lorem ipsum",
				)
				treesInRange = append(treesInRange, ft)
			}
		}

		rand.Seed(time.Now().UnixNano())
		rand.Shuffle(len(treesInRange), func(i, j int) {
			treesInRange[i], treesInRange[j] = treesInRange[j], treesInRange[i]
		})

		if len(treesInRange) > a.returnLimit {
			treesInRange = treesInRange[:a.returnLimit]
		}

		err = json.NewEncoder(w).Encode(treesInRange)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(`failed to encode and send JSON`))
			return
		}

	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

// degreesToRadians converts from degrees to radians.
func degreesToRadians(d float64) float64 {
	return d * math.Pi / 180
}

// Distance calculates the shortest path between two coordinates on the surface
// of the Earth. This function returns two units of measure, the first is the
// distance in miles, the second is the distance in kilometers.
func distance(p, q coord) (mi, km float64) {
	lat1 := degreesToRadians(p.Lat)
	lon1 := degreesToRadians(p.Lon)
	lat2 := degreesToRadians(q.Lat)
	lon2 := degreesToRadians(q.Lon)

	diffLat := lat2 - lat1
	diffLon := lon2 - lon1

	a := math.Pow(math.Sin(diffLat/2), 2) + math.Cos(lat1)*math.Cos(lat2)*
		math.Pow(math.Sin(diffLon/2), 2)

	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))

	mi = c * earthRadiusMi
	km = c * earthRaidusKm

	return mi, km
}
