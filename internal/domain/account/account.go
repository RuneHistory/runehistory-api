package account

type Account struct {
	ID       string
	Nickname string
	Slug     string
}

func NewAccount(uuid string, nickname string, slug string) *Account {
	return &Account{
		ID:       uuid,
		Nickname: nickname,
		Slug:     slug,
	}
}
