package validate

import (
	"errors"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/stretchr/testify/assert"
	"testing"
)

func getMockAccountRules() (*account.MockRepository, AccountRules) {
	repo := new(account.MockRepository)
	rules := NewAccountRules(repo)
	return repo, rules
}

func TestStdAccountRules_IDIsPresent(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "present-id",
	}
	err := rules.IDIsPresent(acc)
	a.Nil(err, "not expecting err for present ID")

	acc = &account.Account{
		ID: "",
	}
	err = rules.IDIsPresent(acc)
	a.NotNil(err, "expecting error for vacant ID")
}

func TestStdAccountRules_IDIsCorrectLength(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "uuid-correct-length-1234567890123456",
	}
	err := rules.IDIsCorrectLength(acc)
	a.Nilf(err, "id with length %d should be valid", len(acc.ID))

	acc = &account.Account{
		ID: "uuid-incorrect-length",
	}
	err = rules.IDIsCorrectLength(acc)
	a.NotNilf(err, "id with length %d should be invalid", len(acc.ID))
}

func TestStdAccountRules_IDIsUnique(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "unique-id",
	}
	repo.On("CountId", acc.ID).Return(1, nil).Once()
	err := rules.IDIsUnique(acc)
	a.Nil(err, "expecting ID to be unique", acc.ID)
	repo.AssertExpectations(t)

	acc.ID = "non-unique-id"
	repo.On("CountId", acc.ID).Return(2, nil).Once()
	err = rules.IDIsUnique(acc)
	a.NotNil(err, "expecting duplicate ID", acc.ID)
	repo.AssertExpectations(t)

	acc.ID = "id-is-unique-err"
	repo.On("CountId", acc.ID).Return(0, errors.New("expecting failure")).Once()
	err = rules.IDIsUnique(acc)
	a.NotNil(err, "expecting error")
	a.EqualError(err, "expecting failure")
	repo.AssertExpectations(t)
}

func TestStdAccountRules_IDWillBeUnique(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "will-be-unique-id",
	}
	repo.On("CountId", acc.ID).Return(0, nil).Once()
	err := rules.IDWillBeUnique(acc)
	a.Nil(err, "expecting id to be unique")
	repo.AssertExpectations(t)

	acc.ID = "non-unique-id"
	repo.On("CountId", acc.ID).Return(1, nil).Once()
	err = rules.IDWillBeUnique(acc)
	a.NotNilf(err, "expecting duplicate id: %s", acc.ID)
	repo.AssertExpectations(t)

	acc.ID = "id-is-unique-err"
	repo.On("CountId", acc.ID).Return(0, errors.New("expecting failure")).Once()
	err = rules.IDWillBeUnique(acc)
	a.NotNil(err, "expecting error")
	a.EqualError(err, "expecting failure")
	repo.AssertExpectations(t)
}

func TestStdAccountRules_NicknameIsPresent(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Nickname: "nickname-is-present",
	}
	err := rules.NicknameIsPresent(acc)
	a.Nilf(err, "expecting nickname to be present: %v", err)

	acc.Nickname = ""
	err = rules.NicknameIsPresent(acc)
	a.NotNil(err, "expecting error")
	a.EqualError(err, "nickname is blank")
}

func TestStdAccountRules_NicknameIsNotTooLong(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Nickname: "iFitInMaxLen",
	}
	err := rules.NicknameIsNotTooLong(acc)
	a.Nilf(err, "expecting nickname to be valid: %v", err)

	acc.Nickname = "iAmWayTooLong"
	err = rules.NicknameIsNotTooLong(acc)
	a.NotNil(err, "expecting error")
	a.EqualError(err, "nickname must be no longer than 12 characters")
}

func TestStdAccountRules_NicknameIsUniqueToID(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID:       "will-be-unique-id",
		Nickname: "My Nickname",
	}
	repo.On("GetByNicknameWithoutId", acc.Nickname, acc.ID).Return(nil, nil).Once()
	err := rules.NicknameIsUniqueToID(acc)
	a.Nil(err, "expecting nickname to be unique to id")
	repo.AssertExpectations(t)

	acc.ID = "non-unique-id"
	repo.On("GetByNicknameWithoutId", acc.Nickname, acc.ID).Return(&account.Account{}, nil).Once()
	err = rules.NicknameIsUniqueToID(acc)
	a.NotNilf(err, "expecting duplicate nickname: %s", acc.Nickname)
	a.EqualError(err, "nickname My Nickname already exists")
	repo.AssertExpectations(t)

	acc.ID = "id-err"
	repo.On("GetByNicknameWithoutId", acc.Nickname, acc.ID).Return(nil, errors.New("expecting failure")).Once()
	err = rules.NicknameIsUniqueToID(acc)
	a.NotNil(err, "expecting error")
	a.EqualError(err, "expecting failure")
	repo.AssertExpectations(t)
}

func TestStdAccountRules_SlugIsPresent(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Slug: "slug-is-present",
	}
	err := rules.SlugIsPresent(acc)
	a.Nilf(err, "expecting slug to be present: %v", err)

	acc.Slug = ""
	err = rules.SlugIsPresent(acc)
	a.NotNil(err, "expecting error")
	a.EqualError(err, "slug is blank")
}

func TestStdAccountRules_SlugIsNotTooLong(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Slug: "iFitInMaxLen",
	}
	err := rules.SlugIsNotTooLong(acc)
	a.Nilf(err, "expecting slug to be valid: %v", err)

	acc.Slug = "iAmWayTooLong"
	err = rules.SlugIsNotTooLong(acc)
	a.NotNil(err, "expecting error")
	a.EqualError(err, "slug must be no longer than 12 characters")
}

func TestStdAccountRules_SlugIsUniqueToID(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID:   "will-be-unique-id",
		Slug: "my-slug",
	}
	repo.On("GetBySlugWithoutId", acc.Slug, acc.ID).Return(nil, nil).Once()
	err := rules.SlugIsUniqueToID(acc)
	a.Nil(err, "expecting slug to be unique to id")
	repo.AssertExpectations(t)

	acc.ID = "non-unique-id"
	repo.On("GetBySlugWithoutId", acc.Slug, acc.ID).Return(&account.Account{}, nil).Once()
	err = rules.SlugIsUniqueToID(acc)
	a.NotNilf(err, "expecting duplicate slug: %s", acc.Slug)
	a.EqualError(err, "slug my-slug already exists")
	repo.AssertExpectations(t)

	acc.ID = "id-err"
	repo.On("GetBySlugWithoutId", acc.Slug, acc.ID).Return(nil, errors.New("expecting failure")).Once()
	err = rules.SlugIsUniqueToID(acc)
	a.NotNil(err, "expecting error")
	a.EqualError(err, "expecting failure")
	repo.AssertExpectations(t)
}
