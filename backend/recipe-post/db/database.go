package database

import (
	"example/recipe-post/db/models"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConnectToDatabase() {
	database, err := gorm.Open(mysql.New(mysql.Config{
		DriverName: "my_mysql_driver",
		DSN:        "gorm:gorm@tcp(localhost:9910)/gorm?charset=utf8&parseTime=True&loc=Local",
	}), &gorm.Config{})

	if err != nil {
		panic("Failed to connect to database!")
	}
	DB = database
}

func Migrate() {
	err := DB.AutoMigrate(&models.Recipe{})
	if err != nil {
		return
	}
}
