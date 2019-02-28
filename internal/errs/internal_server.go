package errs

import "net/http"

type InternalServerError struct {
	message string
}

func (e InternalServerError) Error() string {
	return e.message
}

func (e InternalServerError) Code() int {
	return http.StatusInternalServerError
}

func InternalServer(message string) InternalServerError {
	return InternalServerError{
		message: message,
	}
}
