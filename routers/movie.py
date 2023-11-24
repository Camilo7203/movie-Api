from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from typing import  List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from services.movie import MovieService
from schemas.movie import Movie

movie_rounter = APIRouter()

@movie_rounter.get('/movies',tags=['movies'], response_model= list[Movie],status_code=200)
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_rounter.get('/movies/{id}',tags=['movies'], response_model= Movie)
def get_movie(id:int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
            return JSONResponse(status_code=404, content={'message':'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_rounter.get('/movies/',tags=['movies'],response_model= list[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15))-> list[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
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
