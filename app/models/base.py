from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base
from app.core.constants import DEFAULT_VALUE


class FinanceBaseModel(Base):
    """Абстрактная модель. Общая для моделей пожертвования и проектов."""
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_VALUE)
    fully_invested = Column(Boolean(), default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)