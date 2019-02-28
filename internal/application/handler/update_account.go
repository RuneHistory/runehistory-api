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

type UpdateAccount struct {
	AccountService service.Account
}

type UpdateAccountRequest struct {
	Account mapper.AccountHttpV1
	Slug    string `uriattr:"accountSlug"`
}

type UpdateAccountResponse struct {
	Account *account.Account
}

func (h *UpdateAccount) BindHTTP(r chi.Router) {
	r.Group(func(r chi.Router) {
		r.Put("/v1/accounts/{accountSlug}", h.HandleHTTP)
	})
}

func (h *UpdateAccount) HandleHTTP(w http.ResponseWriter, r *http.Request) {
	req := &UpdateAccountRequest{}
	err := http_transport.ParseRequestURL(r, req)
	if err != nil {
		http_transport.SendError(err, w)
		return
	}
	err = http_transport.ParseRequestJSON(r, &req.Account)
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

func (h *UpdateAccount) handle(r *UpdateAccountRequest) (*UpdateAccountResponse, error) {
	existingAccount, err := h.AccountService.GetBySlug(r.Slug)
	if err != nil {
		return nil, err
	}
	if existingAccount == nil {
		return nil, errs.NotFound(fmt.Sprintf("Account %s not found", r.Slug))
	}

	updatedAccount := mapper.AccountFromHttpV1(&r.Account) // map this from r.Account
	updatedAccount.ID = existingAccount.ID
	updatedAccount.Slug = existingAccount.Slug

	acc, err := h.AccountService.Update(updatedAccount)
	if err != nil {
		return nil, err
	}
	return &UpdateAccountResponse{
		Account: acc,
	}, nil
}
