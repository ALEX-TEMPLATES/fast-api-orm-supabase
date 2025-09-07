import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.config.supabase_client import supabase_client

ACCESS_COOKIE_NAME = "sb_at"
PUBLIC_PATHS = ["/auth/login", "/docs", "/openapi.json"]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(
            f"AuthMiddleware received request: {request.method} {request.url.path}"
        )
        # Пропускаем WebSocket запросы без проверки
        if request.scope["type"] == "websocket":
            return await call_next(request)

        # Пропускаем публичные эндпоинты
        if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
            return await call_next(request)

        # 0. Пропускаем OPTIONS запросы без проверки
        if request.method == "OPTIONS":
            response = await call_next(request)
            return response

        # 1. Инициализируем user в state как None
        request.state.user = None

        # 2. Пытаемся получить токен из cookie
        token = request.cookies.get(ACCESS_COOKIE_NAME)

        if token:
            try:
                # Используем единый клиент Supabase
                user_response = supabase_client.auth.get_user(jwt=token)
                if (
                    user_response
                    and user_response.user
                    and user_response.user.aud == "authenticated"
                ):  # type: ignore
                    logging.info(f"Юзера получили2: {user_response.user.email}")  # type: ignore
                    request.state.user = user_response.user.email
                    response = await call_next(request)
                    return response
                else:
                    raise ValueError("Невалидные данные пользователя из токена.")

            except Exception as e:
                # Если токен есть, но он невалиден (истек, подделан),
                # просто ничего не делаем. request.state.user останется None.
                logging.warning(f"Ошибка валидации токена в middleware: {e}")
                # Если токен есть, но он невалиден, прерываем запрос с ошибкой 401
                return Response(status_code=401, content="Invalid or expired token")

        # 6. Передаем управление дальше (либо к следующему middleware, либо к роуту)
        response = await call_next(request)
        return response
