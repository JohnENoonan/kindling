package internal_test

import (
	"bytes"
	"encoding/json"
	"io"
	"os"
	"path/filepath"
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

		dataFile string
	)

	context("POST", func() {
		it.Before(func() {
			f, err := os.CreateTemp("", "selected.json")
			Expect(err).NotTo(HaveOccurred())
			defer f.Close()

			dataFile = f.Name()

			selectedTreesHandler = internal.NewSelectedTreesHandler().
				WithTrees([]internal.FrontendTree{
					{
						TreeID:    "180683",
						Latitude:  40.72309177,
						Longitude: -73.84421522,
						Selected:  true,
					},
				}).
				WithDataFile(dataFile)

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

		it.After(func() {
			Expect(os.RemoveAll(dataFile)).To(Succeed())
		})

		it("adds the given tree to the list of known trees", func() {
			selectedTreesHandler.ServeHTTP(response, request)

			Expect(response.Code).To(Equal(201))

			f, err := os.Open(dataFile)
			Expect(err).NotTo(HaveOccurred())
			defer f.Close()

			var trees []internal.FrontendTree
			err = json.NewDecoder(f).Decode(&trees)
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

		context("failure cases", func() {
			context("when the request body cannot be parsed", func() {
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

			context("when the data file cannot be accessed or created", func() {
				var tempDir string

				it.Before(func() {
					var err error
					tempDir, err = os.MkdirTemp("", "temp")
					Expect(err).NotTo(HaveOccurred())

					dataFile = filepath.Join(tempDir, "selected.json")

					Expect(os.Chmod(tempDir, 0000)).To(Succeed())

					selectedTreesHandler = selectedTreesHandler.WithDataFile(dataFile)
				})

				it.After(func() {
					Expect(os.Chmod(tempDir, os.ModePerm)).To(Succeed())
					Expect(os.RemoveAll(tempDir))
				})

				it("retuns a 400 error and an error message", func() {
					selectedTreesHandler.ServeHTTP(response, request)
					Expect(response.Code).To(Equal(400))

					message, err := io.ReadAll(response.Body)
					Expect(err).NotTo(HaveOccurred())

					Expect(string(message)).To(Equal(`failed to open or create data file`))
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
