package main

import (
	"context"
	"fmt"
	"os"

	gogpt "github.com/sashabaranov/go-gpt3"
)

func main() {
	c := gogpt.NewClient(os.Getenv("OPENAI_TOKEN"))
	ctx := context.Background()

	prompt := "Write a dating profile for a red oak that is 200 characters or less that does not mention age:"

	req := gogpt.CompletionRequest{
		Model:     gogpt.GPT3TextDavinci003,
		MaxTokens: 256,
		Prompt:    prompt,
	}

	var bios []string

	for i := 0; i < 5; i++ {
		resp, err := c.CreateCompletion(ctx, req)
		if err != nil {
			return
		}

		bios = append(bios, resp.Choices[0].Text)
	}

	fmt.Println(prompt)
	for _, b := range bios {
		fmt.Println(b)
	}
}
