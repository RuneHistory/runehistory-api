package validate

import (
	"errors"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	accountMocks "github.com/runehistory/runehistory-api/internal/domain/account/mocks"
	"github.com/stretchr/testify/assert"
	"testing"
)

func getMockAccountRules() (*accountMocks.MockRepository, AccountRules) {
	repo := new(accountMocks.MockRepository)
	rules := NewAccountRules(repo)
	return repo, rules
}

func TestStdAccountRules_IDIsPresent_PresentID(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "present-id",
	}
	err := rules.IDIsPresent(acc)
	a.Nil(err)
}

func TestStdAccountRules_IDIsPresent_EmptyID(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "",
	}
	err := rules.IDIsPresent(acc)
	a.NotNil(err)
}

func TestStdAccountRules_IDIsCorrectLength_IsCorrectLength(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "uuid-correct-length-1234567890123456",
	}
	err := rules.IDIsCorrectLength(acc)
	a.Nil(err)
}

func TestStdAccountRules_IDIsCorrectLength_TooShort(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "uuid-too-short",
	}
	err := rules.IDIsCorrectLength(acc)
	a.NotNil(err)
}

func TestStdAccountRules_IDIsCorrectLength_TooLong(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "uuid-too-long-uuid-too-long-uuid-too-long-",
	}
	err := rules.IDIsCorrectLength(acc)
	a.NotNil(err)
}

func TestStdAccountRules_IDIsUnique_IDIsUnique(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "unique-id",
	}
	repo.On("CountId", acc.ID).Return(1, nil).Once()
	err := rules.IDIsUnique(acc)
	a.Nil(err)
	repo.AssertExpectations(t)
}

func TestStdAccountRules_IDIsUnique_IDIsDuplicate(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "non-unique-id",
	}
	repo.On("CountId", acc.ID).Return(2, nil).Once()
	err := rules.IDIsUnique(acc)
	a.NotNil(err)
	repo.AssertExpectations(t)
}

func TestStdAccountRules_IDIsUnique_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "id-is-unique-err",
	}
	repo.On("CountId", acc.ID).Return(0, errors.New("expecting failure")).Once()
	err := rules.IDIsUnique(acc)
	a.NotNil(err)
	a.EqualError(err, "expecting failure")
	repo.AssertExpectations(t)
}

func TestStdAccountRules_IDWillBeUnique_IDDoesntExist(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "will-be-unique-id",
	}
	repo.On("CountId", acc.ID).Return(0, nil).Once()
	err := rules.IDWillBeUnique(acc)
	a.Nil(err)
	repo.AssertExpectations(t)
}

func TestStdAccountRules_IDWillBeUnique_IDExists(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "non-unique-id",
	}
	repo.On("CountId", acc.ID).Return(1, nil).Once()
	err := rules.IDWillBeUnique(acc)
	a.NotNil(err)
	repo.AssertExpectations(t)
}

func TestStdAccountRules_IDWillBeUnique_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID: "id-is-unique-err",
	}
	repo.On("CountId", acc.ID).Return(0, errors.New("expecting failure")).Once()
	err := rules.IDWillBeUnique(acc)
	a.NotNil(err)
	a.EqualError(err, "expecting failure")
	repo.AssertExpectations(t)
}

func TestStdAccountRules_NicknameIsPresent_NicknameIsPresent(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Nickname: "nickname-is-present",
	}
	err := rules.NicknameIsPresent(acc)
	a.Nil(err)
}

func TestStdAccountRules_NicknameIsPresent_NicknameIsEmpty(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Nickname: "",
	}
	err := rules.NicknameIsPresent(acc)
	a.NotNil(err)
	a.EqualError(err, "nickname is blank")
}

func TestStdAccountRules_NicknameIsNotTooLong_NicknameIsCorrectLength(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Nickname: "iFitInMaxLen",
	}
	err := rules.NicknameIsNotTooLong(acc)
	a.Nil(err)
}

