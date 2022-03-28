import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


class City(SqlAlchemyBase):
    __tablename__ = 'cities'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    city = sa.Column(sa.String, nullable=True)


class Train(SqlAlchemyBase):
    __tablename__ = 'trains'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    chief = sa.Column(sa.String, nullable=True)


class Timetable(SqlAlchemyBase):
    __tablename__ = 'timetable'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    departure = sa.Column(sa.DateTime)
    train_id = sa.Column(sa.Integer, sa.ForeignKey("trains.id"))
    train = orm.relation('Train')
    city_id = sa.Column(sa.Integer, sa.ForeignKey("cities.id"))
    city = orm.relation('City')


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    global Timetable

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


class AlmostHome:
    def __init__(self, db_file):
        global_init(db_file)
        self.sess = create_session()


ah = AlmostHome("schedule.db")
