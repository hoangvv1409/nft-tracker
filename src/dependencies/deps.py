from typing import Any
from dataclasses import dataclass


@dataclass()
class Dependencies:
    session: Any

    @staticmethod
    def init_real(session):
        return Dependencies(
            session=session,
        )

    @staticmethod
    def init_fake():
        return None
