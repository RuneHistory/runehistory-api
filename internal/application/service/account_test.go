package service

import (
	"errors"
	"fmt"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	accountMocks "github.com/runehistory/runehistory-api/internal/domain/account/mocks"
	validateMocks "github.com/runehistory/runehistory-api/internal/domain/validate/mocks"
	"github.com/runehistory/runehistory-api/internal/errs"
	"github.com/satori/go.uuid"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"testing"
)

func getMocks() (Account, *accountMocks.MockRepository, *validateMocks.MockValidator) {
	repo := new(accountMocks.MockRepository)
	validator := new(validateMocks.MockValidator)
	service := NewAccountService(repo, validator)
	return service, repo, validator
}

func TestAccountService_Get_RepoReturnsMultiple(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	repo.On("Get").Return([]*account.Account{
		{
			ID: "acc-1",
		},
		{
			ID: "acc-2",
		},
	}, nil)
	accounts, err := service.Get()
	a.Nil(err)
	a.Len(accounts, 2)
	a.Equal(accounts[0].ID, "acc-1")
	a.Equal(accounts[1].ID, "acc-2")
}

func TestAccountService_Get_RepoReturnsEmpty(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	repo.On("Get").Return([]*account.Account{}, nil)
	accounts, err := service.Get()
	a.Nil(err)
	a.Len(accounts, 0)
}

func TestAccountService_Get_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	repo.On("Get").Return(nil, errors.New("expecting failure"))
	accounts, err := service.Get()
	a.Nil(accounts)
	a.NotNil(err)
	a.EqualError(err, "expecting failure")
}

func TestAccountService_GetById_RepoReturnsAccount(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	expected := &account.Account{
		ID: "test-id",
	}
	repo.On("GetById", expected.ID).Return(expected, nil)
	actual, err := service.GetById(expected.ID)
	a.Nil(err)
	a.Equal(expected.ID, actual.ID)
}

func TestAccountService_GetById_RepoReturnsNil(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	repo.On("GetById", "i-dont-exist").Return(nil, nil)
	actual, err := service.GetById("i-dont-exist")
	a.Nil(err)
	a.Nil(actual)
}

func TestAccountService_GetById_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	repo.On("GetById", "something-broke").Return(nil, errors.New("expecting failure"))
	actual, err := service.GetById("something-broke")
	a.Nil(actual)
	a.NotNil(err)
	a.EqualError(err, "expecting failure")
}

func TestAccountService_GetBySlug_RepoReturnsAccount(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	expected := &account.Account{
		Slug: "test-slug",
	}
	repo.On("GetBySlug", expected.Slug).Return(expected, nil)
	actual, err := service.GetBySlug(expected.Slug)
	a.Nil(err)
	a.Equal(expected.Slug, actual.Slug)
}

func TestAccountService_GetBySlug_RepoReturnsNil(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	repo.On("GetBySlug", "i-dont-exist").Return(nil, nil)
	actual, err := service.GetBySlug("i-dont-exist")
	a.Nil(err)
	a.Nil(actual)
}

func TestAccountService_GetBySlug_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	service, repo, _ := getMocks()
	repo.On("GetBySlug", "something-broke").Return(nil, errors.New("expecting failure"))
	actual, err := service.GetBySlug("something-broke")
	a.Nil(actual)
	a.NotNil(err)
	a.EqualError(err, "expecting failure")
}

func TestAccountService_Create_RepoReturnsAccount(t *testing.T) {
	a := assert.New(t)
	service, repo, validator := getMocks()
	accountType := fmt.Sprintf("%T", &account.Account{})
	validator.On("NewAccount", mock.AnythingOfType(accountType)).Return(nil)
	repo.On("Create", mock.AnythingOfType(accountType)).Return(nil, nil)
	actual, err := service.Create("New Account")
	a.Nil(err)
	a.Equal("New Account", actual.Nickname)
	uuidV4 := uuid.Must(uuid.FromString(actual.ID))
	a.Equal(actual.ID, uuidV4.String())
	a.Equal(actual.Slug, "new-account")
}

