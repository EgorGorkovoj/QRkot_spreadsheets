from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        """Получить проект по имени."""
        project_id = await session.execute(
            select(self.model.id).where(
                self.model.name == project_name
            )
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[tuple[str]]:
        """
        Метод для получения списка закрытых проектов
        с расчетом разницы времени, которое понадобилось
        для сбора пожертвований.
        Время сбора указывается в секундах.
        """
        second = (extract('second', self.model.create_date) -
                  extract('second', self.model.close_date))
        stmt = select([
            self.model.name,
            second.label('time'),
            self.model.description
        ]).where(self.model.fully_invested.is_(True)).order_by('time')
        projects = await session.execute(stmt)
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
