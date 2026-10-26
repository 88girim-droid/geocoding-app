# 주소 → 위도/경도 변환기

Streamlit 앱. 표의 A열("주소")에 주소를 입력하면 Google Geocoding API로 B열(위도), C열(경도)이 자동으로 채워집니다.

## 로컬 실행

```bash
pip install -r requirements.txt
```

`.streamlit/secrets.toml` 파일을 만들고 (이 파일은 git에 올라가지 않습니다):

```toml
GOOGLE_API_KEY = "본인의 Google Geocoding API 키"
```

실행:

```bash
streamlit run app.py
```

## Streamlit Community Cloud 배포

1. 이 저장소를 GitHub에 올린 뒤 [share.streamlit.io](https://share.streamlit.io) 에서 New app으로 연결합니다.
2. Main file path는 `app.py`로 지정합니다.
3. 앱의 **Settings → Secrets** 에 아래 내용을 추가합니다.

```toml
GOOGLE_API_KEY = "본인의 Google Geocoding API 키"
```

4. Save 후 앱이 재시작되면 바로 사용할 수 있습니다.

## 사용법

- 표의 "주소" 열에 주소를 입력하면 자동으로 위도/경도가 채워집니다.
- CSV를 업로드해 여러 주소를 한번에 처리할 수 있습니다 ('주소' 열 필요).
- 결과는 "CSV 다운로드" 버튼으로 내려받을 수 있습니다.
