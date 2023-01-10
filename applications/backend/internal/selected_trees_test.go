package internal_test

import (
	"bytes"
	"encoding/json"
	"io"
	"testing"

	"net/http"
	"net/http/httptest"

	"github.com/JohnENoonan/kindling/internal"
	"github.com/sclevine/spec"

	. "github.com/onsi/gomega"
)

func testSelectedTrees(t *testing.T, context spec.G, it spec.S) {
	var (
		withT  = NewWithT(t)
		Expect = withT.Expect

		selectedTreesHandler *internal.SelectedTreesHandler
		request              *http.Request
		response             *httptest.ResponseRecorder
	)

	context("POST", func() {
		it.Before(func() {
			selectedTreesHandler = internal.NewSelectedTreesHandler().WithTrees([]internal.FrontendTree{
				{
					TreeID:    "180683",
					Latitude:  40.72309177,
					Longitude: -73.84421522,
					Selected:  true,
				},
			})

			data, err := json.Marshal(internal.FrontendTree{
				TreeID:    "203468",
				Latitude:  40.71760215,
				Longitude: -73.84915064,
			})
			Expect(err).NotTo(HaveOccurred())

			request = httptest.NewRequest(
				"POST",
				"http://example.com/selected-trees",
				bytes.NewBuffer(data),
			)
			response = httptest.NewRecorder()
		})

		it("adds the given tree to the list of known trees", func() {
			selectedTreesHandler.ServeHTTP(response, request)

			Expect(response.Code).To(Equal(201))
			Expect(selectedTreesHandler.GetTrees()).To(ConsistOf([]internal.FrontendTree{
				{
					TreeID:    "180683",
					Latitude:  40.72309177,
					Longitude: -73.84421522,
					Selected:  true,
				},
				{
					TreeID:    "203468",
					Latitude:  40.71760215,
					Longitude: -73.84915064,
					Selected:  true,
				},
			}))
		})

		context("failure cases", func() {
			context("the request body cannot be parsed", func() {
				context("the latitude cannot be parsed", func() {
					it.Before(func() {
						request = httptest.NewRequest(
							"POST",
							"http://example.com/selected-trees",
							bytes.NewBuffer([]byte(`%%%`)),
						)
					})

					it("retuns a 400 error and an error message", func() {
						selectedTreesHandler.ServeHTTP(response, request)
						Expect(response.Code).To(Equal(400))

						message, err := io.ReadAll(response.Body)
						Expect(err).NotTo(HaveOccurred())

						Expect(string(message)).To(Equal(`failed to parse JSON in the request body`))
					})
				})
			})
		})
	})

	context("GET", func() {
		it.Before(func() {
			selectedTreesHandler = internal.NewSelectedTreesHandler().WithTrees([]internal.FrontendTree{
				{
					TreeID:    "180683",
					Latitude:  40.72309177,
					Longitude: -73.84421522,
					Selected:  true,
				},
				{
					TreeID:    "203468",
					Latitude:  40.71760215,
					Longitude: -73.84915064,
					Selected:  true,
				},
			})

			request = httptest.NewRequest(
				"GET",
				"http://example.com/selected-trees",
				nil,
			)
			response = httptest.NewRecorder()
		})

		it("gives list of selected trees", func() {
			selectedTreesHandler.ServeHTTP(response, request)

			var trees []internal.FrontendTree
			err := json.NewDecoder(response.Body).Decode(&trees)
			Expect(err).NotTo(HaveOccurred())

			Expect(trees).To(ConsistOf([]internal.FrontendTree{
				{
					TreeID:    "180683",
					Latitude:  40.72309177,
					Longitude: -73.84421522,
					Selected:  true,
				},
				{
					TreeID:    "203468",
					Latitude:  40.71760215,
					Longitude: -73.84915064,
					Selected:  true,
				},
			}))
		})
	})

	context("IsSelected", func() {
		it.Before(func() {
			selectedTreesHandler = internal.NewSelectedTreesHandler().WithTrees([]internal.FrontendTree{
				{
					TreeID: "180683",
				},
			})
		})

		it("returns true if the given id is in the list", func() {
			Expect(selectedTreesHandler.IsSelected("180683")).To(BeTrue())
		})

		it("returns false if the given id is not in the list", func() {
			Expect(selectedTreesHandler.IsSelected("123456")).To(BeFalse())
		})
	})

	context("failure cases", func() {
		context("when you make a call with an unsupported method", func() {
			it.Before(func() {
				selectedTreesHandler = internal.NewSelectedTreesHandler()

				request = httptest.NewRequest(
					"PUT",
					"http://example.com/selected-trees",
					nil,
				)

				response = httptest.NewRecorder()
			})

			it("returns a 405 error", func() {
				selectedTreesHandler.ServeHTTP(response, request)
				Expect(response.Code).To(Equal(405))
			})
		})
	})
}
