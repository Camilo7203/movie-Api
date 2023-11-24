from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jwt_manager import create_token
from config.database import Session
from models.users import User as UserModel
from fastapi.encoders import jsonable_encoder
from schemas.user import User

user_rounter = APIRouter()


@user_rounter.get('/users',tags=['users'],status_code=200)
def get_movies() :
    db = Session()
    result =result = db.query(UserModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@user_rounter.post('/users/login', tags=['users'])
def login(user: User):
    db = Session()
    result_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    result_password = db.query(UserModel).filter(UserModel.password == user.password).first()
    if not result_email and not result_password:
        return JSONResponse(status_code=404, content={'message':'No se ha encontrado el usuario y/o contraseña'})
    token: str =  create_token(user.dict())
    return JSONResponse(status_code=200,content=token)


@user_rounter.post('/users/register', tags=['users'])
def create_user(user: User):
    db = Session()
    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el usuario"})
    
