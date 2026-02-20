import streamlit as st
import requests
import pandas as pd
from streamlit_js_eval import get_geolocation

# API 키 (보안 규칙 준수)
API_KEY = st.secrets["WEATHER_API_KEY"]

# 페이지 설정
st.set_page_config(page_title="🌍 Global Weather App", layout="centered")

st.title("🌤️ Global Weather App")
st.write("WeatherAPI.com 데이터를 활용한 전 세계 날씨 앱")

# 한글 → 영어 도시명 매핑 테이블
city_map = {
    "서울": "Seoul",
    "부산": "Busan",
    "아산": "Asan",
    "동탄": "Dongtan",
    "인천": "Incheon",
    "대구": "Daegu",
    "대전": "Daejeon",
    "광주": "Gwangju",
    "울산": "Ulsan",
    "제주": "Jeju",
    "도쿄": "Tokyo",
    "오사카": "Osaka",
    "뉴욕": "New York",
    "런던": "London",
    "파리": "Paris",
    "베를린": "Berlin",
    "시드니": "Sydney",
}

# 사용자 입력 (한글/영어 지원)
city = st.text_input("도시 이름을 입력하세요 (한글/영어)", "서울")

# GPS 버튼
if st.button("📍 내 위치(GPS)로 검색"):
    loc = get_geolocation()
    if loc:
        lat, lon = loc["coords"]["latitude"], loc["coords"]["longitude"]
        query = f"{lat},{lon}"
    else:
        query = city_map.get(city, city)
else:
    query = city_map.get(city, city)

# WeatherAPI 호출
url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={query}&days=1&aqi=no&alerts=no"
response = requests.get(url)
data = response.json()

# 에러 처리: location 키가 없을 경우 안내 메시지 출력
if "error" in data:
    st.error("❌ 해당 도시를 찾을 수 없습니다. 영어 이름을 입력하거나 다른 도시를 시도해보세요.")
else:
    # 데이터 추출
    location = data["location"]["name"]
    country = data["location"]["country"]
    current = data["current"]
    forecast = data["forecast"]["forecastday"][0]["astro"]

    temp = current["temp_c"]
    condition = current["condition"]["text"]
    humidity = current["humidity"]
    feelslike = current["feelslike_c"]
    uv = current["uv"]
    moon_phase = forecast["moon_phase"]

    # 날씨 상태별 이모지 & 색상
    emoji_map = {
        "Sunny": "☀️",
        "Clear": "☀️",
        "Partly cloudy": "⛅",
        "Cloudy": "☁️",
        "Rain": "☔",
        "Snow": "☃️",
        "Thunderstorm": "⚡",
    }
    emoji = emoji_map.get(condition, "🌍")

    bg_color = "#f0f8ff" if "Sunny" in condition or "Clear" in condition else "#d3d3d3"
    st.markdown(
        f"<div style='background-color:{bg_color};padding:20px;border-radius:10px;'>"
        f"<h2>{emoji} {location}, {country}</h2>"
        f"<h3>{temp}°C | {condition}</h3>"
        "</div>",
        unsafe_allow_html=True,
    )

    # 추가 정보 박스
    st.subheader("📊 상세 정보")
    st.info(
        f"""
        - 습도: {humidity}%
        - 체감온도: {feelslike}°C
        - 자외선 지수: {uv}
        - 오늘 밤 달의 모양: {moon_phase}
        """
    )

    # 온도 기반 메시지
    if temp >= 35:
        st.warning("🥵 극도로 덥습니다! 외출은 자제하세요.")
    elif temp >= 30:
        st.warning("🔥 더운 날씨! 시원한 실내 운동을 추천합니다.")
    elif temp >= 20:
        st.success("😊 따뜻하고 활동하기 좋은 날씨예요!")
    elif temp >= 10:
        st.info("🌤️ 선선한 날씨, 가벼운 외출에 좋아요.")
    elif temp >= 0:
        st.warning("❄️ 쌀쌀합니다. 따뜻하게 입으세요.")
    else:
        st.error("🥶 매우 추운 날씨! 외출 시 방한 필수입니다.")

    # 운동 추천 (세밀화)
    st.subheader("🏋️ 운동 추천")
    if temp >= 35:
        st.write("실내 운동: 요가, 필라테스, 홈트레이닝")
        st.write("야외 운동: ❌ 외출 자제")
    elif temp >= 30:
        st.write("실내 운동: 실내 자전거, 스트레칭")
        st.write("야외 운동: 이른 아침 산책")
    elif temp >= 25:
        st.write("실내 운동: 근력 운동, 홈트레이닝")
        st.write("야외 운동: 저녁 조깅, 자전거 타기")
    elif temp >= 20:
        st.write("실내 운동: 스트레칭, 필라테스")
        st.write("야외 운동: 등산, 테니스")
    elif temp >= 15:
        st.write("실내 운동: 웨이트 트레이닝")
        st.write("야외 운동: 조깅, 축구")
    elif temp >= 10:
        st.write("실내 운동: 실내 자전거")
        st.write("야외 운동: 가벼운 산책")
    elif temp >= 5:
        st.write("실내 운동: 요가, 스트레칭")
        st.write("야외 운동: 짧은 산책")
    elif temp >= 0:
        st.write("실내 운동: 홈트레이닝")
        st.write("야외 운동: ❄️ 방한 준비 후 등산")
    else:
        st.write("실내 운동: 실내 자전거, 요가")
        st.write("야외 운동: ❌ 외출 자제")

    # 옷 코디 추천
    st.subheader("👕 오늘의 옷 코디 추천")
    if temp >= 35:
        st.write("👕 민소매, 🩳 반바지, 🕶️ 선글라스")
    elif temp >= 30:
        st.write("👕 반팔 티셔츠, 🩳 반바지")
    elif temp >= 25:
        st.write("👕 반팔, 👖 얇은 바지")
    elif temp >= 20:
        st.write("👕 얇은 긴팔, 👖 청바지")
    elif temp >= 15:
        st.write("🧥 가벼운 자켓, 👖 긴바지")
    elif temp >= 10:
        st.write("🧥 두꺼운 자켓, 🧣 목도리")
    elif temp >= 5:
        st.write("🧥 코트, 🧤 장갑")
    elif temp >= 0:
        st.write("🧥 패딩, 🧣 목도리, 🧤 장갑")
    else:
        st.write("🧥 두꺼운 패딩, 🧣 목도리, 🧤 장갑, 🧢 모자")

    # 날씨에 맞는 장소 추천
    st.subheader("📍 오늘 가기 좋은 장소")
    if "Rain" in condition or "Snow" in condition:
        st.write("☔ 실내 카페, 🏛️ 박물관, 🎬 영화관")
    elif "Sunny" in condition or "Clear" in condition:
        if temp >= 30:
            st.write("🏖️ 해변 (이른 아침), 🌳 공원 그늘")
        elif temp >= 20:
            st.write("🌳 공원, 🏞️ 등산로, 🚴 자전거 도로")
        else:
            st.write("🏞️ 산책로, 🏕️ 캠핑장")
    else:
        st.write("🏢 쇼핑몰, 🍽️ 맛집 탐방, 🎮 실내 체험관")
