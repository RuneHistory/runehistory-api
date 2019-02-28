package errs

import (
	"errors"
	"net/http"
	"testing"
)

func TestNotFound(t *testing.T) {
	err := errors.New("this is a failure")
	customErr := NotFound(err.Error())
	if err.Error() != customErr.Error() {
		t.Errorf("Error was incorrect, got: %s, want: %s", customErr.Error(), err.Error())
	}
	if customErr.Code() != http.StatusNotFound {
		t.Errorf("HTTP code was incorrect, got: %d, want: %d", customErr.Code(), http.StatusNotFound)
	}
}
