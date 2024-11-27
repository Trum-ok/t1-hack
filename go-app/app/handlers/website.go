package handlers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func AddWebsitePage(c echo.Context) error {
	return c.String(http.StatusOK, "Website page")
}

func AddWebsiteSubmit(c echo.Context) error {
	return c.String(http.StatusOK, "Website submit")
}
