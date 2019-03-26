package errs

import (
	"errors"
	"github.com/stretchr/testify/assert"
	"net/http"
	"testing"
)

func TestNotFound(t *testing.T) {
	a := assert.New(t)
	err := errors.New("this is a failure")
	customErr := NotFound(err.Error())
	a.Equal(err.Error(), customErr.Error())
	a.Equal(http.StatusNotFound, customErr.Code())
}
