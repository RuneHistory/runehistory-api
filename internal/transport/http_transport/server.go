package http_transport

import (
	"context"
	"fmt"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
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
	r := newRouter()
	httpServer := &http.Server{
		Addr:    listenAddress,
		Handler: r,
	}
	return &Server{
		httpServer: httpServer,
		Router:     r,
	}
}

func newRouter() chi.Router {
	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(10 * time.Second))
	return r
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
