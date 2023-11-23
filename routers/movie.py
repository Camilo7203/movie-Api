from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_beare import JWTbearer

movie_rounter = APIRouter


class Movie(BaseModel):
    id: Optional[int] = None
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


@movie_rounter.get('/movies',tags=['movies'], response_model= list[Movie],status_code=200,dependencies=[Depends(JWTbearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_rounter.get('/movies/{id}',tags=['movies'], response_model= Movie)
def get_movie(id:int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
            return JSONResponse(status_code=404, content={'message':'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_rounter.get('/movies/',tags=['movies'],response_model= list[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15))-> list[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all
    if not result:
            return JSONResponse(status_code=404, content={'message':'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_rounter.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@movie_rounter.put('/movies/{id}',tags=['movies'],response_model= dict,status_code=200)
def update_movie(id: int,movie: Movie)-> dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200,content={"message": "Se modifico la pelicula"}) 


@movie_rounter.delete('/movies/{id}',tags=['movies'],response_model= dict,status_code=200)
def delete_movie(id: int)-> dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    db.delete(result)
    db.commit()

    return JSONResponse(status_code=200,content={"message": "Se elimino la pelicula"}) 
