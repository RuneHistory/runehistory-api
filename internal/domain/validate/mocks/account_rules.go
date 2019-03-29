package mocks

import (
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/stretchr/testify/mock"
)

type MockValidator struct {
	mock.Mock
}

func (x *MockValidator) NewAccount(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockValidator) UpdateAccount(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}

type MockAccountRules struct {
	mock.Mock
}

func (x *MockAccountRules) IDIsPresent(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) IDIsCorrectLength(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) IDWillBeUnique(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) IDIsUnique(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) NicknameIsPresent(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) NicknameIsNotTooLong(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) NicknameIsUniqueToID(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) SlugIsPresent(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) SlugIsNotTooLong(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
func (x *MockAccountRules) SlugIsUniqueToID(a *account.Account) error {
	args := x.Called(a)
	return args.Error(0)
}
