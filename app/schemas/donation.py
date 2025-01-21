from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    """Схема для создания пожертвования."""
    full_amount: PositiveInt
    comment: Optional[str]


class DonationtDB(DonationCreate):
    """Схема для короткого отображения пожертвования пользователя."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class AllDonationDB(DonationtDB):
    """Схема для отображения полной информации пожертвования пользователя."""
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]