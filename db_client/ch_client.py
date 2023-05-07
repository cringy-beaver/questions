import httpx
from sqlalchemy import MetaData, Column
from clickhouse_sqlalchemy import get_declarative_base, types, engines


def dumpt(response_plain_text: str) -> list[dict]:
    """Dump raw input to dict, using tab as delimiter"""
    rows = response_plain_text.strip().split('\n')
    columns = ['id', 'number',
               'title', 'body',
               'created_at', 'link_to_s3_question_pic']
    result = [dict(zip(columns, row.split('\t'))) for row in rows]

    return result


class DBClient:
    def __init__(self, host: str,
                 port: str, user: str,
                 password: str):
        self.metadata = MetaData()
        self.Base = get_declarative_base(metadata=self.metadata)

        self.__uri = f"http://{host}:{port}/"
        self.__auth = (user, password)

        class Question(self.Base):
            __tablename__ = 'questions'
            id = Column(types.Int32, primary_key=True)
            number = Column(types.Int32)
            title = Column(types.String)
            body = Column(types.String)
            created_at = Column(types.DateTime)
            link_to_s3_question_pic = Column(types.String, nullable=True)
            __table_args__ = (
                engines.MergeTree(),
            )

        self.Question = Question

    async def create_table(self):
        query: str | None = f"CREATE TABLE IF NOT EXISTS " \
                            f"{self.Question.__tablename__} " \
                f"(id Int32, number Int32, title String, body String, " \
                f"created_at DateTime, link_to_s3_question_pic String) " \
                f"ENGINE = Memory"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)
        return response.text

    async def insert_question(self, question):
        query: str | None = f"INSERT INTO {self.Question.__tablename__} " \
                f"(id, number, title, body, " \
                f"created_at, link_to_s3_question_pic) " \
                f"VALUES ({question['id']}, {question['number']}, " \
                f"'{question['title']}', " \
                f"'{question['body']}', '{question['created_at']}', " \
                f"'{question['link_to_s3_question_pic']}')"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)
        return response.text

    async def get_questions_filter_by_title(self, title_filter=None):
        query: str | None = f"SELECT * FROM {self.Question.__tablename__}"
        if title_filter:
            query += f" WHERE title = '{title_filter}'"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)

        return dumpt(response.text) if response.text else []

    async def get_questions_filter_by_date(self, date_filter=None):
        query: str | None = f"SELECT * FROM {self.Question.__tablename__}"
        if date_filter:
            query += f" WHERE created_at = '{date_filter}'"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)

        return dumpt(response.text) if response.text else []

    async def get_questions_filter_by_number(self, number_filter=None):
        query: str | None = f"SELECT * FROM {self.Question.__tablename__}"
        if number_filter:
            query += f" WHERE number = '{number_filter}'"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)

        return dumpt(response.text) if response.text else []

    async def get_questions_filter_by_id(self, id_filter=None) -> list[dict]:
        query: str | None = f"SELECT * FROM {self.Question.__tablename__}"
        if id_filter:
            query += f" WHERE id = '{id_filter}'"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)

        return dumpt(response.text) if response.text else []

    async def get_questions_filter_by_body(self, body_filter=None) \
            -> list[dict]:
        query: str | None = f"SELECT * FROM {self.Question.__tablename__}"
        if body_filter:
            query += f" WHERE body = '{body_filter}'"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)

        return dumpt(response.text) if response.text else []

    async def get_all_questions(self):
        query: str | None = f"SELECT * FROM {self.Question.__tablename__}"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)

        return dumpt(response.text) if response.text else []

    async def update_question(self, question_id, question):
        query: str | None = f"ALTER TABLE {self.Question.__tablename__} " \
                            f"UPDATE " \
                f"number = {question['number']}, " \
                f"title = '{question['title']}', " \
                f"body = '{question['body']}', " \
                f"created_at = '{question['created_at']}', " \
                f"link_to_s3_question_pic = " \
                f"'{question['link_to_s3_question_pic']}' " \
                f"WHERE id = {question_id}"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)

        return dumpt(response.text) if response.text else response.status_code

    async def delete_question(self, question_id):
        query: str | None = f"ALTER TABLE {self.Question.__tablename__} " \
                f"DELETE WHERE id = {question_id}"
        async with httpx.AsyncClient() as client:
            response = await client.post(self.__uri, data=query,
                                         auth=self.__auth)

        return dumpt(response.text) if response.text else response.status_code
