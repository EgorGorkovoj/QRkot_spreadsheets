from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.core.constants import FORMAT


async def convert_seconds_to_dhms(seconds: int) -> str:
    """Функция для конвертации секунд в дни, часы, минуты, секунды."""
    days = seconds // (24 * 60 * 60)
    seconds -= days * (24 * 60 * 60)
    hours = seconds // (60 * 60)
    seconds -= hours * (60 * 60)
    minutes = seconds // 60
    seconds -= minutes * 60
    if days == 1:
        return f'{days} day, {hours}:{minutes}:{seconds}'
    return f'{days} days, {hours}:{minutes}:{seconds}'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Функция отвечающая за создание гугл-таблицы."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """
    Функция для выдачи прав доступа к таблице
    личному гугл-аккаунту.
    """
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """
    Функция отвечающая за формирование отчета в гугл-таблице
    на основе переданных данных. В гугл-таблицах значения по
    умолчанию в ячейках None, поэтому нужно использовать метод update.
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = list(project)
        new_row[1] = await convert_seconds_to_dhms(project[1])
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
