import os

from dotenv import load_dotenv
# app/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_user = os.getenv("db_user")
db_password = os.getenv("db_password")



DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@localhost:3306/llmagent?charset=utf8mb4"

engine = create_engine(
  DATABASE_URL,
  echo=False,      # 디버깅용으로 보고 싶으면 True
  pool_size=5,
  max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
  """
  FastAPI dependency로 사용할 데이터베이스 세션을 생성하고 반환.
  요청이 끝나면 자동으로 세션을 닫음.
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()





def release_conn(conn):
  """
  기존에는 pool.release_connection(conn)을 호출했지만,
  이제는 SQLAlchemy Session을 닫기만 하면 됨.
  """
  conn.close()
