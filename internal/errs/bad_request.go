package errs

import (
	"net/http"
)

type BadRequestError struct {
	message string
}

func (e BadRequestError) Error() string {
	return e.message
}

func (e BadRequestError) Code() int {
	return http.StatusBadRequest
}

func BadRequest(message string) BadRequestError {
	return BadRequestError{
		message: message,
	}
}
