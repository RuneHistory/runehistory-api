package errs

import (
	"errors"
	"github.com/stretchr/testify/assert"
	"net/http"
	"testing"
)

func TestBadRequest(t *testing.T) {
	a := assert.New(t)
	err := errors.New("this is a failure")
	customErr := BadRequest(err.Error())
	a.Equal(err.Error(), customErr.Error())
	a.Equal(http.StatusBadRequest, customErr.Code())
}
