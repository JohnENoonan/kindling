package internal

type BackendTree struct {
	TreeID    string `json:"tree_id"`
	Latitude  string `json:"latitude"`
	Longitude string `json:"longitude"`
}

type FrontendTree struct {
	TreeID    string `json:"tree_id"`
	Latitude  string `json:"latitude"`
	Longitude string `json:"longitude"`
}

func (bt BackendTree) MakeFront() FrontendTree {
	return FrontendTree{
		TreeID:    bt.TreeID,
		Latitude:  bt.Latitude,
		Longitude: bt.Longitude,
	}

}
