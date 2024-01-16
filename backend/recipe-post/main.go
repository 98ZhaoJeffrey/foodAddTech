package main

import (
	"example/recipe-post/config"
	"example/recipe-post/router"
)

func Init() {
	// init models and other stuff
	config.LoadEnv()
}

func main() {
	router := router.InitRouter()
	router.Run("localhost:8080")
}
