package internal

type BackendTree struct {
	TreeID    string  `json:"tree_id"`
	TreeDbh   int     `json:"tree_dbh"`
	SpcLatin  string  `json:"spc_latin" `
	SpcCommon string  `json:"spc_common"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
}

type FrontendTree struct {
	TreeID    string  `json:"tree_id"`
	SpcLatin  string  `json:"spc_latin" `
	SpcCommon string  `json:"spc_common"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`

	Bio      string   `json:"bio"`
	Selected bool     `json:"selected"`
	Features Features `json:"features"`
}

type Features struct {
	Diameter int `json:"diameter"`
}

func (bt BackendTree) MakeFront(selected bool, bio string) FrontendTree {
	return FrontendTree{
		TreeID:    bt.TreeID,
		SpcLatin:  bt.SpcLatin,
		SpcCommon: bt.SpcCommon,
		Latitude:  bt.Latitude,
		Longitude: bt.Longitude,
		Selected:  selected,
		Bio:       bio,
		Features: Features{
			Diameter: bt.TreeDbh,
		},
	}
}
