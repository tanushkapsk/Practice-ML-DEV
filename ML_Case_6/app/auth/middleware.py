# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from typing import Annotated
# from sqlalchemy.orm import Session
# from app.db.dependencies import get_db
#
# from .config import SECRET_KEY, ALGORITHM
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid authentication credentials")
#
#         from users.models import User
#         user = db.query(User).filter(User.username == username).first()
#         if user is None:
#             raise HTTPException(status_code=401, detail="User not found")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated, Optional, NamedTuple
from sqlalchemy.orm import Session
from app.db.dependencies import get_db

from .config import SECRET_KEY, ALGORITHM
from users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class CurrentUser(NamedTuple):
    user: Optional[User] = None
    error_key: str = ''
    error_message: str = ''


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db),
) -> CurrentUser:
    user = None
    error_key = ''
    error_message = ''

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            error_key = 'invalid',
            error_message = 'Недопустимые учетные данные для проверки подлинности.',
        else:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                error_key = 'not_authorization',
                error_message = 'Пользователь не найден. Пожалуйста, авторизуйтесь или зарегистрируйтесь повторно.',

    except JWTError:
        error_key = 'not_authorization',
        error_message = 'Ваша сессия авторизации истекла. Пожалуйста, авторизуйтесь или зарегистрируйтесь повторно.',

    return CurrentUser(user=user, error_key=error_key, error_message=error_message)
