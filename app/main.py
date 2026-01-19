from logging import INFO

from fastapi import FastAPI, Request, HTTPException
import mysql.connector
import os
import logging
from logging.handlers import RotatingFileHandler

# ---------------------------
# [TASK 1] 로그 저장 폴더 생성
# ---------------------------
# TODO: "logs"라는 이름의 폴더를 생성해주세요!
# Hint: os.makedirs()를 활용하면 됩니다. 이미 폴더가 있어도 에러가 나지 않도록 exist_ok=True 옵션 사용
log_dir = "logs"
log_fname = "app.log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir,exist_ok=True)


# ---------------------------
# [TASK 2] 로그 포맷 및 핸들러 설정
# ---------------------------
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# TODO: LOG_FORMAT을 사용하여 formatter를 생성하세요
# Hint: logging.Formatter()를 사용하여 LOG_FORMAT을 전달
formatter = logging.Formatter(LOG_FORMAT) # 이 부분을 채워주세요!

file_handler = RotatingFileHandler(
    # TODO: 로그 파일 경로를 지정하세요 (logs 폴더 안에 app.log 파일)
    # Hint: "logs/파일명.확장자" 형식으로 작성
    filename=os.path.join(log_dir, log_fname),  # 이 부분을 채워주세요!

    # TODO: 로그 파일의 최대 크기를 바이트 단위로 지정하세요
    # Hint: 1MB = 1024 * 1024 바이트
    maxBytes=1024,  # 이 부분을 채워주세요!

    # TODO: 보관할 백업 파일 개수를 지정하세요
    # Hint: 5개의 백업 파일을 유지하려면?
    backupCount=5,  # 이 부분을 채워주세요!

    encoding="utf-8"
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# ---------------------------
# [TASK 3] 루트 로거 통합 설정
# ---------------------------
root_logger = logging.getLogger()

# TODO: 로그 레벨을 INFO로 설정하세요
# Hint: logging 모듈의 INFO 상수를 사용하세요
root_logger.setLevel(INFO)  # 이 부분을 채워주세요!

# TODO: 파일 핸들러를 루트 로거에 추가하세요
# Hint: addHandler() 메서드를 사용하여 file_handler를 추가
root_logger.addHandler(file_handler)

# TODO: 콘솔 핸들러를 루트 로거에 추가하세요
# Hint: addHandler() 메서드를 사용하여 console_handler를 추가
root_logger.addHandler(file_handler)

logging.getLogger("uvicorn").handlers = root_logger.handlers
logging.getLogger("uvicorn.access").handlers = root_logger.handlers

app = FastAPI()

import time
from fastapi import Request
from loguru import logger

@app.middleware("http")
async def log_response_details(request: Request, call_next):
    # 1. 요청 처리 시작 시간 기록
    start_time = time.time()

    # 2. 다음 단계(핸들러)로 요청을 전달하고 응답(response)을 받음
    response = await call_next(request)

    # 3. 소요 시간 계산
    process_time = (time.time() - start_time) * 1000  # ms 단위

    # 4. 주요 응답 헤더 추출
    content_type = response.headers.get("content-type")
    content_length = response.headers.get("content-length")

    # 5. Loguru로 기록
    # 상태 코드에 따라 로그 레벨을 다르게 하면 더 좋습니다.
    log_msg = (
        f"RES | Status: {response.status_code} | "
        f"Type: {content_type} | "
        f"Length: {content_length} bytes | "
        f"Duration: {process_time:.2f}ms"
    )

    if response.status_code >= 400:
        logger.error(log_msg)
    else:
        logger.info(log_msg)

    return response

def get_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="tester",
        password="tester",
        database="llmagent"
    )


# ---------------------------
# CREATE
# ---------------------------
@app.post("/todos")
async def create_todo(request: Request):
    logging.info("할 일 목록 생성 요청")
    method = request.method
    url = str(request.url)
    path = request.url.path

    # 2. 주요 헤더 정보
    headers = request.headers
    host = headers.get("host")
    user_agent = headers.get("user-agent")
    content_type = headers.get("content-type")
    auth = headers.get("authorization")  # 보안상 일부만 찍거나 존재 여부만 확인하는 것이 좋습니다.

    # 3. 쿼리 파라미터 (예: /todos?priority=high&sort=desc)
    query_params = dict(request.query_params)

    # 4. 구조화된 로깅
    # logger.info(f" [NEW REQUEST] {method} {path}")
    # logger.info(f" URL: {url}")
    # logger.info(
    #     f" Headers | Host: {host} | UA: {user_agent} | CT: {content_type} | Auth: {'Present' if auth else 'None'}")
    # logger.info(f" Query Params: {query_params}")

    body = await request.json()
    content = body.get("content")


    if not content:
        logging.error("제목이 없는 할 일 생성 시도: content missing")

        raise HTTPException(status_code=400, detail="content is required")

    conn = get_db()
    cursor = conn.cursor()

    # 👉 학생이 작성해야 하는 SQL
    # INSERT 문 작성
    # 예: INSERT INTO todo (content) VALUES (%s)
    cursor.execute(
        ### TODO: 여기에 INSERT SQL 작성 ###
        """
        INSERT INTO todo (content) VALUES (%s)
        """
        ,
        (content,)
    )
    conn.commit()

    todo_id = cursor.lastrowid
    logging.info(f"새로운 할 일 생성 완료: ID {todo_id}")

    # 👉 학생이 작성해야 하는 SQL
    # SELECT 문 작성하여 방금 만든 todo 조회
    cursor.execute(
        ### TODO: 여기에 SELECT SQL 작성 ###
        """
        SELECT id, content, created_at
        FROM todo
        WHERE id = %s
        """
        ,
        (todo_id,)
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "content": row[1],
        "created_at": str(row[2])
    }


# ---------------------------
# READ
# ---------------------------
@app.get("/todos")
def get_todos():
    logging.info("할 일 목록 조회 요청")
    conn = get_db()
    cursor = conn.cursor()

    # 👉 학생이 작성해야 하는 SQL
    # 전체 todo 조회 SELECT 문 작성
    cursor.execute(
        ### TODO: 여기에 전체 조회 SELECT SQL 작성 ###
        """
        SELECT id, content, created_at 
        FROM todo
        ORDER BY id DESC
        """
    )
    rows = cursor.fetchall()
    logging.info("할 일 목록 조회 완료")
    cursor.close()
    conn.close()

    return [
        {
            "id": r[0],
            "content": r[1],
            "created_at": str(r[2])
        }
        for r in rows
    ]


# ---------------------------
# DELETE
# ---------------------------
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    logging.info("특정 할 일 목록 삭제 요청")
    conn = get_db()
    cursor = conn.cursor()

    # 👉 학생이 작성해야 하는 SQL
    # 삭제 DELETE 문 작성
    cursor.execute(
        ### TODO: 여기에 DELETE SQL 작성 ###
        """
        DELETE FROM todo WHERE id = %s
        
        """
        ,
        (todo_id,)
    )
    conn.commit()

    affected = cursor.rowcount

    cursor.close()
    conn.close()
    logging.info("할 일 목록 삭제 완료")
    if affected == 0:
        logging.error(f"{todo_id}, 할 일이 존재하지 않습니다")
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted"}

