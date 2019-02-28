package handler

import (
	"github.com/go-chi/chi"
	"github.com/runehistory/runehistory-api/internal/application/service"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/runehistory/runehistory-api/internal/mapper"
	"github.com/runehistory/runehistory-api/internal/transport/http_transport"
	"net/http"
)

type GetAccounts struct {
	AccountService service.Account
}

type GetAccountsRequest struct {
}

type GetAccountsResponse struct {
	Accounts []*account.Account
}

func (h *GetAccounts) BindHTTP(r chi.Router) {
	r.Group(func(r chi.Router) {
		r.Get("/v1/accounts", h.HandleHTTP)
	})
}

func (h *GetAccounts) HandleHTTP(w http.ResponseWriter, r *http.Request) {
	req := &GetAccountsRequest{}
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

	mapped := make([]*mapper.AccountHttpV1, len(res.Accounts))
	for k, acc := range res.Accounts {
		mapped[k] = mapper.AccountToHttpV1(acc)
	}

	http_transport.SendJson(mapped, w)
}

func (h *GetAccounts) handle(r *GetAccountsRequest) (*GetAccountsResponse, error) {
	accounts, err := h.AccountService.Get()
	if err != nil {
		return nil, err
	}
	return &GetAccountsResponse{
		Accounts: accounts,
	}, nil
}
