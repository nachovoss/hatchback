from .auth import router as auth_router
from .tenant import router as tenant_router
from .user import router as user_router

routers = [auth_router, tenant_router, user_router]
