package internal_test

import (
	"testing"
	"time"

	"github.com/onsi/gomega/format"
	"github.com/sclevine/spec"
	"github.com/sclevine/spec/report"

	. "github.com/onsi/gomega"
)

func TestBackend(t *testing.T) {
	format.MaxLength = 0
	SetDefaultEventuallyTimeout(10 * time.Minute)

	suite := spec.New("backend", spec.Report(report.Terminal{}))
	suite("AllTrees", testAllTrees)
	suite("RandomTree", testRandomTree)
	suite("SelectedTrees", testSelectedTrees)
	suite.Run(t)
}
