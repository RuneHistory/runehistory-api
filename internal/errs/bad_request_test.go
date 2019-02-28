package errs

import (
	"errors"
	"net/http"
	"testing"
)

func TestBadRequest(t *testing.T) {
	err := errors.New("this is a failure")
	customErr := BadRequest(err.Error())
	if err.Error() != customErr.Error() {
		t.Errorf("Error was incorrect, got: %s, want: %s", customErr.Error(), err.Error())
	}
	if customErr.Code() != http.StatusBadRequest {
		t.Errorf("HTTP code was incorrect, got: %d, want: %d", customErr.Code(), http.StatusBadRequest)
	}
}
