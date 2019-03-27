package validate

import "github.com/runehistory/runehistory-api/internal/domain/account"

type Validator interface {
	// A set of different states/actions that may be performed.
	// Have tests against these funcs to make sure each one tests the resource
	// as expected.
	// Each one of these funcs should just use different sets of the "rules" we create in the other files/
	NewAccount(a *account.Account) error
	UpdateAccount(a *account.Account) error
}

func NewValidator(accountRules AccountRules) Validator {
	return &StdValidator{
		accountRules: accountRules,
	}
}

type StdValidator struct {
	accountRules AccountRules
}

func (x *StdValidator) NewAccount(a *account.Account) error {
	if err := x.accountRules.IDIsPresent(a); err != nil {
		return err
	}
	if err := x.accountRules.IDIsCorrectLength(a); err != nil {
		return err
	}
	if err := x.accountRules.IDWillBeUnique(a); err != nil {
		return err
	}
	if err := x.accountRules.NicknameIsPresent(a); err != nil {
		return err
	}
	if err := x.accountRules.NicknameIsNotTooLong(a); err != nil {
		return err
	}
	if err := x.accountRules.NicknameIsUniqueToID(a); err != nil {
		return err
	}
	if err := x.accountRules.SlugIsPresent(a); err != nil {
		return err
	}
	if err := x.accountRules.SlugIsNotTooLong(a); err != nil {
		return err
	}
	if err := x.accountRules.SlugIsUniqueToID(a); err != nil {
		return err
	}
	return nil
}

func (x *StdValidator) UpdateAccount(a *account.Account) error {
	if err := x.accountRules.IDIsPresent(a); err != nil {
		return err
	}
	if err := x.accountRules.IDIsCorrectLength(a); err != nil {
		return err
	}
	if err := x.accountRules.IDIsUnique(a); err != nil {
		return err
	}
	if err := x.accountRules.NicknameIsPresent(a); err != nil {
		return err
	}
	if err := x.accountRules.NicknameIsNotTooLong(a); err != nil {
		return err
	}
	if err := x.accountRules.NicknameIsUniqueToID(a); err != nil {
		return err
	}
	if err := x.accountRules.SlugIsPresent(a); err != nil {
		return err
	}
	if err := x.accountRules.SlugIsNotTooLong(a); err != nil {
		return err
	}
	if err := x.accountRules.SlugIsUniqueToID(a); err != nil {
		return err
	}
	return nil
}
