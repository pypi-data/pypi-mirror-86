import requests


# class AbstractAuth:
#     """Abstract class to make authenticated requests."""
#
#     def __init__(self, websession, host: str):
#         """Initialize the auth."""
#         self.websession = websession
#         self.host = host
#
#     @abstractmethod
#     async def async_get_access_token(self) -> str:
#         """Return a valid access token."""
#
#     async def request(self, method, url, **kwargs) -> ClientResponse:
#         """Make a request."""
#         headers = kwargs.get("headers")
#
#         if headers is None:
#             headers = {}
#         else:
#             headers = dict(headers)
#
#         access_token = await self.async_get_access_token()
#         headers["authorization"] = f"Bearer {access_token}"
#
#         return await self.websession.request(
#             method, f"{self.host}/{url}", **kwargs, headers=headers,
#         )


class AbstractAuth:

    def __init__(self, token):
        self.token = token

        self.header = None
        self.host = "openapi.investec.com"
        self.domain = "za"
        self.api = "pb"
        self.version = "v1"
        self.accounts = "accounts"
        self.balance = "accounts{accountId}/balance"

    # def get(self):
    #     print("Random crap")
