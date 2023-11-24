from fastapi.security import HTTPBearer
from fastapi import Request , HTTPException
from jwt_manager import validate_token
from config.database import Session
from routers.users import UserModel


class JWTbearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        db = Session()
        result_email = db.query(UserModel).filter(UserModel.email == data.email).first()
        if not result_email:
            raise HTTPException(status_code =403, details= "credenciales son invalidas")
        