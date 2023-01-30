package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"os"
	"path/filepath"
	"strings"
	"time"

	gogpt "github.com/sashabaranov/go-gpt3"
)

var (
	rootProblem = []string{
		"disconnected",
		"filled with ennui",
		"depressed",
		"thirsty",
		"flat-footed",
		"lacking in confidence",
		"outdoorsy",
		"spirited",
		"fiending",
	}

	lights = []string{
		"delightful",
		"bright",
		"intelligent",
		"sparkling",
		"brilliant",
		"luminous",
		"heavenly",
		"charming",
		"radiant",
	}

	shoes = []string{
		"trying their best",
		"tattooed",
		"laid-back",
		"quirky",
		"open",
		"a bit messy",
		"lofty",
		"untidy",
		"cunning",
		"grounded",
		"chill",
		"spry",
		"hip",
	}

	gaurds = []string{
		"protective",
		"guarded",
		"defensive",
		"secretive",
		"mysterious",
		"puzzling",
		"enigmatic",
		"sappy",
		"conscientious",
		"independent",
		"reserved",
	}

	introverted = []string{
		"shy",
		"introverted",
		"anxious",
		"lonely",
		"quiet",
		"introspective",
		"a good listener",
		"academic",
		"thoughtful",
		"observant",
		"compassionate",
	}

	extroverted = []string{
		"amicable",
		"bubbly",
		"effervescent",
		"a partier",
		"outgoing",
		"easily excitable",
		"lively",
		"zealous",
		"zany",
		"friendly",
		"extroverted",
		"confident",
	}

	small = []string{
		"slim",
		"slender",
		"fit",
		"nimble",
		"lithe",
		"svelte",
	}

	medium = []string{
		"a mid-size cutie",
		"basic",
		"athletic",
		"modest",
		"average",
		"built",
	}

	large = []string{
		"thicc",
		"beefy",
		"stocky",
		"sturdy",
		"plump",
		"broad",
		"well-endowed",
		"bodacious",
		"full-figured",
	}
)

const average = 141

