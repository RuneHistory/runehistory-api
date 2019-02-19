package http_transport

import (
	"context"
	"fmt"
	"github.com/go-chi/chi"
	"net"
	"net/http"
	"sync"
	"time"
)

type Server struct {
	httpServer *http.Server
	Router     chi.Router
}

func NewServer(listenAddress string) *Server {
	r := chi.NewRouter()
	httpServer := &http.Server{
		Addr:    listenAddress,
		Handler: r,
	}
	return &Server{
		httpServer: httpServer,
		Router:     r,
	}
}

func (s *Server) Start(stopWg *sync.WaitGroup, shutdownCh chan struct{}, errCh chan error) {
	stopWg.Add(1)
	defer stopWg.Done()

	startFuncErrCh := make(chan error)
	startFunc := func() {
		fmt.Println("Starting server")
		listener, err := net.Listen("tcp", s.httpServer.Addr)
		if err != nil {
			startFuncErrCh <- err
			return
		}
		fmt.Println("Server listening at " + listener.Addr().String())
		err = s.httpServer.Serve(listener)
		if err != nil {
			startFuncErrCh <- err
			return
		}
	}

	stopFunc := func() {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		err := s.httpServer.Shutdown(ctx)
		if err != nil {
			panic(err)
		}
	}

	go startFunc()

	select {
	case err := <-startFuncErrCh:
		errCh <- err
	case <-shutdownCh:
		stopFunc()
	}
}
