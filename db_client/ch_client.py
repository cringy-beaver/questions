import sqlalchemy
from clickhouse_sqlalchemy import (
    make_session, get_declarative_base, types, engines
)
from aiochclient import ChClient
# import asyncpg
from sqlalchemy import MetaData, Column
from clickhouse_sqlalchemy import (
    Table, get_declarative_base, types, engines
)
import datetime


class DBClient:
    def __init__(self, host: str,
                 port: str, user: str,
                 password: str, db_name='default'):
        self.__uri = f"clickhouse://{user}:{password}@{host}:{port}/{db_name}"
        self.engine = sqlalchemy.create_engine(self.__uri)
        self.session = make_session(self.engine)
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.Base = get_declarative_base(metadata=self.metadata)

        class Question(self.Base):
            __tablename__ = 'questions'
            id = sqlalchemy.Column(types.Int32, primary_key=True)
            number = sqlalchemy.Column(types.Int32)
            title = sqlalchemy.Column(types.String)
            body = sqlalchemy.Column(types.String)
            created_at = sqlalchemy.Column(types.DateTime)
            link_to_s3_question_pic = sqlalchemy.Column(types.String)
            __table_args__ = (
                engines.MergeTree(),
            )

        self.Question = Question
        self.Base.metadata.create_all(self.engine)

    def add_question(self, question_data):
        new_question = self.Question(**question_data)
        self.session.add(new_question)
        self.session.commit()

    def get_questions_filter_by_date(self, date_filter=None):
        query = self.session.query(self.Question)
        if date_filter:
            query = query.filter(self.Question.created_at > date_filter)
        return query.all()

    def get_questions_filter_by_number(self, number_filter=None):
        query = self.session.query(self.Question)
        if number_filter:
            query = query.filter(self.Question.number == number_filter)
        return query.all()

    def get_questions_filter_by_id(self, id_filter=None):
        query = self.session.query(self.Question)
        if id_filter:
            query = query.filter(self.Question.id == id_filter)
        return query.all()

    def get_questions_filter_by_title(self, title_filter=None):
        query = self.session.query(self.Question)
        if title_filter:
            query = query.filter(self.Question.title == title_filter)
        return query.all()

    def get_questions_filter_by_body(self, body_filter=None):
        query = self.session.query(self.Question)
        if body_filter:
            query = query.filter(self.Question.body == body_filter)
        return query.all()

    def get_all_questions(self):
        return self.session.query(self.Question).all()

# # DBClient/client.py
# from aiochclient import ChClient
# import asyncpg
# from sqlalchemy import MetaData, Column
# from clickhouse_sqlalchemy import (
#     Table, get_declarative_base, types, engines
# )
# import datetime
#
# class DBClient:
#     def __init__(self, host: str,
#                  port: str, user: str,
#                  password: str, db_name='default'):
#         self.__uri = f"clickhouse://{user}:{password}@{host}:{port}/{db_name}"
#         self.metadata = MetaData()
#         self.Base = get_declarative_base(metadata=self.metadata)
#
#         class Question(self.Base):
#             __tablename__ = 'questions'
#             id = Column(types.Int32, primary_key=True)
#             number = Column(types.Int32)
#             title = Column(types.String)
#             body = Column(types.String)
#             created_at = Column(types.DateTime)
#             link_to_s3_question_pic = Column(types.String)
#             __table_args__ = (
#                 engines.Memory(),
#             )
#
#         self.Question = Question
#
#     async def create_table(self):
#         async with ChClient(self.__uri) as client:
#             await client.execute(f"CREATE TABLE IF NOT EXISTS {self.Question.__tablename__} "
#                                   f"(id Int32, number Int32, title String, body String, "
#                                   f"created_at DateTime, link_to_s3_question_pic String) ENGINE = Memory")
#
#     async def add_question(self, question_data):
#         async with ChClient(self.__uri) as client:
#             await client.execute(f"INSERT INTO {self.Question.__tablename__} "
#                                   f"(id, number, title, body, created_at, link_to_s3_question_pic) VALUES",
#                                   [tuple(question_data.values())])
#
#     async def get_questions_filter_by_title(self, title_filter=None):
#         async with ChClient(self.__uri) as client:
#             query = f"SELECT * FROM {self.Question.__tablename__}"
#             if title_filter:
#                 query += f" WHERE title = '{title_filter}'"
#             result = await client.fetch(query)
#         return [dict(zip(['id', 'number', 'title', 'body', 'created_at', 'link_to_s3_question_pic'], row)) for row in result]
