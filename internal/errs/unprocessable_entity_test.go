package errs

import (
	"errors"
	"github.com/stretchr/testify/assert"
	"net/http"
	"testing"
)

func TestUnprocessableEntity(t *testing.T) {
	a := assert.New(t)
	err := errors.New("this is a failure")
	customErr := UnprocessableEntity(err.Error())
	a.Equal(err.Error(), customErr.Error())
	a.Equal(http.StatusUnprocessableEntity, customErr.Code())
}
