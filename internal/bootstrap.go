package internal

import (
	"database/sql"
	"github.com/go-chi/chi"
	"github.com/runehistory/runehistory-api/internal/application/handler"
	"github.com/runehistory/runehistory-api/internal/application/service"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/runehistory/runehistory-api/internal/repository/mysql"
)

func Init(r chi.Router, db *sql.DB) {
	var accountRepo account.Repository = &mysql.AccountMySQL{
		DB: db,
	}
	var accountService service.Account = &service.AccountService{AccountRepo: accountRepo}
	handlers := []handler.Handler{
		&handler.HelloWorld{
			AccountService: accountService,
		},
	}

	for _, h := range handlers {
		h.BindHTTP(r)
	}
}
