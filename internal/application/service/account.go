package service

import "github.com/runehistory/runehistory-api/internal/domain/account"

type Account interface {
	Get(id string) (*account.Account, error)
}

type AccountService struct {
	AccountRepo account.Repository
}

func (s *AccountService) Get(id string) (*account.Account, error) {
	return s.AccountRepo.Get(id)
}