func TestStdAccountRules_NicknameIsNotTooLong_NicknameIsTooLong(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Nickname: "iAmWayTooLong",
	}
	err := rules.NicknameIsNotTooLong(acc)
	a.NotNil(err)
	a.EqualError(err, "nickname must be no longer than 12 characters")
}

func TestStdAccountRules_NicknameIsUniqueToID_NicknameIsUnique(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID:       "will-be-unique-id",
		Nickname: "My Nickname",
	}
	repo.On("GetByNicknameWithoutId", acc.Nickname, acc.ID).Return(nil, nil).Once()
	err := rules.NicknameIsUniqueToID(acc)
	a.Nil(err)
	repo.AssertExpectations(t)
}

func TestStdAccountRules_NicknameIsUniqueToID_NicknameNotUnique(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID:       "non-unique-id",
		Nickname: "My Nickname",
	}
	repo.On("GetByNicknameWithoutId", acc.Nickname, acc.ID).Return(&account.Account{}, nil).Once()
	err := rules.NicknameIsUniqueToID(acc)
	a.NotNil(err)
	a.EqualError(err, "nickname My Nickname already exists")
	repo.AssertExpectations(t)
}

func TestStdAccountRules_NicknameIsUniqueToID_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID:       "id-err",
		Nickname: "My Nickname",
	}
	repo.On("GetByNicknameWithoutId", acc.Nickname, acc.ID).Return(nil, errors.New("expecting failure")).Once()
	err := rules.NicknameIsUniqueToID(acc)
	a.NotNil(err)
	a.EqualError(err, "expecting failure")
	repo.AssertExpectations(t)
}

func TestStdAccountRules_SlugIsPresent_SlugIsPresent(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Slug: "slug-is-present",
	}
	err := rules.SlugIsPresent(acc)
	a.Nil(err)
}

func TestStdAccountRules_SlugIsPresent_SlugIsEmpty(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Slug: "",
	}
	err := rules.SlugIsPresent(acc)
	a.NotNil(err)
	a.EqualError(err, "slug is blank")
}

func TestStdAccountRules_SlugIsNotTooLong_SlugIsCorrectLength(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Slug: "ifitinmaxlen",
	}
	err := rules.SlugIsNotTooLong(acc)
	a.Nil(err)
}

func TestStdAccountRules_SlugIsNotTooLong_SlugIsTooLong(t *testing.T) {
	a := assert.New(t)
	_, rules := getMockAccountRules()

	acc := &account.Account{
		Slug: "iamwaytoolong",
	}
	err := rules.SlugIsNotTooLong(acc)
	a.NotNil(err)
	a.EqualError(err, "slug must be no longer than 12 characters")
}

func TestStdAccountRules_SlugIsUniqueToID_SlugIsUnique(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID:   "will-be-unique-id",
		Slug: "my-slug",
	}
	repo.On("GetBySlugWithoutId", acc.Slug, acc.ID).Return(nil, nil).Once()
	err := rules.SlugIsUniqueToID(acc)
	a.Nil(err)
	repo.AssertExpectations(t)
}

func TestStdAccountRules_SlugIsUniqueToID_SlugNotUnique(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID:   "non-unique-id",
		Slug: "my-slug",
	}
	repo.On("GetBySlugWithoutId", acc.Slug, acc.ID).Return(&account.Account{}, nil).Once()
	err := rules.SlugIsUniqueToID(acc)
	a.NotNil(err)
	a.EqualError(err, "slug my-slug already exists")
	repo.AssertExpectations(t)
}

func TestStdAccountRules_SlugIsUniqueToID_RepoReturnsErr(t *testing.T) {
	a := assert.New(t)
	repo, rules := getMockAccountRules()

	acc := &account.Account{
		ID:   "id-err",
		Slug: "my-slug",
	}
	repo.On("GetBySlugWithoutId", acc.Slug, acc.ID).Return(nil, errors.New("expecting failure")).Once()
	err := rules.SlugIsUniqueToID(acc)
	a.NotNil(err)
	a.EqualError(err, "expecting failure")
	repo.AssertExpectations(t)
}