type Tree struct {
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

type Indentifier struct {
	Diameter     int    `json:"diameter"`
	SpcCommon    string `json:"spc_common"`
	Introverted  bool   `json:"introverted"`
	HasGuards    bool   `json:"has_guards"`
	RootProblems bool   `json:"root_problems"`
	HasLights    bool   `json:"has_lights"`
	HasShoes     bool   `json:"has_shoes"`
}

type BioTable struct {
	Indentifier Indentifier `json:"identifier"`
	Bios        []string    `json:"bios"`
}

func main() {
	var allTreesFile, inputFile, outputFile string
	set := flag.NewFlagSet("", flag.ContinueOnError)
	set.StringVar(&allTreesFile, "all-trees-file", "", "path to the all tres file")
	set.StringVar(&outputFile, "output-file", "", "path to the bio output file")
	set.StringVar(&inputFile, "input-file", "", "path to the bio input file")
	err := set.Parse(os.Args[1:])
	if err != nil {
		log.Fatal(err)
	}

	if allTreesFile == "" {
		log.Fatal("--all-trees-file is required")
	}

	if outputFile == "" {
		log.Fatal("--output-file is required")
	}

	if inputFile == "" {
		log.Fatal("--input-file is required")
	}

	fmt.Println("Loading data...")

	data, err := os.Open(allTreesFile)
	if err != nil {
		log.Fatal(err)
	}

	var trees []Tree
	err = json.NewDecoder(data).Decode(&trees)
	if err != nil {
		log.Fatal(err)
	}

	err = data.Close()
	if err != nil {
		log.Fatal(err)
	}

	ids := map[Indentifier]int{}

	for _, t := range trees {
		id := generateIdentifier(t)
		ids[id] += 1
	}

	input, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}

	var bioTable []BioTable
	err = json.NewDecoder(input).Decode(&bioTable)
	if err != nil {
		log.Fatal(err)
	}

	err = input.Close()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Done loading data!")

	c := gogpt.NewClient(os.Getenv("OPENAI_TOKEN"))
	ctx := context.Background()

	fmt.Println("Creating checkpoint directory.")

	err = os.MkdirAll("checkpoints", os.ModePerm)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Beginning bio generation.")

	now := time.Now()

	var counter, bg int
	for i, b := range bioTable {
		occurrences := ids[b.Indentifier]
		iterations := occurrences / average
		if iterations == 0 {
			iterations = 1
		}

		if len(b.Bios) >= iterations {
			continue
		}

		if counter%100 == 0 {
			fmt.Println("Creating checkpoint!")
			checkPoint, err := os.Create(filepath.Join("checkpoints", fmt.Sprintf("checkpoint%d.json", counter/100)))
			if err != nil {
				log.Fatal(err)
			}

			err = json.NewEncoder(checkPoint).Encode(&bioTable)
			if err != nil {
				log.Fatal(err)
			}

			err = checkPoint.Close()
			if err != nil {
				log.Fatal(err)
			}
		}

		if counter > 1000 {
			fmt.Printf("Went to index %d\n", i-1)
			break
		}

		for j := 0; j < (iterations - len(b.Bios)); j++ {
			req := gogpt.CompletionRequest{
				Model:     gogpt.GPT3TextDavinci003,
				MaxTokens: 256,
				Prompt:    buildPrompt(b.Indentifier),
			}

			resp, err := c.CreateCompletion(ctx, req)
			if err != nil {
				return
			}

			bioTable[i].Bios = append(bioTable[i].Bios, strings.TrimSpace(resp.Choices[0].Text))

			bg++

			if bg%100 == 0 {
				fmt.Printf("%d bios generated, currently on the %d identifier of the run\n", bg, counter)
			}
		}
		counter++
	}

	output, err := os.Create(outputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer output.Close()

	err = json.NewEncoder(output).Encode(&bioTable)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("There where %d bios generated in %s\n", bg, time.Since(now).String())

	fmt.Println("Deleting checkpoints directory!")
	err = os.RemoveAll("checkpoints")
	if err != nil {
		log.Fatal(err)
	}

}

func generateIdentifier(t Tree) Indentifier {
	var d int
	if t.Diameter < 4 {
		d = -1
	}

	if t.Diameter > 11 {
		d = 1
	}

	return Indentifier{
		SpcCommon:    t.SpcCommon,
		Diameter:     d,
		Introverted:  t.Introverted,
		HasGuards:    t.HasGuards,
		RootProblems: t.RootProblems,
		HasLights:    t.HasLights,
		HasShoes:     t.HasShoes,
	}

}

func buildPrompt(id Indentifier) string {
	prompt := "Write a dating profile that is 200 characters long for"
	if strings.ToLower(id.SpcCommon[:1]) == "a" ||
		strings.ToLower(id.SpcCommon[:1]) == "e" ||
		strings.ToLower(id.SpcCommon[:1]) == "i" ||
		strings.ToLower(id.SpcCommon[:1]) == "o" ||
		strings.ToLower(id.SpcCommon[:1]) == "u" {
		prompt += " an"
	} else {
		prompt += " a"
	}

	prompt += " " + id.SpcCommon

	rand.Seed(time.Now().Unix())

	var attributes []string

	switch id.Diameter {
	case -1:
		attributes = append(attributes, small[rand.Intn(len(small))])
	case 0:
		attributes = append(attributes, medium[rand.Intn(len(medium))])
	case 1:
		attributes = append(attributes, large[rand.Intn(len(large))])
	}

	if id.Introverted {
		attributes = append(attributes, introverted[rand.Intn(len(introverted))])
	} else {
		attributes = append(attributes, extroverted[rand.Intn(len(extroverted))])
	}

	if id.HasGuards {
		attributes = append(attributes, gaurds[rand.Intn(len(gaurds))])
	}

	if id.RootProblems {
		attributes = append(attributes, rootProblem[rand.Intn(len(rootProblem))])
	}

	if id.HasLights {
		attributes = append(attributes, lights[rand.Intn(len(lights))])
	}

	if id.HasShoes {
		attributes = append(attributes, shoes[rand.Intn(len(shoes))])
	}

	if len(attributes) > 0 {
		prompt += fmt.Sprintf(" that is %s", strings.Join(attributes, ", "))
	}

	prompt += ":"
	return prompt
}
