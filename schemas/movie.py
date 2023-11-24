from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    title: str = Field(min_length=3,max_length=15)
    overview: str = Field(min_length=15,max_length=50)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=10)

    model_config = {
     "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 9.9,
                    "category": "Acción"
                }
            ]
        }
    }