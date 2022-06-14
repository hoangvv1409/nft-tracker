from ..interface import ITokenRepository
from ..models import TokenSchema


class TokenRepository(ITokenRepository):
    def __init__(self, session):
        self.session = session
        self.model = TokenSchema

    def count(self, contract_address: str):
        q = self.session.query(TokenSchema)
        q = q.filter(
            TokenSchema.contract_address == contract_address)

        return q.count()
