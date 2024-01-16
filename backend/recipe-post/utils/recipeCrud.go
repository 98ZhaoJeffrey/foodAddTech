package util

import (
	"errors"
	database "example/recipe-post/db"
	"example/recipe-post/db/models"
	"fmt"
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type RecipeData struct {
	Title       string
	Description string
	Image       string
	Time        time.Duration
	Ingredients map[string]models.Ingredients
	Steps       []models.Step
	Nutritions  models.Nutritions
}

func CreateRecipe(data RecipeData) (*models.Recipe, error) {
	recipe := models.Recipe{
		Title:       data.Title,
		Description: data.Description,
		Image:       &data.Image,
		Time:        data.Time,
		Ingredients: data.Ingredients,
		Steps:       data.Steps,
		Nutritions:  data.Nutritions,
	}
	if err := database.DB.Create(&recipe).Error; err != nil {
		return nil, err
	}
	return &recipe, nil
}

func GetRecipeById(id uuid.UUID) (*models.Recipe, error) {
	var recipe models.Recipe
	if err := database.DB.First(&recipe, id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, fmt.Errorf("recipe not found")
		}
		return nil, err
	}
	return &recipe, nil
}

func DeleteRecipe(id uuid.UUID) error {
	if err := database.DB.Delete(&models.Recipe{}, id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return fmt.Errorf("recipe not found")
		}
		return err
	}
	return nil
}

// func updateRecipe(id uint, data recipeData) (*models.Recipe, error) {
// 	// impletement for later
// 	return nil, nil
// }
