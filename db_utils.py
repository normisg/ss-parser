from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_PATH
import dateutil.parser

Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    published = Column(Integer)  # Store as Unix timestamp (seconds since epoch)
    is_processed = Column(Boolean, default=False)
    is_match = Column(Boolean, default=None)
    location = Column(String, default=None)
    building_type = Column(String, default=None)
    rooms = Column(Integer, default=None)
    floor = Column(Integer, default=None)
    area = Column(Float, default=None)
    price = Column(Integer, default=None)
    price_m2 = Column(Float, default=None)
    street = Column(String, default=None)

engine = create_engine(DATABASE_PATH)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_entries_to_db(entries):
    session = Session()
    for entry in entries:
        exists = session.query(Entry).filter_by(link=entry.get('link')).first()
        if not exists:
            published_val = entry.get('published')
            published_ts = None
            if published_val:
                try:
                    dt = dateutil.parser.parse(published_val)
                    published_ts = int(dt.timestamp())
                except Exception:
                    published_ts = None
            db_entry = Entry(
                title=entry.get('title'),
                link=entry.get('link'),
                published=published_ts,
                is_processed=False,
                location=entry.get('location'),
                building_type=entry.get('building_type'),
                rooms=entry.get('rooms'),
                floor=entry.get('floor'),
                area=entry.get('area'),
                price=entry.get('price'),
                price_m2=entry.get('price_m2'),
                street=entry.get('street')
            )
            session.add(db_entry)
    session.commit()
    session.close()
