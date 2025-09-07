from fastapi import APIRouter

from .auth import router as auth_router
from .example import router as example_router

api_router = APIRouter()
api_router.include_router(example_router, prefix="/examples", tags=["examples"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

__all__ = ["api_router"]
