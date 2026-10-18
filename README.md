# Daily AI News

매일 한국시간 오전 8시에 최신 AI 뉴스 5개를 검색·요약하여 Gmail로 보내는 GitHub Actions 프로젝트입니다.

## 설정

저장소의 **Settings → Secrets and variables → Actions**에서 다음 Repository secrets를 추가하세요.

- `OPENAI_API_KEY`: OpenAI API 키
- `GMAIL_ADDRESS`: 발신할 Gmail 주소
- `GMAIL_APP_PASSWORD`: 해당 계정의 Google 앱 비밀번호(일반 로그인 비밀번호가 아님)
- `RECIPIENT_EMAIL`: 뉴스를 받을 이메일 주소

Google 앱 비밀번호를 사용하려면 Google 계정에서 2단계 인증을 활성화해야 합니다. 조직 정책에 따라 앱 비밀번호를 사용할 수 없는 계정도 있습니다.

## 실행

- 자동 실행: 매일 `23:00 UTC` (`08:00 Asia/Seoul`)
- 수동 실행: GitHub의 **Actions → Send daily AI news → Run workflow**

GitHub Actions의 예약 실행은 서버 상황에 따라 몇 분 정도 늦어질 수 있습니다.

## 로컬 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="..."
export GMAIL_ADDRESS="..."
export GMAIL_APP_PASSWORD="..."
export RECIPIENT_EMAIL="받을 이메일 주소"
python main.py
```

비밀값은 저장소나 `.env` 파일에 커밋하지 마세요.
