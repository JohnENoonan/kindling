package internal_test

import (
	"encoding/json"
	"io"
	"testing"

	"net/http"
	"net/http/httptest"

	"github.com/JohnENoonan/kindling/internal"
	"github.com/sclevine/spec"

	. "github.com/onsi/gomega"
)

func testRandomTree(t *testing.T, context spec.G, it spec.S) {
	var (
		withT  = NewWithT(t)
		Expect = withT.Expect

		randomTreeHandler    internal.RandomTreeHandler
		allTreesHandler      internal.AllTreesHandler
		selectedTreesHandler *internal.SelectedTreesHandler
		request              *http.Request
		response             *httptest.ResponseRecorder
	)

	context("GET", func() {
		it.Before(func() {
			selectedTreesHandler = internal.NewSelectedTreesHandler().WithTrees([]internal.FrontendTree{
				{
					TreeID:    180683,
					Latitude:  40.72309177,
					Longitude: -73.84421522,
				},
			})

			allTreesHandler = internal.NewAllTreesHandler(selectedTreesHandler).
				WithTrees([]internal.BackendTree{
					{
						TreeID:    180683,
						Latitude:  40.72309177,
						Longitude: -73.84421522,
					},
					{
						TreeID:    203468,
						SpcCommon: "Pine",
						Latitude:  40.71760215,
						Longitude: -73.84915064,
					},
				}).
				WithBios(internal.BioTable{
					Table: []internal.BioEntry{
						{
							Indentifier: internal.Indentifier{
								SpcCommon: "Pine",
								Diameter:  -1,
							},
							Bios: []string{"Pine for me", "test1", "test2"},
						},
					},
				})

			randomTreeHandler = internal.NewRandomTreeHandler(&allTreesHandler)

			request = httptest.NewRequest(
				"GET",
				"http://example.com/random-tree",
				nil,
			)
			response = httptest.NewRecorder()
		})

		it("returns all trees in a given area", func() {
			randomTreeHandler.ServeHTTP(response, request)

			var tree internal.FrontendTree
			err := json.NewDecoder(response.Body).Decode(&tree)
			Expect(err).NotTo(HaveOccurred())

			Expect(tree).To(Equal(internal.FrontendTree{
				TreeID:    203468,
				SpcCommon: "Pine",
				Latitude:  40.71760215,
				Longitude: -73.84915064,
				Selected:  false,
				Bio:       "Pine for me",
			}))
		})

		context("failure cases", func() {
			context("when a non-selected tree cannot be found", func() {
				it.Before(func() {
					selectedTreesHandler = internal.NewSelectedTreesHandler().WithTrees([]internal.FrontendTree{
						{
							TreeID: 180683,
						},
					})

					allTreesHandler = internal.NewAllTreesHandler(selectedTreesHandler).WithTrees([]internal.BackendTree{
						{
							TreeID: 180683,
						},
					})

				})

				it("returns a 400 er and an error message", func() {
					randomTreeHandler.ServeHTTP(response, request)
					Expect(response.Code).To(Equal(400))

					message, err := io.ReadAll(response.Body)
					Expect(err).NotTo(HaveOccurred())

					Expect(string(message)).To(Equal("could not find random tree what was not selected after 5 tries"))
				})
			})

			context("when you make a call with an unsupported method", func() {
				it.Before(func() {
					request = httptest.NewRequest(
						"POST",
						"http://example.com/random-tree",
						nil,
					)
				})

				it("returns a 405 error", func() {
					randomTreeHandler.ServeHTTP(response, request)
					Expect(response.Code).To(Equal(405))
				})
			})
		})
	})
}
