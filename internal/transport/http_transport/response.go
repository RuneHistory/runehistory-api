package http_transport

import "C"
import (
	"encoding/json"
	"github.com/runehistory/runehistory-api/internal/errs"
	"net/http"
)

type Response interface {
}

type errorResponse struct {
	Message string `json:"error"`
}

func SendJson(response Response, w http.ResponseWriter) {
	encoded, err := json.Marshal(response)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(encoded)
}

func SendError(errResponse error, w http.ResponseWriter) {
	e := errorResponse{
		Message: errResponse.Error(),
	}

	encoded, err := json.Marshal(e)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(getErrorCode(errResponse))
	_, _ = w.Write(encoded)
}

func getErrorCode(err error) int {
	switch errResponse := err.(type) {
	case errs.HttpError:
		return errResponse.Code()
	default:
		return http.StatusInternalServerError
	}
}
