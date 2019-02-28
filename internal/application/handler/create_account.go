package handler

import (
	"github.com/go-chi/chi"
	"github.com/runehistory/runehistory-api/internal/application/service"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/runehistory/runehistory-api/internal/mapper"
	"github.com/runehistory/runehistory-api/internal/transport/http_transport"
	"net/http"
)

type CreateAccount struct {
	AccountService service.Account
}

type CreateAccountRequest struct {
	Nickname string `json:"nickname"`
}

type CreateAccountResponse struct {
	Account *account.Account
}

func (h *CreateAccount) BindHTTP(r chi.Router) {
	r.Group(func(r chi.Router) {
		r.Post("/v1/accounts", h.HandleHTTP)
	})
}

func (h *CreateAccount) HandleHTTP(w http.ResponseWriter, r *http.Request) {
	req := &CreateAccountRequest{}
	err := http_transport.ParseRequest(r, req)
	if err != nil {
		http_transport.SendError(err, w)
		return
	}

	res, err := h.handle(req)
	if err != nil {
		http_transport.SendError(err, w)
		return
	}

	mapped := mapper.AccountToHttpV1(res.Account)

	http_transport.SendJson(mapped, w)
}

func (h *CreateAccount) handle(r *CreateAccountRequest) (*CreateAccountResponse, error) {
	acc, err := h.AccountService.Create(r.Nickname)
	if err != nil {
		return nil, err
	}
	return &CreateAccountResponse{
		Account: acc,
	}, nil
}
