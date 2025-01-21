from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.constants import MAX_LENGTH


class CharityProjectBase(BaseModel):
    """Базовая cхема благотворительного проекта."""
    name: str = Field(None, max_length=MAX_LENGTH)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    """Схема частичного обновления благотворительного проекта."""
    pass


class CharityProjectCreate(CharityProjectUpdate):
    """Схема для создания благотворительного проекта."""
    name: str = Field(..., max_length=MAX_LENGTH)
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    """Схема для отображения информации о проекте."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
