package account

import (
	"github.com/stretchr/testify/mock"
)

type MockRepository struct {
	mock.Mock
}

func (x *MockRepository) Get() ([]*Account, error) {
	args := x.Called()
	var r0 []*Account
	if acc, ok := args.Get(0).([]*Account); ok {
		r0 = acc
	}
	return r0, args.Error(1)
}
func (x *MockRepository) GetById(id string) (*Account, error) {
	args := x.Called(id)
	var r0 *Account
	if acc, ok := args.Get(0).(*Account); ok {
		r0 = acc
	}
	return r0, args.Error(1)
}
func (x *MockRepository) CountId(id string) (int, error) {
	args := x.Called(id)
	return args.Int(0), args.Error(1)
}
func (x *MockRepository) GetBySlug(slug string) (*Account, error) {
	args := x.Called(slug)
	var r0 *Account
	if acc, ok := args.Get(0).(*Account); ok {
		r0 = acc
	}
	return r0, args.Error(1)
}
func (x *MockRepository) GetByNicknameWithoutId(nickname string, id string) (*Account, error) {
	args := x.Called(nickname, id)
	var r0 *Account
	if acc, ok := args.Get(0).(*Account); ok {
		r0 = acc
	}
	return r0, args.Error(1)
}
func (x *MockRepository) GetBySlugWithoutId(slug string, id string) (*Account, error) {
	args := x.Called(slug, id)
	var r0 *Account
	if acc, ok := args.Get(0).(*Account); ok {
		r0 = acc
	}
	return r0, args.Error(1)
}
func (x *MockRepository) Create(a *Account) (*Account, error) {
	args := x.Called(a)
	var r0 *Account
	if acc, ok := args.Get(0).(*Account); ok {
		r0 = acc
	}
	return r0, args.Error(1)
}
func (x *MockRepository) Update(a *Account) (*Account, error) {
	args := x.Called(a)
	var r0 *Account
	if acc, ok := args.Get(0).(*Account); ok {
		r0 = acc
	}
	return r0, args.Error(1)
}
