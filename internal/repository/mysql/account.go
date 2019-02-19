package mysql

import (
	"database/sql"
	"github.com/runehistory/runehistory-api/internal/domain/account"
)

type AccountMySQL struct {
	DB *sql.DB
}

func (x *AccountMySQL) Get(id string) (*account.Account, error) {
	return &account.Account{
		ID:       id,
		Nickname: "Jim",
		Slug:     "jim",
	}, nil
}
