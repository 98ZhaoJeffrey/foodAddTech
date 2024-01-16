package router

import (
	"net/http"

	"example/recipe-post/router/api"

	"github.com/gin-gonic/gin"
)

func helloWorld(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, "Hello World from Recipe Post")
}

func InitRouter() *gin.Engine {
	router := gin.Default()
	router.GET("/hello", helloWorld)

	apiRouter := router.Group("/api")
	recipeRouter := apiRouter.Group("/recipe")
	// need to protect with jwt token
	{
		recipeRouter.GET("/:id", api.GetRecipeById)
		recipeRouter.POST("/", api.CreateRecipe)
		recipeRouter.DELETE("/:id", api.DeleteRecipe)
	}
	return router
}
