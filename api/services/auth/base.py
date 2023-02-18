class BaseAuthenticationService:
    async def authenticate(self, **credentials):
        pass

    async def verify_authentication(self, **kwargs):
        pass

    async def get_current_user(self):
        pass


class BaseAuthorizationService:
    pass
