package internal

type BackendTree struct {
	TreeID    string `json:"tree_id"`
	TreeDbh   string `json:"tree_dbh"`
	SpcLatin  string `json:"spc_latin" `
	SpcCommon string `json:"spc_common"`
	Latitude  string `json:"latitude"`
	Longitude string `json:"longitude"`
}

type FrontendTree struct {
	TreeID    string `json:"tree_id"`
	SpcLatin  string `json:"spc_latin" `
	SpcCommon string `json:"spc_common"`
	Latitude  string `json:"latitude"`
	Longitude string `json:"longitude"`

	Bio      string   `json:"bio"`
	Selected bool     `json:"selected"`
	Features Features `json:"features"`
}

type Features struct {
	Diameter string `json:"diameter"`
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
