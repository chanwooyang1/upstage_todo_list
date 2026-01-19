import httpx
from loguru import logger


async def compare_responses():
    async with httpx.AsyncClient() as client:
        # 1. JSON 응답을 주는 곳 (예: Upstage API 엔드포인트 또는 일반 API)
        # 여기서는 설명을 위해 업스테이지 홈페이지와 일반 JSON API를 예로 듭니다.

        # Case A: JSON 응답 (API 호출)
        res_json = await client.get("https://jsonplaceholder.typicode.com/todos")

        logger.info("--- [CASE A: JSON Response] ---")
        logger.info(f"MIME Type (Content-Type): {res_json.headers.get('Content-Type')}")
        logger.info(f"Status Code: {res_json.status_code}")
        logger.info(f'Status Message: {res_json.json()["message"]}')
        logger.info(f"Body Preview: {res_json.text[:50]}...")

        # Case B: HTML 응답 (웹 페이지 호출)
        res_html = await client.get("https://www.upstage.ai/")
        logger.info("--- [CASE B: HTML Response] ---")
        logger.info(f"MIME Type (Content-Type): {res_html.headers.get('Content-Type')}")
        logger.info(f"Status Code: {res_html.status_code}")
        logger.info(f'Status Message: {res_html.json()["message"]}')
        logger.info(f"Body Preview: {res_html.text[:50]}...")


# 실행
import asyncio

asyncio.run(compare_responses())