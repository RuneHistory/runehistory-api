package mapper

import (
	"github.com/runehistory/runehistory-api/internal/domain/account"
	"testing"
)

func TestAccountToHttpV1Mapping(t *testing.T) {
	acc := account.NewAccount("my-uuid", "Jim", "jim")
	mapped, err := AccountToHttpV1(acc)
	if err != nil {
		t.Error(err)
	}
	if mapped.UUID != acc.ID {
		t.Errorf("ID was incorrect, got: %s, want: %s", mapped.UUID, acc.ID)
	}
	if mapped.Nickname != acc.Nickname {
		t.Errorf("Nickname was incorrect, got: %s, want: %s", mapped.Nickname, acc.Nickname)
	}
	if mapped.Slug != acc.Slug {
		t.Errorf("Slug was incorrect, got: %s, want: %s", mapped.Slug, acc.Slug)
	}
}
