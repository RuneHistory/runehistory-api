# RuneHistory API

## Migrations
We are using [migrate](https://github.com/golang-migrate/migrate) for migrations.

```
docker run -v {{ migration dir }}:/migrations --network host migrate/migrate 
    -path=/migrations/ -database mysql://localhost:3306/database up {{ version }}
```