package account

import "testing"

func TestNewAccount(t *testing.T) {
	uuid := "my-uuid"
	nickname := "Jim"
	slug := "jim"
	a := NewAccount(uuid, nickname, slug)
	if a.ID != uuid {
		t.Errorf("ID was incorrect, got: %s, want: %s", a.ID, uuid)
	}
	if a.Nickname != nickname {
		t.Errorf("Nickname was incorrect, got: %s, want: %s", a.Nickname, nickname)
	}
	if a.Slug != slug {
		t.Errorf("Slug was incorrect, got: %s, want: %s", a.Slug, slug)
	}
}
