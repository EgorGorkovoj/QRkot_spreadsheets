from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_charity_project_exists,
    check_charity_project_before_edit,
    check_charity_project_is_not_invested_or_closed
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import create_new_investing


router = APIRouter()


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получение списка благотворительных проектов.
    Доступно всем пользователям.
    """
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создание благотворительного проекта.
    Только для суперпользователей.
    """
    await check_name_duplicate(charity_project.name, session)
    project = await charity_project_crud.create(
        charity_project, session
    )
    free_donations = await (
        donation_crud.get_a_free_projects_or_dotanations(session)
    )
    if free_donations is not None:
        await create_new_investing(project, free_donations, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Частичное обновление благотворительного проекта.
    Только для суперпользователей.
    """
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_before_edit(charity_project, obj_in)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Удаление благотворительного проекта. Только для суперпользователей.
    Нельзя удалить закрытый или инвестировынный проект.
    """
    project = await check_charity_project_exists(project_id, session)
    await check_charity_project_is_not_invested_or_closed(project)
    project = await charity_project_crud.remove(project, session)
    return project
