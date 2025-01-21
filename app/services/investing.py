from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def close_project_or_donat(
        obj_db: Union[CharityProject, Donation],
        close_date: datetime
):
    """Меняет статус объекта БД пожертвования или проекта."""
    obj_db.fully_invested = True
    obj_db.close_date = close_date
    obj_db.invested_amount = obj_db.full_amount


async def create_new_investing(
        obj_db_project: Union[CharityProject, Donation],
        obj_db_invest: Union[list[CharityProject], list[Donation]],
        session: AsyncSession
) -> None:
    """
    Функция инвестирования проектов.
    Параметры функции:
    1) obj_db_project - объект БД модели проекта или пожертвования;
    2) obj_db_invest - список объектов БД модели проекта или пожертвования;
    3) session - асинхронная сессия.
    Если obj_db_project является пожертвованием,
    а obj_db_invest - незакрытыми проектами,
    процесс инвестирования представляет собой распределение суммы пожертвования
    между незакрытыми проектами.
    Если obj_db_project является проектом,
    а obj_db_invest - нераспределенными пожертвованиями,
    процесс инвестирования представляет собой добавление в проект сумм
    нераспределенных пожертвований.
    В процессе инвестирования объекты, средства которых были распределены,
    будут закрыты (fully_invested=True). Все изменения будут сохранятся в БД.
    """
    # Треб. сумм для проекта.
    full_amount = obj_db_project.full_amount
    close_date = datetime.now()
    for invest in obj_db_invest:
        # Остаток свободной суммы пожертвования.
        free_sum = invest.full_amount - invest.invested_amount
        # Остаток суммы проекта.
        remains_sum = full_amount - free_sum
        if remains_sum > 0:
            close_project_or_donat(invest, close_date)
            # Заинвестировано.
            obj_db_project.invested_amount += full_amount - remains_sum
            full_amount = remains_sum
        elif remains_sum < 0:
            close_project_or_donat(obj_db_project, close_date)
            invest.invested_amount += full_amount
        else:
            close_project_or_donat(invest, close_date)
            close_project_or_donat(obj_db_project, close_date)
        session.add(invest)
        if remains_sum <= 0:
            break
    session.add(obj_db_project)
    await session.commit()
    await session.refresh(obj_db_project)
