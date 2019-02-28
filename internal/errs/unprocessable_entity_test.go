package errs

import (
	"errors"
	"net/http"
	"testing"
)

func TestUnprocessableEntity(t *testing.T) {
	err := errors.New("this is a failure")
	customErr := UnprocessableEntity(err.Error())
	if err.Error() != customErr.Error() {
		t.Errorf("Error was incorrect, got: %s, want: %s", customErr.Error(), err.Error())
	}
	if customErr.Code() != http.StatusUnprocessableEntity {
		t.Errorf("HTTP code was incorrect, got: %d, want: %d", customErr.Code(), http.StatusUnprocessableEntity)
	}
}
