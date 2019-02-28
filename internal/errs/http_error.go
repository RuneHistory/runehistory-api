package errs

type HttpError interface {
	Error() string
	Code() int
}
