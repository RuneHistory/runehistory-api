package errs

import (
	"errors"
	"net/http"
	"testing"
)

func TestInternalServer(t *testing.T) {
	err := errors.New("this is a failure")
	customErr := InternalServer(err.Error())
	if err.Error() != customErr.Error() {
		t.Errorf("Error was incorrect, got: %s, want: %s", customErr.Error(), err.Error())
	}
	if customErr.Code() != http.StatusInternalServerError {
		t.Errorf("HTTP code was incorrect, got: %d, want: %d", customErr.Code(), http.StatusInternalServerError)
	}
}
