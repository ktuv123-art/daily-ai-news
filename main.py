import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from zoneinfo import ZoneInfo

from openai import OpenAI


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def create_news_digest() -> str:
    today = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")
    client = OpenAI(api_key=required_env("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
        tools=[{"type": "web_search"}],
        tool_choice="required",
        input=f"""
오늘은 한국시간 {today}이다. 현재 웹을 검색해 가장 최신이며 중요한 AI 뉴스 5개를 골라라.

요구사항:
- 서로 다른 사건만 선정하고 오래된 소식이나 단순 재게시 기사는 제외한다.
- 가능하면 기업·기관의 공식 발표를 우선하고, 보도 날짜와 사건 발생 날짜를 구분한다.
- 한국어로 작성한다.
- 각 항목은 제목, 날짜, 핵심 요약 2~3문장, 클릭 가능한 원문 URL을 포함한다.
- 링크는 반드시 실제 원문 URL을 그대로 표시한다.
- 이메일에 바로 넣을 수 있는 간결한 HTML만 출력한다. 마크다운 코드 펜스는 쓰지 않는다.
""".strip(),
    )
    return response.output_text


def send_email(body_html: str) -> None:
    sender = required_env("GMAIL_ADDRESS")
    recipient = os.getenv("RECIPIENT_EMAIL", sender)
    app_password = required_env("GMAIL_APP_PASSWORD")
    today = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")

    message = EmailMessage()
    message["Subject"] = f"{today} 오늘의 AI 뉴스 5선"
    message["From"] = sender
    message["To"] = recipient
    message.set_content("HTML을 지원하는 이메일 앱에서 확인해 주세요.")
    message.add_alternative(
        f"<html><body><h1>오늘의 AI 뉴스 5선</h1>{body_html}</body></html>",
        subtype="html",
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(message)


if __name__ == "__main__":
    digest = create_news_digest()
    if not digest.strip():
        raise RuntimeError("The generated digest was empty")
    send_email(digest)

