from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def insert_into_db(session: AsyncSession,
                         table_name: str,
                         fields: dict[str, any],
                         schema: str = 'public') -> None:
    field_names, field_values = fields.items()
    field_list = ', '.join(field_names)
    val_list = ', '.join([f':{f_name}' for f_name in field_names])
    query = text(f'INSERT INTO {schema}.{table_name} ({field_list}) VALUES ({val_list});')
    await session.execute(query, fields)
