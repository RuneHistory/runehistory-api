package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/runehistory/runehistory-api/internal"
	"github.com/runehistory/runehistory-api/internal/transport/http_transport"
	"os"
	"os/signal"
	"sync"
	"syscall"
)

func main() {
	wg := &sync.WaitGroup{}
	shutdownCh := make(chan struct{})
	errCh := make(chan error)
	go HandleShutdownSignal(shutdownCh)

	db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:3306)/runehistory?multiStatements=true")
	if err != nil {
		panic(err)
	}
	err = db.Ping()
	if err != nil {
		panic(err)
	}

	s := http_transport.NewServer("127.0.0.1:8000")

	// initialise the app
	internal.Init(s.Router, db)

	// start publicly accessible things / websocket servers
	go s.Start(wg, shutdownCh, errCh)

	select {
	case err := <-errCh:
		fmt.Println("Failed to start up: " + err.Error())

	case <-shutdownCh:
		fmt.Println("Waiting for shutdown")
		wg.Wait()
		fmt.Println("All services shutdown")
	}
}

func HandleShutdownSignal(shutdownCh chan struct{}) {
	quitCh := make(chan os.Signal)
	signal.Notify(quitCh, os.Interrupt, syscall.SIGTERM)

	hit := false
	for {
		<-quitCh
		if hit {
			os.Exit(0)
		}
		if !hit {
			close(shutdownCh)
		}
		hit = true
	}
}
