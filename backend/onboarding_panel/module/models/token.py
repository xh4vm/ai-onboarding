from .base import JSONModel


class TokenPair(JSONModel):
    access: str
    refresh: str


class TokenHeader(JSONModel):
    token: str

    def get_payload(self) -> str:
        try:
            _, payload = self.token.split()
        except Exception:
            raise ValueError("Bad token format")
            
        return payload
