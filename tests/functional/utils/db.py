from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def insert_into_db(session: AsyncSession,
                         table_name: str,
                         fields: dict[str, any],
                         schema: str = 'public') -> None:
    field_names = fields.keys()
    field_list = ', '.join(field_names)
    val_list = ', '.join([f':{f_name}' for f_name in field_names])
    query = text(f'INSERT INTO {schema}.{table_name} ({field_list}) VALUES ({val_list});')
    await session.execute(query, fields)
    await session.commit()


async def delete_from_db(session: AsyncSession,
                         table_name: str,
                         eq_condition: tuple[str, any],
                         schema: str = 'public') -> None:
    cond_field_name, cond_field_val = eq_condition
    query = text(f'DELETE FROM {schema}.{table_name} WHERE {cond_field_name} = :{cond_field_name};')
    await session.execute(query, {cond_field_name: cond_field_val})
    await session.commit()
