//package http_transport
//
//import (
//	"encoding/json"
//	"github.com/runehistory/runehistory-api/internal/errs"
//	"io/ioutil"
//	"net/http"
//	"strings"
//)
//
//func RequestFromBody(r *http.Request, req interface{}) error {
//	requestBytes, err := ioutil.ReadAll(r.Body)
//	if err != nil {
//		return errs.BadRequest(err.Error())
//	}
//
//	err = json.Unmarshal(requestBytes, req)
//	if err != nil {
//		return errs.BadRequest(err.Error())
//	}
//	return nil
//}

package http_transport

import (
	"encoding/json"
	"fmt"
	"github.com/runehistory/runehistory-api/internal/errs"
	"io/ioutil"
	"net/http"
	"strings"

	"github.com/tomwright/chiuriattr"
	"github.com/tomwright/queryparam"
)

// ParseRequest parses all parts of the given request
func ParseRequest(r *http.Request, req interface{}) error {
	if err := ParseRequestURL(r, req); err != nil {
		return err
	}
	if err := ParseRequestJSON(r, req); err != nil {
		return err
	}
	return nil
}

// ParseRequestURL parses all parts of the given request that relate to the URL
func ParseRequestURL(r *http.Request, req interface{}) error {
	if err := ParseRequestURI(r, req); err != nil {
		return err
	}
	if err := ParseRequestQuery(r, req); err != nil {
		return err
	}
	return nil
}

func ParseRequestURI(r *http.Request, req interface{}) error {
	err := chiuriattr.Unmarshal(r, req)
	if err != nil {
		return errs.BadRequest(fmt.Sprintf("could not decode request uri: %s", err))
	}
	return nil
}

func ParseRequestQuery(r *http.Request, req interface{}) error {
	err := queryparam.Unmarshal(r.URL, req)
	if err != nil {
		return errs.BadRequest(fmt.Sprintf("could not decode query attributes: %s", err))
	}
	return nil
}

func ParseRequestJSON(r *http.Request, req ...interface{}) error {
	if r.ContentLength == 0 {
		return nil
	}
	if strings.HasPrefix(r.Header.Get("Content-Type"), "application/json") {
		bytes, err := GetRequestBody(r)
		if err != nil {
			return err
		}

		for _, re := range req {
			err = ParseJSONFromBytes(bytes, re)
			if err != nil {
				return err
			}
		}
	}

	return nil
}

func GetRequestBody(r *http.Request) ([]byte, error) {
	bytes, err := ioutil.ReadAll(r.Body)
	if err != nil {
		return nil, errs.UnprocessableEntity(fmt.Sprintf("could not read request body: %s", err))
	}
	return bytes, nil
}

func ParseJSONFromBytes(bytes []byte, req interface{}) error {
	err := json.Unmarshal(bytes, req)
	if err != nil {
		return errs.BadRequest(fmt.Sprintf("could not decode request body: %s", err))
	}

	return nil
}
