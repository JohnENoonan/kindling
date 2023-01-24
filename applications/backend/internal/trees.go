package internal

type BackendTree struct {
	TreeID       int     `json:"tree_id"`
	SpeciesID    int     `json:"species_id"`
	Name         string  `json:"name"`
	Diameter     int     `json:"diameter"`
	SpcLatin     string  `json:"spc_latin"`
	SpcCommon    string  `json:"spc_common"`
	Introverted  bool    `json:"introverted"`
	HasGuards    bool    `json:"has_guards"`
	RootProblems bool    `json:"root_problems"`
	HasLights    bool    `json:"has_lights"`
	HasShoes     bool    `json:"has_shoes"`
	Address      string  `json:"address"`
	Zipcode      int     `json:"zipcode"`
	Neighborhood string  `json:"neighborhood"`
	Latitude     float64 `json:"latitude"`
	Longitude    float64 `json:"longitude"`
}

type FrontendTree struct {
	TreeID    int     `json:"tree_id"`
	SpeciesID int     `json:"species_id"`
	SpcLatin  string  `json:"spc_latin" `
	SpcCommon string  `json:"spc_common"`
	Name      string  `json:"name"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`

	Bio      string   `json:"bio"`
	Selected bool     `json:"selected"`
	Features Features `json:"features"`
}

type Features struct {
	Diameter     int    `json:"diameter"`
	Introverted  bool   `json:"introverted"`
	HasGuards    bool   `json:"has_guards"`
	RootProblems bool   `json:"root_problems"`
	HasLights    bool   `json:"has_lights"`
	HasShoes     bool   `json:"has_shoes"`
	Address      string `json:"address"`
	Zipcode      int    `json:"zipcode"`
	Neighborhood string `json:"neighborhood"`
}

func (bt BackendTree) MakeFront(selected bool, bio string) FrontendTree {
	return FrontendTree{
		TreeID:    bt.TreeID,
		SpeciesID: bt.SpeciesID,
		SpcLatin:  bt.SpcLatin,
		SpcCommon: bt.SpcCommon,
		Name:      bt.Name,
		Latitude:  bt.Latitude,
		Longitude: bt.Longitude,
		Selected:  selected,
		Bio:       bio,
		Features: Features{
			Diameter:     bt.Diameter,
			Introverted:  bt.Introverted,
			HasGuards:    bt.HasGuards,
			RootProblems: bt.RootProblems,
			HasLights:    bt.HasLights,
			HasShoes:     bt.HasShoes,
			Address:      bt.Address,
			Zipcode:      bt.Zipcode,
			Neighborhood: bt.Neighborhood,
		},
	}
}