func TestAccountService_Create_NicknameFailsValidation(t *testing.T) {
	a := assert.New(t)
	service, _, validator := getMocks()
	accountType := fmt.Sprintf("%T", &account.Account{})
	validator.On("NewAccount", mock.AnythingOfType(accountType)).Return(errors.New("validation failed"))
	actual, err := service.Create("New Account")
	a.Nil(actual)
	a.NotNil(err)
	a.IsType(errs.BadRequestError{}, err)
	a.EqualError(err, "validation failed")
}

func TestAccountService_Create_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	service, repo, validator := getMocks()
	accountType := fmt.Sprintf("%T", &account.Account{})
	validator.On("NewAccount", mock.AnythingOfType(accountType)).Return(nil)
	repo.On("Create", mock.AnythingOfType(accountType)).Return(nil, errors.New("repo failed"))
	actual, err := service.Create("New Account")
	a.Nil(actual)
	a.NotNil(err)
	a.EqualError(err, "repo failed")
}

func TestAccountService_Update_RepoReturnsAccount(t *testing.T) {
	a := assert.New(t)
	service, repo, validator := getMocks()
	accountType := fmt.Sprintf("%T", &account.Account{})

	expected := &account.Account{
		ID:       "account-to-update",
		Nickname: "New Nickname",
		Slug:     "new-slug",
	}

	validator.On("UpdateAccount", mock.AnythingOfType(accountType)).Return(nil)
	repo.On("Update", mock.AnythingOfType(accountType)).Return(nil, nil)
	actual, err := service.Update(expected)
	a.Nil(err)
	a.Equal(expected.ID, actual.ID)
	a.Equal(expected.Nickname, actual.Nickname)
	a.Equal(expected.Slug, actual.Slug)
}

func TestAccountService_Update_FailsValidation(t *testing.T) {
	a := assert.New(t)
	service, _, validator := getMocks()
	accountType := fmt.Sprintf("%T", &account.Account{})

	expected := &account.Account{
		ID:       "account-to-update",
		Nickname: "New Nickname",
		Slug:     "new-slug",
	}

	validator.On("UpdateAccount", mock.AnythingOfType(accountType)).Return(errors.New("validation failed"))
	actual, err := service.Update(expected)
	a.Nil(actual)
	a.NotNil(err)
	a.IsType(errs.BadRequestError{}, err)
	a.EqualError(err, "validation failed")
}

func TestAccountService_Update_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	service, repo, validator := getMocks()
	accountType := fmt.Sprintf("%T", &account.Account{})
	expected := &account.Account{
		ID:       "account-to-update",
		Nickname: "New Nickname",
		Slug:     "new-slug",
	}

	validator.On("UpdateAccount", mock.AnythingOfType(accountType)).Return(nil)
	repo.On("Update", mock.AnythingOfType(accountType)).Return(nil, errors.New("repo failed"))
	actual, err := service.Update(expected)
	a.Nil(actual)
	a.NotNil(err)
	a.EqualError(err, "repo failed")
}

func TestAccountService_Update_SlugIsUpdatedWithNickname(t *testing.T) {
	a := assert.New(t)
	service, repo, validator := getMocks()
	accountType := fmt.Sprintf("%T", &account.Account{})

	expected := &account.Account{
		ID:       "account-to-update",
		Nickname: "Current Nickname",
		Slug:     "current-slug",
	}
	expected.Nickname = "New Nickname"

	validator.On("UpdateAccount", mock.AnythingOfType(accountType)).Return(nil)
	repo.On("Update", mock.AnythingOfType(accountType)).Return(nil, nil)
	actual, err := service.Update(expected)
	a.Nil(err)
	a.Equal(expected.ID, actual.ID)
	a.Equal(expected.Nickname, actual.Nickname)
	a.Equal("new-nickname", actual.Slug)
}
