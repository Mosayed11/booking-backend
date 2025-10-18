from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import hashlib
from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter(prefix='/auth', tags=['auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str = ''

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    email: str
    full_name: str

users_db = {}
SECRET_KEY = 'my-super-secret-key-for-testing-123456'

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({'exp': expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        email = payload.get('sub')
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token'
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )

@router.post('/register')
async def register(user_data: UserRegister):
    if user_data.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered'
        )
    
    hashed_password = hash_password(user_data.password)
    
    users_db[user_data.email] = {
        'email': user_data.email,
        'hashed_password': hashed_password,
        'full_name': user_data.full_name
    }
    
    return {'message': 'User registered successfully', 'email': user_data.email}

@router.post('/login')
async def login(user_data: UserLogin):
    user = users_db.get(user_data.email)
    
    if not user or not verify_password(user_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password'
        )
    
    access_token = create_access_token({'sub': user_data.email})
    
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'message': 'Login successful'
    }

@router.get('/me')
async def get_current_user_endpoint(current_user: str = Depends(get_current_user)):
    user = users_db.get(current_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return UserResponse(email=user['email'], full_name=user['full_name'])
