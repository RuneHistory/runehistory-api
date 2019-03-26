package errs

import (
	"errors"
	"github.com/stretchr/testify/assert"
	"net/http"
	"testing"
)

func TestInternalServer(t *testing.T) {
	a := assert.New(t)
	err := errors.New("this is a failure")
	customErr := InternalServer(err.Error())
	a.Equal(err.Error(), customErr.Error())
	a.Equal(http.StatusInternalServerError, customErr.Code())
}
