from sqlalchemy import create_engine, Column, MetaData

from clickhouse_sqlalchemy import (
    Table, make_session, get_declarative_base, types, engines
)
import datetime

uri = 'clickhouse://master:content344DB@185.154.194.183:8123/default'
engine = create_engine(uri)
session = make_session(engine)
metadata = MetaData(bind=engine)
Base = get_declarative_base(metadata=metadata)


class Question(Base):
    __tablename__ = 'questions'
    id = Column(types.Int32, primary_key=True)
    number = Column(types.Int32)
    title = Column(types.String)
    body = Column(types.String)
    created_at = Column(types.DateTime)
    link_to_s3_question_pic = Column(types.String)
    __table_args__ = (
        engines.Memory(),
    )


Question.__table__.create(engine)

new_question = Question(id=1, title='How to use SQLAlchemy ORM?',
                        body='I want to use SQLAlchemy ORM in my project, '
                                'but I don\'t know how to start.',
                        created_at=datetime.datetime(2023, 6, 5),
                        link_to_s3_question_pic='https://i.imgur.com/4jYk1B2.png')
session.add(new_question)
session.commit()

#####
questions = session.query(Question).filter(Question.created_at
                                           > datetime.datetime(2011, 1, 1))\
    .all()

for question in questions:
    print(f"{question.id}: {question.title} ({question.body})" +
          "created at: " + str(question.created_at))
