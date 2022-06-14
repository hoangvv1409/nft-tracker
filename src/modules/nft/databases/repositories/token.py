from ..interface import ITokenRepository
from ..models import TokenSchema


class TokenRepository(ITokenRepository):
    def __init__(self, session):
        self.session = session
        self.model = TokenSchema
