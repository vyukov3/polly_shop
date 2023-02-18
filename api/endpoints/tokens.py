from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm

from api.schemas import tokens as schemas
from api.services.auth.authentication import JwtAuthenticationService, get_authentication_service


api_router = APIRouter(prefix="/tokens", tags=["Authentication"])


@api_router.post("")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: JwtAuthenticationService = Depends(get_authentication_service),
) -> schemas.TokensResponse:
    tokens = await auth_service.authenticate(form_data.username, form_data.password)
    return schemas.TokensResponse.construct(access_token=tokens.access_token, refresh_token=tokens.refresh_token)


@api_router.post("/refresh")
async def refresh(
    bearer: str = Depends(
        HTTPBearer(scheme_name="Refresh token", description="Set Authorization header to refresh token")
    ),
    auth_service: JwtAuthenticationService = Depends(get_authentication_service),
) -> schemas.AccessToken:
    await auth_service.verify_authentication(bearer.credentials, token_type="refresh")
