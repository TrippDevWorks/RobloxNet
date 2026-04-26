import requests

class Auth:
    def __init__(self, cookie: str):
        self.session = requests.Session()
        self.session.cookies.set(".ROBLOSECURITY", cookie, domain=".roblox.com")
        self.xcsrf_token = self._get_xcsrf_token()
        self.session.headers.update({"X-CSRF-TOKEN": self.xcsrf_token})
        

    def get_xcsrf(self) -> str:
        response = self.session.post("https://auth.roblox.com/v2/logout")
        token = response.headers.get("x-csrf-token")

        if not token:
            raise RuntimeError("Failed to retrieve X-CSRF-Token.")

        return token
