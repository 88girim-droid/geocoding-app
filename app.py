import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="주소 → 위도/경도 변환기", page_icon="📍", layout="centered")
st.title("📍 주소 → 위도/경도 변환기")
st.caption("A열에 주소를 입력하면 Google Geocoding API로 B열(위도), C열(경도)이 자동으로 채워집니다.")

API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
if not API_KEY:
    st.error(
        "GOOGLE_API_KEY가 설정되어 있지 않습니다. "
        "Streamlit Cloud의 App settings → Secrets에 `GOOGLE_API_KEY = \"...\"` 를 추가해주세요."
    )
    st.stop()

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        {"주소": [""] * 10, "위도": [None] * 10, "경도": [None] * 10}
    )

@st.cache_data(show_spinner=False)
def _geocode_cached(address: str, api_key: str):
    resp = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json",
        params={"address": address, "key": api_key},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") == "OK" and data.get("results"):
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"], None
    return None, None, data.get("status", "UNKNOWN_ERROR")


uploaded = st.file_uploader("CSV 업로드 (선택, '주소' 열 필요)", type=["csv"])
if uploaded is not None:
    new_df = pd.read_csv(uploaded)
    if "주소" not in new_df.columns:
        st.error("CSV에 '주소' 열이 없습니다.")
    else:
        for col in ["위도", "경도"]:
            if col not in new_df.columns:
                new_df[col] = None
        st.session_state.df = new_df[["주소", "위도", "경도"]]
        st.rerun()

edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    disabled=["위도", "경도"],
    use_container_width=True,
    key="editor",
)

errors = []
changed = False
for i, row in edited_df.iterrows():
    address = str(row["주소"]).strip() if pd.notna(row["주소"]) else ""
    has_coords = pd.notna(row["위도"]) and pd.notna(row["경도"])

    if address and not has_coords:
        lat, lng, err = _geocode_cached(address, API_KEY)
        edited_df.at[i, "위도"] = lat
        edited_df.at[i, "경도"] = lng
        if err:
            errors.append(f"'{address}': {err}")
        changed = True
    elif not address and has_coords:
        edited_df.at[i, "위도"] = None
        edited_df.at[i, "경도"] = None
        changed = True

st.session_state.df = edited_df

for e in errors:
    st.warning(f"지오코딩 실패 - {e}")

if changed:
    st.rerun()

st.download_button(
    "CSV 다운로드",
    edited_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="geocoded.csv",
    mime="text/csv",
)
