from abc import ABC, abstractmethod
from app.schemas import PlatformResult


class BasePlatform(ABC):

    @abstractmethod
    async def publish(self, message: str, cta_url: str) -> PlatformResult:
        pass