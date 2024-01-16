package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Ingredients struct {
	Quantity uint
	Unit     string
}

type Step struct {
	Description string
}

type Nutritions struct {
	Calories     uint
	Fat          uint
	Protein      uint
	Carbohydrate uint
	Sodium       uint
	Cholesterol  uint
	Sugar        uint
	Fibre        uint
}

type Recipe struct {
	Id          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4()"`
	Title       string
	Description string
	Image       *string
	Time        time.Duration          `gorm:"not null"`
	Ingredients map[string]Ingredients `gorm:"not null"`
	Steps       []Step                 `gorm:"not null"`
	Nutritions  Nutritions             `gorm:"not null"`
}

func (r *Recipe) BeforeCreate(tx *gorm.DB) {
	r.Id = uuid.New()
}
