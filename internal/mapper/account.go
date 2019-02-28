package mapper

import (
	"github.com/runehistory/runehistory-api/internal/domain/account"
)

type AccountHttpV1 struct {
	ID       string `json:"id"`
	Slug     string `json:"slug"`
	Nickname string `json:"nickname"`
}

func AccountToHttpV1(acc *account.Account) *AccountHttpV1 {
	return &AccountHttpV1{
		ID:       acc.ID,
		Slug:     acc.Slug,
		Nickname: acc.Nickname,
	}
}

func AccountFromHttpV1(acc *AccountHttpV1) *account.Account {
	return &account.Account{
		ID:       acc.ID,
		Slug:     acc.Slug,
		Nickname: acc.Nickname,
	}
}
