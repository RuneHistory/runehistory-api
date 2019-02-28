package service

import (
	"github.com/mozillazg/go-slugify"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/runehistory/runehistory-api/internal/domain/validate"
	"github.com/runehistory/runehistory-api/internal/errs"
	"github.com/satori/go.uuid"
)

type Account interface {
	Get() ([]*account.Account, error)
	GetById(id string) (*account.Account, error)
	GetBySlug(id string) (*account.Account, error)
	Create(nickname string) (*account.Account, error)
	Update(account *account.Account) (*account.Account, error)
}

type AccountService struct {
	AccountRepo account.Repository
	Validator   validate.Validator
}

func (s *AccountService) Get() ([]*account.Account, error) {
	return s.AccountRepo.Get()
}

func (s *AccountService) GetById(id string) (*account.Account, error) {
	return s.AccountRepo.GetById(id)
}

func (s *AccountService) GetBySlug(slug string) (*account.Account, error) {
	return s.AccountRepo.GetBySlug(slug)
}

func (s *AccountService) Create(nickname string) (*account.Account, error) {
	id := uuid.NewV4().String()
	slug := slugify.Slugify(nickname)
	a := account.NewAccount(id, nickname, slug)
	if err := s.Validator.NewAccount(a); err != nil {
		return nil, errs.BadRequest(err.Error())
	}
	return s.AccountRepo.Create(a)
}

func (s *AccountService) Update(acc *account.Account) (*account.Account, error) {
	acc.Slug = slugify.Slugify(acc.Nickname)
	if err := s.Validator.UpdateAccount(acc); err != nil {
		return nil, errs.BadRequest(err.Error())
	}
	return s.AccountRepo.Update(acc)
}
