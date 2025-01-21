from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_before_edit(
        charity_project: CharityProject,
        update_data: CharityProjectUpdate
) -> None:
    """Проверяет проект перед его редактированием."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    if (update_data.full_amount and
       update_data.full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=422,
            detail='Требуемая сумма не может быть меньше уже внесенной!'
        )


async def check_charity_project_is_not_invested_or_closed(
        charity_project: CharityProject
) -> None:
    """Проверяет, есть ли в проекте пожертвования."""
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Проект не подлежит удалению, в него внесены пожертвования!'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Удаление закрытых проектов запрещено!'
        )