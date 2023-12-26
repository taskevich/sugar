from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, JSON, func
from sqlalchemy import create_engine, CheckConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, Session, validates, relationship

CONN_STRING = "postgresql://postgres:joDcjToeAX@45.12.238.117:5432/taskevin_sugar"
engine = create_engine(CONN_STRING)
Base = declarative_base()
metadata = Base.metadata


class Utils:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Horror(Base, Utils):
    __tablename__ = "horrors"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column("name", String(32), nullable=False, unique=True)


class Hard(Base, Utils):
    __tablename__ = "hards"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), nullable=False, unique=True)


class Users(Base, Utils):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Quests(Base, Utils):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    slug = Column(String(64), nullable=False)
    my_erp_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)
    legend = Column(Text, nullable=False, default="Здесь должна быть ваша легенда")
    files = Column(JSON)
    price = Column(Integer, nullable=False, default=0)
    min_players = Column(Integer, default=2, nullable=False)
    max_players = Column(Integer, default=6, nullable=False)
    count_actors = Column(Integer, default=1, nullable=False)
    hard_id = Column(Integer, ForeignKey(Hard.id), nullable=False)
    horror_id = Column(Integer, ForeignKey(Horror.id), nullable=False)
    play_time = Column(Integer, default=60, nullable=False)
    is_hide = Column(Boolean, nullable=False, default=False)
    age_limit = Column(Integer, default=18)


class Visitors(Base, Utils):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    email = Column(String(64))
    phone = Column(String(16), nullable=False)
    age = Column(Integer, CheckConstraint("age > 0 AND age < 100"), default=18)

    orders = relationship("Orders", back_populates="visitor")

    @validates('age')
    def validate_age(self, key, value):
        if not 0 < value < 100:
            raise ValueError(f'Invalid age {value}')
        return value


class Orders(Base, Utils):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    visitor_id = Column(Integer, ForeignKey(Visitors.id), nullable=False)
    quest_id = Column(Integer, ForeignKey(Quests.id), nullable=False)
    pick_hard = Column(Integer, ForeignKey(Hard.id), nullable=False)
    pick_horror = Column(Integer, ForeignKey(Horror.id), nullable=False)
    pick_players = Column(Integer, default=1, nullable=False)
    pick_actors = Column(Integer, default=1, nullable=False)
    pick_date_id = Column(ForeignKey("schedules.id"), nullable=False)
    visitor = relationship("Visitors", back_populates="orders")


class Services(Base, Utils):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    text = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    quest_id = Column(Integer, ForeignKey(Quests.id), nullable=True)


class OrderToService(Base):
    __tablename__ = "order_to_service"

    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey(Orders.id), nullable=False)
    service_id = Column(Integer, ForeignKey(Services.id), nullable=False)


class Schedules(Base, Utils):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, nullable=False)
    quest_id = Column(Integer, ForeignKey(Quests.id), nullable=True)
    date = Column(DateTime, nullable=False, server_default=func.now())
    is_busy = Column(Boolean, default=False)
    parent = relationship(Quests, cascade="all,delete", backref="schedule")


class Reviews(Base, Utils):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, nullable=False)
    visitor = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    stars = Column(Integer, default=5)
    quest_id = Column(Integer, ForeignKey(Quests.id), nullable=False)


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, nullable=False)
    quest_id = Column(Integer, ForeignKey(Quests.id), nullable=True)
    photo = Column(Text, nullable=True)
    is_main = Column(Boolean, default=False)


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine, tables=[Hard.__table__, Horror.__table__])
Base.metadata.create_all(engine, tables=[Users.__table__, Quests.__table__, Visitors.__table__, Services.__table__,
                                         Orders.__table__, OrderToService.__table__, Schedules.__table__,
                                         Reviews.__table__, Gallery.__table__])
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def SessionManager() -> Session:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
