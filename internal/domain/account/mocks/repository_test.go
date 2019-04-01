package account_mocks

import (
	"errors"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestMockRepository_Get_ValidTypes(t *testing.T) {
	a := assert.New(t)
	tests := []struct {
		ExpectAccs []*account.Account
		ExpectErr  error
	}{
		{
			[]*account.Account{
				{
					ID: "test-1",
				},
			},
			nil,
		},
		{
			[]*account.Account{
				{
					ID: "test-2",
				},
			},
			nil,
		},
		{
			nil,
			errors.New("expect failure"),
		},
	}

	for _, test := range tests {
		m := new(MockRepository)
		m.On("Get").Return(test.ExpectAccs, test.ExpectErr)
		actualAccs, actualErr := m.Get()
		a.Equal(test.ExpectAccs, actualAccs)
		a.Equal(test.ExpectErr, actualErr)
	}
}

func TestMockRepository_Get_InvalidReturnType(t *testing.T) {
	a := assert.New(t)
	retVal := []account.Account{
		{
			ID: "should-fail",
		},
	}
	var expectedAccs []*account.Account
	m := new(MockRepository)
	m.On("Get").Return(retVal, nil)
	actualAccs, actualErr := m.Get()
	a.Equal(expectedAccs, actualAccs)
	a.Nil(actualErr)
}

func TestMockRepository_GetById(t *testing.T) {
	a := assert.New(t)
	tests := []struct {
		InId      string
		ExpectAcc *account.Account
		ExpectErr error
	}{
		{
			"test-1",
			&account.Account{
				ID: "test-1",
			},
			nil,
		},
		{
			"test-2",
			nil,
			errors.New("expect fail"),
		},
	}

	for _, test := range tests {
		m := new(MockRepository)
		m.On("GetById", test.InId).Return(test.ExpectAcc, test.ExpectErr)
		actualAcc, actualErr := m.GetById(test.InId)
		a.Equal(test.ExpectAcc, actualAcc)
		a.Equal(test.ExpectErr, actualErr)
	}
}

func TestMockRepository_GetById_InvalidReturnType(t *testing.T) {
	a := assert.New(t)
	retVal := account.Account{
		ID: "should-fail",
	}
	var expectedAcc *account.Account
	m := new(MockRepository)
	m.On("GetById", "should-fail").Return(retVal, nil)
	actualAcc, actualErr := m.GetById("should-fail")
	a.Equal(expectedAcc, actualAcc)
	a.Nil(actualErr)
}

func TestMockRepository_CountId(t *testing.T) {
	a := assert.New(t)
	tests := []struct {
		InId        string
		ExpectCount int
		ExpectErr   error
	}{
		{
			"test-1",
			123,
			nil,
		},
		{
			"test-2",
			0,
			errors.New("expect fail"),
		},
	}

	for _, test := range tests {
		m := new(MockRepository)
		m.On("CountId", test.InId).Return(test.ExpectCount, test.ExpectErr)
		actualCount, actualErr := m.CountId(test.InId)
		a.Equal(test.ExpectCount, actualCount)
		a.Equal(test.ExpectErr, actualErr)
	}
}

func TestMockRepository_GetBySlug(t *testing.T) {
	a := assert.New(t)
	tests := []struct {
		InSlug    string
		ExpectAcc *account.Account
		ExpectErr error
	}{
		{
			"test-1",
			&account.Account{
				Slug: "test-1",
			},
			nil,
		},
		{
			"test-2",
			nil,
			errors.New("expect fail"),
		},
	}

	for _, test := range tests {
		m := new(MockRepository)
		m.On("GetBySlug", test.InSlug).Return(test.ExpectAcc, test.ExpectErr)
		actualAcc, actualErr := m.GetBySlug(test.InSlug)
		a.Equal(test.ExpectAcc, actualAcc)
		a.Equal(test.ExpectErr, actualErr)
	}
}

func TestMockRepository_GetBySlug_InvalidReturnType(t *testing.T) {
	a := assert.New(t)
	retVal := account.Account{
		Slug: "should-fail",
	}
	var expectedAcc *account.Account
	m := new(MockRepository)
	m.On("GetBySlug", "should-fail").Return(retVal, nil)
	actualAcc, actualErr := m.GetBySlug("should-fail")
	a.Equal(expectedAcc, actualAcc)
	a.Nil(actualErr)
}

func TestMockRepository_GetByNicknameWithoutId(t *testing.T) {
	a := assert.New(t)
	tests := []struct {
		InNickname string
		InID       string
		ExpectAcc  *account.Account
		ExpectErr  error
	}{
		{
			"test-1",
			"test-1",
			&account.Account{
				Nickname: "test-1",
			},
			nil,
		},
		{
			"test-2",
			"test-2",
			nil,
			errors.New("expect fail"),
		},
	}

	for _, test := range tests {
		m := new(MockRepository)
		m.On("GetByNicknameWithoutId", test.InNickname, test.InID).Return(test.ExpectAcc, test.ExpectErr)
		actualAcc, actualErr := m.GetByNicknameWithoutId(test.InNickname, test.InID)
		a.Equal(test.ExpectAcc, actualAcc)
		a.Equal(test.ExpectErr, actualErr)
	}
}

func TestMockRepository_GetByNicknameWithoutId_InvalidReturnType(t *testing.T) {
	a := assert.New(t)
	retVal := account.Account{
		Nickname: "should-fail",
		ID:       "should-fail",
	}
	var expectedAcc *account.Account
	m := new(MockRepository)
	m.On("GetByNicknameWithoutId", "should-fail", "should-fail").Return(retVal, nil)
	actualAcc, actualErr := m.GetByNicknameWithoutId("should-fail", "should-fail")
	a.Equal(expectedAcc, actualAcc)
	a.Nil(actualErr)
}

func TestMockRepository_GetBySlugWithoutId(t *testing.T) {
	a := assert.New(t)
	tests := []struct {
		InSlug    string
		InID      string
		ExpectAcc *account.Account
		ExpectErr error
	}{
		{
			"test-1",
			"test-1",
			&account.Account{
				Slug: "test-1",
			},
			nil,
		},
		{
			"test-2",
			"test-2",
			nil,
			errors.New("expect fail"),
		},
	}

	for _, test := range tests {
		m := new(MockRepository)
		m.On("GetBySlugWithoutId", test.InSlug, test.InID).Return(test.ExpectAcc, test.ExpectErr)
		actualAcc, actualErr := m.GetBySlugWithoutId(test.InSlug, test.InID)
		a.Equal(test.ExpectAcc, actualAcc)
		a.Equal(test.ExpectErr, actualErr)
	}
}

func TestMockRepository_GetBySlugWithoutId_InvalidReturnType(t *testing.T) {
	a := assert.New(t)
	retVal := account.Account{
		Slug: "should-fail",
		ID:   "should-fail",
	}
	var expectedAcc *account.Account
	m := new(MockRepository)
	m.On("GetBySlugWithoutId", "should-fail", "should-fail").Return(retVal, nil)
	actualAcc, actualErr := m.GetBySlugWithoutId("should-fail", "should-fail")
	a.Equal(expectedAcc, actualAcc)
	a.Nil(actualErr)
}

func TestMockRepository_Create(t *testing.T) {
	a := assert.New(t)
	tests := []struct {
		InAcc     *account.Account
		ExpectAcc *account.Account
		ExpectErr error
	}{
		{
			&account.Account{
				Slug: "test-1",
			},
			&account.Account{
				Slug: "test-1",
			},
			nil,
		},
		{
			nil,
			nil,
			errors.New("expect fail"),
		},
	}

	for _, test := range tests {
		m := new(MockRepository)
		m.On("Create", test.InAcc).Return(test.ExpectAcc, test.ExpectErr)
		actualAcc, actualErr := m.Create(test.InAcc)
		a.Equal(test.ExpectAcc, actualAcc)
		a.Equal(test.ExpectErr, actualErr)
	}
}

func TestMockRepository_Update(t *testing.T) {
	a := assert.New(t)
	tests := []struct {
		InAcc     *account.Account
		ExpectAcc *account.Account
		ExpectErr error
	}{
		{
			&account.Account{
				Slug: "test-1",
			},
			&account.Account{
				Slug: "test-1",
			},
			nil,
		},
		{
			nil,
			nil,
			errors.New("expect fail"),
		},
	}

	for _, test := range tests {
		m := new(MockRepository)
		m.On("Update", test.InAcc).Return(test.ExpectAcc, test.ExpectErr)
		actualAcc, actualErr := m.Update(test.InAcc)
		a.Equal(test.ExpectAcc, actualAcc)
		a.Equal(test.ExpectErr, actualErr)
	}
}
