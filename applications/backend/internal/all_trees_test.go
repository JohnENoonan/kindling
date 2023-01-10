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

func testAllTrees(t *testing.T, context spec.G, it spec.S) {
	var (
		withT  = NewWithT(t)
		Expect = withT.Expect

		allTreesHandler      internal.AllTreesHandler
		selectedTreesHandler *internal.SelectedTreesHandler
		request              *http.Request
		response             *httptest.ResponseRecorder
	)

	it.Before(func() {
		selectedTreesHandler = internal.NewSelectedTreesHandler().WithTrees([]internal.FrontendTree{
			{
				TreeID:    "180683",
				Latitude:  "40.72309177",
				Longitude: "-73.84421522",
			},
		})

		allTreesHandler = internal.NewAllTreesHandler(selectedTreesHandler).WithTrees([]internal.BackendTree{
			{
				TreeID:    "180683",
				Latitude:  "40.72309177",
				Longitude: "-73.84421522",
			},
			{
				TreeID:    "203468",
				Latitude:  "40.71760215",
				Longitude: "-73.84915064",
			},
			{
				TreeID:    "12345",
				Latitude:  "50.0",
				Longitude: "-75.0",
			},
		})

		request = httptest.NewRequest(
			"GET",
			"http://example.com/all-trees?latitude=40.72309177&longitude=-73.84421522&radius=0.5",
			nil,
		)
		response = httptest.NewRecorder()
	})

	it("returns all trees in a given area", func() {
		allTreesHandler.ServeHTTP(response, request)

		var trees []internal.FrontendTree
		err := json.NewDecoder(response.Body).Decode(&trees)
		Expect(err).NotTo(HaveOccurred())

		Expect(trees).To(ConsistOf([]internal.FrontendTree{
			{
				TreeID:    "180683",
				Latitude:  "40.72309177",
				Longitude: "-73.84421522",
				Selected:  true,
				Bio:       "Lorem ipsum",
			},
			{
				TreeID:    "203468",
				Latitude:  "40.71760215",
				Longitude: "-73.84915064",
				Selected:  false,
				Bio:       "Lorem ipsum",
			},
		}))
	})

	context("when there are more than allotted results", func() {
		it.Before(func() {
			allTreesHandler = allTreesHandler.WithReturnLimit(1)
		})

		it("returns only 2 trees", func() {
			allTreesHandler.ServeHTTP(response, request)

			var trees []internal.FrontendTree
			err := json.NewDecoder(response.Body).Decode(&trees)
			Expect(err).NotTo(HaveOccurred())

			Expect(len(trees)).To(Equal(1))
		})
	})

	context("failure cases", func() {
		context("when the query parameters cannot be parsed", func() {
			context("the latitude cannot be parsed", func() {
				it.Before(func() {
					request = httptest.NewRequest(
						"GET",
						"http://example.com/all-trees?latitude=fail&longitude=-73.84421522&radius=0.5",
						nil,
					)
				})

				it("retuns a 400 error and an error message", func() {
					allTreesHandler.ServeHTTP(response, request)
					Expect(response.Code).To(Equal(400))

					message, err := io.ReadAll(response.Body)
					Expect(err).NotTo(HaveOccurred())

					Expect(string(message)).To(Equal(`failed to convert "latitude"`))
				})
			})

			context("the longitude cannot be parsed", func() {
				it.Before(func() {
					request = httptest.NewRequest(
						"GET",
						"http://example.com/all-trees?latitude=40.72309177&longitude=fail&radius=0.5",
						nil,
					)
				})

				it("retuns a 400 error and an error message", func() {
					allTreesHandler.ServeHTTP(response, request)
					Expect(response.Code).To(Equal(400))

					message, err := io.ReadAll(response.Body)
					Expect(err).NotTo(HaveOccurred())

					Expect(string(message)).To(Equal(`failed to convert "longitude"`))
				})
			})

			context("the radius cannot be parsed", func() {
				it.Before(func() {
					request = httptest.NewRequest(
						"GET",
						"http://example.com/all-trees?latitude=40.72309177&longitude=-73.84421522&radius=fail",
						nil,
					)
				})

				it("retuns a 400 error and an error message", func() {
					allTreesHandler.ServeHTTP(response, request)
					Expect(response.Code).To(Equal(400))

					message, err := io.ReadAll(response.Body)
					Expect(err).NotTo(HaveOccurred())

					Expect(string(message)).To(Equal(`failed to convert "radius"`))
				})
			})
		})

		context("when the struct fields cannot be parsed", func() {
			context("the latitude cannot be parsed", func() {
				it.Before(func() {
					allTreesHandler = allTreesHandler.WithTrees([]internal.BackendTree{
						{
							TreeID:    "180683",
							Latitude:  "fail",
							Longitude: "-73.84421522",
						},
					})
				})

				it("retuns a 400 error and an error message", func() {
					allTreesHandler.ServeHTTP(response, request)
					Expect(response.Code).To(Equal(400))

					message, err := io.ReadAll(response.Body)
					Expect(err).NotTo(HaveOccurred())

					Expect(string(message)).To(Equal(`failed to convert "latitude" in struct`))
				})
			})

			context("the longitude cannot be parsed", func() {
				it.Before(func() {
					allTreesHandler = allTreesHandler.WithTrees([]internal.BackendTree{
						{
							TreeID:    "180683",
							Latitude:  "40.72309177",
							Longitude: "fail",
						},
					})
				})

				it("retuns a 400 error and an error message", func() {
					allTreesHandler.ServeHTTP(response, request)
					Expect(response.Code).To(Equal(400))

					message, err := io.ReadAll(response.Body)
					Expect(err).NotTo(HaveOccurred())

					Expect(string(message)).To(Equal(`failed to convert "longitude" in struct`))
				})
			})
		})

		context("when you make a call with an unsupported method", func() {
			it.Before(func() {
				request = httptest.NewRequest(
					"POST",
					"http://example.com/all-trees?latitude=40.72309177&longitude=-73.84421522&radius=0.5",
					nil,
				)
			})

			it("returns a 405 error", func() {
				allTreesHandler.ServeHTTP(response, request)
				Expect(response.Code).To(Equal(405))
			})
		})
	})
}
