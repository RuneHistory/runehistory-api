package errs

import "net/http"

type NotFoundError struct {
	message string
}

func (e NotFoundError) Error() string {
	return e.message
}

func (e NotFoundError) Code() int {
	return http.StatusNotFound
}

func NotFound(message string) NotFoundError {
	return NotFoundError{
		message: message,
	}
}
