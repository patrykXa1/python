from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Players(Base):
    __tablename__ = 'players'

    id = Column(INTEGER, primary_key=True)
    nick = Column(VARCHAR)
    e_mail = Column(VARCHAR)

    def __init__(self, nick, e_mail):
        """Creates columns nick and e_mail"""
        self.nick = nick
        self.e_mail = e_mail


class Scores(Base):
    __tablename__ = 'scores'

    id = Column(INTEGER, primary_key=True)
    id_player = Column(INTEGER, ForeignKey('players.id'))
    score = Column(INTEGER)

    def __init__(self, id_player, score):
        """Creates columns id_player and score"""
        self.id_player = id_player
        self.score = score


engine = create_engine("postgresql://student8:st2021%8@212.182.24.105:15432/student8")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

if __name__ == "__main__":
    session = Session()
    # session.add(Players("gracz1","ahdsf@gmail.com"))
    for player in session.query(Players).all():
        print(player.id,player.nick,player.e_mail)

    for score in session.query(Scores).all():
        print(score.id,score.id_player,score.score)
        session = Session()

    session.commit()
    session.close()
