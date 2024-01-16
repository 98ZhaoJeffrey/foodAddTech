package api

import (
	"example/recipe-post/db/models"
	util "example/recipe-post/utils"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type RecipeJson struct {
	Title       string                        `json:"title"`
	Description string                        `json:"description"`
	Image       string                        `json:"image"`
	Time        time.Duration                 `json:"time"`
	Ingredients map[string]models.Ingredients `json:"ingredients"`
	Steps       []models.Step                 `json:"steps"`
	Nutritions  models.Nutritions             `json:"nutritions"`
}

type IngredientsJson struct {
	Quantity uint   `json:"quantity"`
	Unit     string `json:"unit"`
}

type StepJson struct {
	Description string `json:"description"`
}

type NutritionsJson struct {
	Calories     uint `json:"calories"`
	Fat          uint `json:"fat"`
	Protein      uint `json:"protein"`
	Carbohydrate uint `json:"carbohydrate"`
	Sodium       uint `json:"sodium"`
	Cholesterol  uint `json:"cholesterol"`
	Sugar        uint `json:"sugar"`
	Fibre        uint `json:"fibre"`
}

func GetRecipeById(c *gin.Context) {
	id, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid UUID"})
		return
	}
	recipe, err := util.GetRecipeById(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, "Error with creating a recipe")
	}
	c.IndentedJSON(http.StatusOK, recipe)
}

func CreateRecipe(c *gin.Context) {
	var recipeJson RecipeJson
	if err := c.BindJSON(&recipeJson); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	recipeData := util.RecipeData{
		Title:       recipeJson.Title,
		Description: recipeJson.Description,
		Image:       recipeJson.Image,
		Time:        recipeJson.Time,
		Ingredients: recipeJson.Ingredients,
		Steps:       recipeJson.Steps,
		Nutritions:  recipeJson.Nutritions,
	}
	recipe, err := util.CreateRecipe(recipeData)

	if err != nil {
		c.JSON(http.StatusBadRequest, "Error with creating a recipe")
	}
	c.IndentedJSON(http.StatusOK, recipe)
}

func DeleteRecipe(c *gin.Context) {
	id, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid UUID"})
		return
	}
	util.DeleteRecipe(id)
	c.IndentedJSON(http.StatusOK, "Deleted a recipe")
}
