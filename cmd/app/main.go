package main

import (
	"database/sql"
	"fmt"
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

	// start mysql etc
	var db *sql.DB
	s := http_transport.NewServer("127.0.0.1:8080")

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
