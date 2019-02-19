package handler

import "github.com/go-chi/chi"

type Handler interface {
	BindHTTP(r chi.Router)
}
