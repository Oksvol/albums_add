import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def save_album(album_data):
    """
    Сохраняет данные об альбоме в базу данных
    """
    session = connect_db()
    
    artist = album_data['artist'];
    album  = album_data['album'];
    
    # Проверка в базе данных на предмет наличия исполнителя в базе
    album_exists = session.query(Album).filter(Album.artist == artist, Album.album == album).all()
    if album_exists:
        print("Такой альбом уже есть")
        return False
    else:
        # Если нет альбома, добавляем
        year   = album_data['year'];
        genre  = album_data['genre'];
        # Если год не указан, пропускаем
        if type(year) == None: pass
        # Проверяем правильно ли передали нам год
        else:
            try:
                if int(year) > dt.datetime.now().year:
                    raise ValueError("Этот альбом только будет написан) Сейчас только ", dt.datetime.now().year, " год. Очнись, Док!:)")
            except ValueError:
                raise ValueError("Неверно указан год выпуска альбома")
        
        new_album = Album(artist=artist, year=year, genre=genre,\
                           album=album)
        session.add(new_album)
        session.commit()
        return True


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

