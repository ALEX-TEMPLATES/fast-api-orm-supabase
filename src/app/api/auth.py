import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from supabase import Client

from app.config.supabase_client import supabase_client

router = APIRouter()

ACCESS_COOKIE_NAME = "sb_at"


class LoginRequest(BaseModel):
    email: str
    password: str


def get_supabase_client() -> Client:
    """Возвращает единый экземпляр клиента Supabase."""
    return supabase_client


@router.post("/login")
def login(
    response: Response,
    login_data: LoginRequest,
    client: Client = Depends(get_supabase_client),
):
    """
    Аутентифицирует пользователя с кредами из настроек и устанавливает
    HttpOnly cookie с access_token.
    """
    try:
        auth_response = client.auth.sign_in_with_password(
            {
                "email": login_data.email,
                "password": login_data.password,
            }
        )
        session = auth_response.session
        if not session or not session.access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не удалось получить сессию от Supabase.",
            )

        response.set_cookie(
            key=ACCESS_COOKIE_NAME,
            value=session.access_token,
            httponly=True,
            samesite="lax",  # 'strict' or 'lax'
            secure=False,  # В проде должно быть True, если используется HTTPS
            path="/",
        )
        return {"status": "ok", "message": "Успешный вход."}

    except Exception as e:
        logging.error(f"Ошибка при входе через Supabase: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка Supabase: {str(e)}"
        )


def get_current_user(
    request: Request,
    client: Client = Depends(get_supabase_client),
) -> dict:
    """
    Зависимость для проверки токена из cookie и получения данных пользователя.
    """
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен доступа отсутствует.",
        )
    try:
        user_response = client.auth.get_user(jwt=token)
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не удалось получить пользователя по токену.",
            )
        return user_response.user.model_dump()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен невалиден или истек.",
        )


def require_user(request: Request) -> dict:
    """
    Проверяет, был ли пользователь аутентифицирован middleware.
    Если нет - возвращает ошибку 401.
    """
    if not hasattr(request.state, "user") or request.state.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходима аутентификация",
        )
    return request.state.user


@router.get("/me")
def me(current_user: dict = Depends(require_user)):
    """
    Возвращает информацию о текущем аутентифицированном пользователе.
    """
    return {"user": current_user}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    """
    Удаляет cookie аутентификации, завершая сессию пользователя.
    """
    response.delete_cookie(
        key=ACCESS_COOKIE_NAME,
        path="/",
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
