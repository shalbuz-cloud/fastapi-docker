import uuid
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from app.forms import UserLoginForm, UserCreateForm
from app.models import connect_db, User, AuthToken
from app.utils import get_password_hash
from app.auth import check_auth_token

router = APIRouter()


@router.get('/')
def index():
    return {'status': 'OK'}


@router.post('/login', name='user:login')
def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        return {'error': 'Email/password invalid'}
    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    database.add(auth_token)
    database.commit()
    return {'auth_token': auth_token.token}


@router.post('/user', name='user:create')
def create_user(user: UserCreateForm = Body(..., embed=True), database=Depends(connect_db)):
    exists_user = database.query(User.id).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        nickname=user.nickname,
    )
    database.add(new_user)
    database.commit()
    return {'user_id': new_user.id}


@router.get('/user', name='user:get')
def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()
    return {'id': user.id, 'email': user.email, 'nickname': user.nickname}
