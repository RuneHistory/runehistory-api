package account

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestNewAccount(t *testing.T) {
	a := assert.New(t)
	uuid := "my-uuid"
	nickname := "Jim"
	slug := "jim"
	acc := NewAccount(uuid, nickname, slug)
	a.Equal(uuid, acc.ID)
	a.Equal(nickname, acc.Nickname)
	a.Equal(slug, acc.Slug)
}
