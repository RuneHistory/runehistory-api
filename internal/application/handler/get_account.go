package handler

import (
	"fmt"
	"github.com/go-chi/chi"
	"github.com/runehistory/runehistory-api/internal/application/service"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/runehistory/runehistory-api/internal/errs"
	"github.com/runehistory/runehistory-api/internal/mapper"
	"github.com/runehistory/runehistory-api/internal/transport/http_transport"
	"net/http"
)

type GetAccount struct {
	AccountService service.Account
}

type GetAccountRequest struct {
	Slug string `uriattr:"accountSlug"`
}

type GetAccountResponse struct {
	Account *account.Account
}

func (h *GetAccount) BindHTTP(r chi.Router) {
	r.Group(func(r chi.Router) {
		r.Get(fmt.Sprintf("/v1/accounts/{%s}", "accountSlug"), h.HandleHTTP)
	})
}

func (h *GetAccount) HandleHTTP(w http.ResponseWriter, r *http.Request) {
	req := &GetAccountRequest{}
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

func (h *GetAccount) handle(r *GetAccountRequest) (*GetAccountResponse, error) {
	acc, err := h.AccountService.GetBySlug(r.Slug)
	if err != nil {
		return nil, err
	}
	if acc == nil {
		return nil, errs.NotFound(fmt.Sprintf("Account %s not found", r.Slug))
	}
	return &GetAccountResponse{
		Account: acc,
	}, nil
}
