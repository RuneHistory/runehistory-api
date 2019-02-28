package mysql

import (
	"database/sql"
	"github.com/runehistory/runehistory-api/internal/domain/account"
)

type AccountMySQL struct {
	DB *sql.DB
}

func (r *AccountMySQL) Get() ([]*account.Account, error) {
	var accounts []*account.Account
	results, err := r.DB.Query("SELECT id, nickname, slug FROM account")
	if err == sql.ErrNoRows {
		return accounts, nil
	}
	for results.Next() {
		var a account.Account
		err = results.Scan(&a.ID, &a.Nickname, &a.Slug)
		if err != nil {
			return nil, err
		}
		accounts = append(accounts, &a)
	}
	return accounts, nil
}

func (r *AccountMySQL) GetById(id string) (*account.Account, error) {
	var a account.Account
	err := r.DB.QueryRow("SELECT id, nickname, slug FROM account where id = ?", id).Scan(&a.ID, &a.Nickname, &a.Slug)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &a, nil
}

func (r *AccountMySQL) CountId(id string) (int, error) {
	var count int
	err := r.DB.QueryRow("SELECT COUNT(id) FROM account where id = ?", id).Scan(&count)

	if err == sql.ErrNoRows {
		return 0, nil
	}
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (r *AccountMySQL) GetBySlug(slug string) (*account.Account, error) {
	var a account.Account
	err := r.DB.QueryRow("SELECT id, nickname, slug FROM account where slug = ?", slug).Scan(&a.ID, &a.Nickname, &a.Slug)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &a, nil
}

func (r *AccountMySQL) Create(a *account.Account) (*account.Account, error) {
	_, err := r.DB.Exec("INSERT INTO account (id, nickname, slug) VALUES (?, ?, ?)", a.ID, a.Nickname, a.Slug)
	if err != nil {
		return nil, err
	}
	return a, nil
}

func (r *AccountMySQL) Update(a *account.Account) (*account.Account, error) {
	_, err := r.DB.Exec("UPDATE account SET nickname = ?, slug = ? WHERE id = ?", a.Nickname, a.Slug, a.ID)
	if err != nil {
		return nil, err
	}
	return a, nil
}

func (r *AccountMySQL) GetByNicknameWithoutId(nickname string, id string) (*account.Account, error) {
	var a account.Account
	err := r.DB.QueryRow("SELECT id, nickname, slug FROM account where slug = ? and id != ?", nickname, id).Scan(&a.ID, &a.Nickname, &a.Slug)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &a, nil
}

func (r *AccountMySQL) GetBySlugWithoutId(slug string, id string) (*account.Account, error) {
	var a account.Account
	err := r.DB.QueryRow("SELECT id, nickname, slug FROM account where slug = ? and id != ?", slug, id).Scan(&a.ID, &a.Nickname, &a.Slug)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &a, nil
}
