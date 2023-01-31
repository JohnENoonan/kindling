package internal

import (
	"math/rand"
)

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

type Indentifier struct {
	Diameter     int    `json:"diameter"`
	SpcCommon    string `json:"spc_common"`
	Introverted  bool   `json:"introverted"`
	HasGuards    bool   `json:"has_guards"`
	RootProblems bool   `json:"root_problems"`
	HasLights    bool   `json:"has_lights"`
	HasShoes     bool   `json:"has_shoes"`
}

type BioEntry struct {
	Indentifier Indentifier `json:"identifier"`
	Bios        []string    `json:"bios"`
}

type BioTable struct {
	Table []BioEntry
}

func (bt BackendTree) MakeFront(bio string) FrontendTree {
	return FrontendTree{
		TreeID:    bt.TreeID,
		SpeciesID: bt.SpeciesID,
		SpcLatin:  bt.SpcLatin,
		SpcCommon: bt.SpcCommon,
		Name:      bt.Name,
		Latitude:  bt.Latitude,
		Longitude: bt.Longitude,
		Selected:  false,
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

func (bt BackendTree) MakeIdentifier() Indentifier {
	var d int
	if bt.Diameter < 4 {
		d = -1
	}

	if bt.Diameter > 11 {
		d = 1
	}

	return Indentifier{
		SpcCommon:    bt.SpcCommon,
		Diameter:     d,
		Introverted:  bt.Introverted,
		HasGuards:    bt.HasGuards,
		RootProblems: bt.RootProblems,
		HasLights:    bt.HasLights,
		HasShoes:     bt.HasShoes,
	}
}

func (bioT BioTable) GetBio(t BackendTree) string {
	rand.Seed(int64(t.TreeID))

	id := t.MakeIdentifier()

	for _, be := range bioT.Table {
		if id == be.Indentifier {
			return be.Bios[rand.Intn(len(be.Bios))]
		}
	}

	return ""
}
