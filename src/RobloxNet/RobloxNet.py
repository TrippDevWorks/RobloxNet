import requests
from .Legacy import Legacy
from .OpenCloud import OpenCloud

class Auth:
    def __init__(self, ClientType: str, Token: str):
        if not Token:
            raise ValueError("[AUTH] No authentication Token was provided on initalization, did you forget to add your api key?.")
        self.session = requests.Session()
        client_type = ClientType.strip().lower()
        if client_type == "legacy":
            self.session.cookies.set(".ROBLOSECURITY", Token, domain=".roblox.com")
            self.xcsrf_token = self.get_xcsrf()
            self.session.headers.update({"X-CSRF-TOKEN": self.xcsrf_token})
            self.client = Legacy(Token, session=self.session)
        elif client_type == "opencloud":
            self.session.headers.update({"x-api-key": Token})
            self.client = OpenCloud(Token, session=self.session)
        else:
            raise ValueError(
                f"Unsupported ClientType: {ClientType}. Choose 'Legacy' or 'OpenCloud'."
            )

    def get_xcsrf(self) -> str:
        response = self.session.post("https://auth.roblox.com/v2/logout")
        token = response.headers.get("x-csrf-token")
        if not token:
            raise RuntimeError("[AUTH] Failed to retrieve X-CSRF-Token.")
        return token
