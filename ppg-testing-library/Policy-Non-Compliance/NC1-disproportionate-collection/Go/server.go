package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/rs/zerolog/log"
)

type Message struct {
	Name      string
	Joke      string
}

func main() {
	http.ListenAndServe(":8080", NewRouter())
}

func NewRouter() *gin.Engine {
	r := gin.New()
	r.Use(gin.Recovery())
	r.Use(logger.SetLogger())

	r.POST("/data", parse_data)
	r.POST("/data1", parse_data1)

	return r
}

func parse_data(c *gin.Context) {
    c.Request.ParseForm()
	name := c.Request.Form.Get("name")
	joke := c.Request.Form.Get("joke")
    message := &Message{
        Name: name,
        Joke: joke
    }
}

// TODO split this up into a separate test case and align with Python
func parse_data1(c *gin.Context) {
    c.Request.ParseForm()
	name := c.Request.Form.Get("name")
	joke := c.Request.Form.Get("joke")
    message := &Message{
        Name: name,
        Joke: joke
    }
	process(joke)}

func process(any: data){
}