package account_mocks

import (
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/stretchr/testify/mock"
)

type MockRepository struct {
	mock.Mock
}

func (x *MockRepository) Get() ([]*account.Account, error) {
	args := x.Called()
	var r0 []*account.Account
	r1 := args.Error(1)
	if r1 != nil {
		return nil, r1
	}
	if acc, ok := args.Get(0).([]*account.Account); ok {
		r0 = acc
	}
	return r0, r1
}
func (x *MockRepository) GetById(id string) (*account.Account, error) {
	args := x.Called(id)
	var r0 *account.Account
	r1 := args.Error(1)
	if r1 != nil {
		return nil, r1
	}
	if acc, ok := args.Get(0).(*account.Account); ok {
		r0 = acc
	}
	return r0, r1
}
func (x *MockRepository) CountId(id string) (int, error) {
	args := x.Called(id)
	return args.Int(0), args.Error(1)
}
func (x *MockRepository) GetBySlug(slug string) (*account.Account, error) {
	args := x.Called(slug)
	var r0 *account.Account
	r1 := args.Error(1)
	if r1 != nil {
		return nil, r1
	}
	if acc, ok := args.Get(0).(*account.Account); ok {
		r0 = acc
	}
	return r0, r1
}
func (x *MockRepository) GetByNicknameWithoutId(nickname string, id string) (*account.Account, error) {
	args := x.Called(nickname, id)
	var r0 *account.Account
	r1 := args.Error(1)
	if r1 != nil {
		return nil, r1
	}
	if acc, ok := args.Get(0).(*account.Account); ok {
		r0 = acc
	}
	return r0, r1
}
func (x *MockRepository) GetBySlugWithoutId(slug string, id string) (*account.Account, error) {
	args := x.Called(slug, id)
	var r0 *account.Account
	r1 := args.Error(1)
	if r1 != nil {
		return nil, r1
	}
	if acc, ok := args.Get(0).(*account.Account); ok {
		r0 = acc
	}
	return r0, r1
}
func (x *MockRepository) Create(a *account.Account) (*account.Account, error) {
	args := x.Called(a)
	r0 := a
	if acc, ok := args.Get(0).(*account.Account); ok {
		r0 = acc
	}
	r1 := args.Error(1)
	if r1 != nil {
		r0 = nil
	}
	return r0, r1
}
func (x *MockRepository) Update(a *account.Account) (*account.Account, error) {
	args := x.Called(a)
	r0 := a
	if acc, ok := args.Get(0).(*account.Account); ok {
		r0 = acc
	}
	r1 := args.Error(1)
	if r1 != nil {
		r0 = nil
	}
	return r0, r1
}
