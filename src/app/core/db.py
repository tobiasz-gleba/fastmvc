from typing import Optional

import projects.users.schema

from sqlmodel import SQLModel, create_engine, Session, select


sqlite_url = f"postgresql://postgres:postgres@postgres:5432/database"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)


class Query():

    def __init__(self, statement):
        self.statement = statement

    async def result(self):
        result_list = []
        with Session(engine) as session:
            query_result = session.exec(self.statement)
            for result in query_result:
                result_list.append(result)

        return result_list

class Command():
    
    def _add(self, sqlmodel_object):
        with Session(engine) as session:
            session.add(sqlmodel_object)
            session.commit()
            session.refresh(sqlmodel_object)
        return sqlmodel_object

    async def insert(self, sqlmodel_object):
        return self._add(sqlmodel_object)

    async def update(self, sqlmodel_object):
        return self._add(sqlmodel_object)

    async def delete(self, sqlmodel_object):
        with Session(engine) as session:
            session.delete(sqlmodel_object)
            session.commit()
            session.refresh(sqlmodel_object)
        return sqlmodel_object