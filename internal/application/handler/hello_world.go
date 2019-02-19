package handler

import (
	"fmt"
	"github.com/go-chi/chi"
	"github.com/runehistory/runehistory-api/internal/application/service"
	"net/http"
)

type HelloWorld struct {
	AccountService service.Account
}

func (h *HelloWorld) BindHTTP(r chi.Router) {
	r.Get("/hello", h.HandleHTTP)
}

func (h *HelloWorld) HandleHTTP(w http.ResponseWriter, r *http.Request) {
	account, err := h.AccountService.Get("some-uuid")
	if err != nil {
		panic(err)
	}
	fmt.Println(account)
	_, err = w.Write([]byte("hello"))
	_, err = w.Write([]byte(account.Nickname))
	if err != nil {
		panic(err)
	}
}
