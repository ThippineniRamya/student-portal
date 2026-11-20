from sqlalchemy import create_engine
from sqlalchemy.orm import session,sessionmaker,declarative_base,base
engine=create_engine("sqlite:///./student.db")

SessionLocal=sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False

)
Base=declarative_base()
def getdb():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()
