from api.endpoints.health_check import api_router as health_check_router
from api.endpoints.users import api_router as users_router
from api.endpoints.tokens import api_router as tokens_router


list_of_routes = [
    health_check_router,
    users_router,
    tokens_router,
]


__all__ = [
    "list_of_routes",
]
