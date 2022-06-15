import math
from typing import Tuple, List
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

    def get_sorted_tokens(
        self, contract_address: str,
        page: int = 1, page_size: int = 50,
        sort_by: str = None,
    ) -> Tuple[int, int, List[TokenSchema]]:
        q = self.session.query(TokenSchema)
        q = q.filter(TokenSchema.contract_address == contract_address)

        count = q.count()

        q = q.limit(page_size)
        q = q.offset((page - 1) * page_size)
        records = q.all()

        total_page = math.ceil(count / page_size)

        return count, total_page, records
