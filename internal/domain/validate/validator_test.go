package validate

import (
	"errors"
	"github.com/runehistory/runehistory-api/internal/domain/account"
	validateMocks "github.com/runehistory/runehistory-api/internal/domain/validate/mocks"
	"github.com/stretchr/testify/assert"
	"testing"
)

func getMock() (*validateMocks.MockAccountRules, Validator) {
	rules := new(validateMocks.MockAccountRules)
	validator := NewValidator(rules)
	return rules, validator
}

func TestStdValidator_NewAccount_AllValidationsWork(t *testing.T) {
	a := assert.New(t)
	rules, validator := getMock()

	acc := &account.Account{}

	calledRules := []string{
		"IDIsPresent",
		"IDIsCorrectLength",
		"IDWillBeUnique",
		"NicknameIsPresent",
		"NicknameIsNotTooLong",
		"NicknameIsUniqueToID",
		"SlugIsPresent",
		"SlugIsNotTooLong",
		"SlugIsUniqueToID",
	}

	for _, rule := range calledRules {
		rules.On(rule, acc).Return(nil).Once()
	}
	err := validator.NewAccount(acc)
	a.Nil(err, "not expecting err: %v", err)
	rules.AssertExpectations(t)

	for _, failingRule := range calledRules {
		rules, validator = getMock()
		hitFailed := false
		for _, rule := range calledRules {
			if rule == failingRule {
				hitFailed = true
				e := errors.New(failingRule)
				rules.On(rule, acc).Return(e).Once()
			} else if !hitFailed {
				rules.On(rule, acc).Return(nil).Once()
			}
		}
		err := validator.NewAccount(acc)
		a.EqualError(err, failingRule)
		rules.AssertExpectations(t)
	}
}

func TestStdValidator_UpdateAccount_AllValidationsWork(t *testing.T) {
	a := assert.New(t)
	rules, validator := getMock()

	acc := &account.Account{}

	calledRules := []string{
		"IDIsPresent",
		"IDIsCorrectLength",
		"IDIsUnique",
		"NicknameIsPresent",
		"NicknameIsNotTooLong",
		"NicknameIsUniqueToID",
		"SlugIsPresent",
		"SlugIsNotTooLong",
		"SlugIsUniqueToID",
	}

	for _, rule := range calledRules {
		rules.On(rule, acc).Return(nil).Once()
	}
	err := validator.UpdateAccount(acc)
	a.Nil(err, "not expecting err: %v", err)
	rules.AssertExpectations(t)

	for _, failingRule := range calledRules {
		rules, validator = getMock()
		hitFailed := false
		for _, rule := range calledRules {
			if rule == failingRule {
				hitFailed = true
				e := errors.New(failingRule)
				rules.On(rule, acc).Return(e).Once()
			} else if !hitFailed {
				rules.On(rule, acc).Return(nil).Once()
			}
		}
		err := validator.UpdateAccount(acc)
		a.EqualError(err, failingRule)
		rules.AssertExpectations(t)
	}
}
