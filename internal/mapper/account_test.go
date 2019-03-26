package mapper

import (
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestAccountToHttpV1(t *testing.T) {
	a := assert.New(t)
	acc := account.NewAccount("my-uuid", "Jim", "jim")
	mapped := AccountToHttpV1(acc)
	a.Equal(acc.ID, mapped.ID)
	a.Equal(acc.Nickname, mapped.Nickname)
	a.Equal(acc.Slug, mapped.Slug)
}

func TestAccountFromHttpV1(t *testing.T) {
	a := assert.New(t)
	acc := &AccountHttpV1{
		ID:       "my-uuid",
		Slug:     "jim",
		Nickname: "Jim",
	}
	mapped := AccountFromHttpV1(acc)
	a.Equal(acc.ID, mapped.ID)
	a.Equal(acc.Nickname, mapped.Nickname)
	a.Equal(acc.Slug, mapped.Slug)
}
