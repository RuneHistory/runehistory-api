package errs

import "net/http"

type UnprocessableEntityError struct {
	message string
}

func (e UnprocessableEntityError) Error() string {
	return e.message
}

func (e UnprocessableEntityError) Code() int {
	return http.StatusUnprocessableEntity
}

func UnprocessableEntity(message string) UnprocessableEntityError {
	return UnprocessableEntityError{
		message: message,
	}
}
