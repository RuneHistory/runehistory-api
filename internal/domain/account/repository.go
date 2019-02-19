package account

type Repository interface {
	Get(id string) (*Account, error)
}
