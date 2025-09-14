import streamlit as st
import requests
import time

# Socket.IO 서버 주소 (로컬에서 실행 중일 때)
# Streamlit Cloud에 배포할 때는 서버의 실제 URL로 변경해야 합니다.
SOCKET_IO_SERVER_URL = "http://localhost:5000"

st.title("JCT Volleyball Scoreboard")
st.write("Welcome to the new app!")

# Host/Client 모드 전환을 위한 라디오 버튼
mode = st.radio("모드 선택", ("Host 모드 (점수 입력)", "Client 모드 (점수 확인)"), index=0)

st.write("---")

# ----- Host 모드 (점수 입력) -----
if mode == "Host 모드 (점수 입력)":
    st.title("Host 모드 (점수 입력)")
    st.write("점수를 입력하고 서버로 전송합니다.")

    # 서버에서 현재 점수를 가져와 초기화 (Host가 시작할 때만)
    if 'scores' not in st.session_state:
        try:
            response = requests.get(f"{SOCKET_IO_SERVER_URL}/get_scores")
            if response.status_code == 200:
                st.session_state.scores = response.json()
            else:
                st.session_state.scores = {'team_a': 0, 'team_b': 0} # 서버 오류 시 기본값
        except requests.exceptions.ConnectionError:
            st.warning("서버에 연결할 수 없습니다. server.py가 실행 중인지 확인하세요.")
            st.session_state.scores = {'team_a': 0, 'team_b': 0} # 연결 실패 시 기본값


    col1, col2 = st.columns(2)

    with col1:
        st.header("팀 A")
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.scores['team_a']}</h1>", unsafe_allow_html=True)
        if st.button("팀 A +1점", key="host_a_plus"):
            st.session_state.scores['team_a'] += 1
            try:
                requests.post(f"{SOCKET_IO_SERVER_URL}/update_score", json=st.session_state.scores)
                st.rerun() # 변경: st.experimental_rerun() -> st.rerun()
            except requests.exceptions.ConnectionError:
                st.error("서버에 점수 업데이트 실패! server.py가 실행 중인지 확인하세요.")

        if st.button("팀 A -1점", key="host_a_minus"): # -1점 버튼 추가
            st.session_state.scores['team_a'] -= 1
            try:
                requests.post(f"{SOCKET_IO_SERVER_URL}/update_score", json=st.session_state.scores)
                st.rerun() # 변경: st.experimental_rerun() -> st.rerun()
            except requests.exceptions.ConnectionError:
                st.error("서버에 점수 업데이트 실패! server.py가 실행 중인지 확인하세요.")


    with col2:
        st.header("팀 B")
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.scores['team_b']}</h1>", unsafe_allow_html=True)
        if st.button("팀 B +1점", key="host_b_plus"):
            st.session_state.scores['team_b'] += 1
            try:
                requests.post(f"{SOCKET_IO_SERVER_URL}/update_score", json=st.session_state.scores)
                st.rerun() # 변경: st.experimental_rerun() -> st.rerun()
            except requests.exceptions.ConnectionError:
                st.error("서버에 점수 업데이트 실패! server.py가 실행 중인지 확인하세요.")

        if st.button("팀 B -1점", key="host_b_minus"): # -1점 버튼 추가
            st.session_state.scores['team_b'] -= 1
            try:
                requests.post(f"{SOCKET_IO_SERVER_URL}/update_score", json=st.session_state.scores)
                st.rerun() # 변경: st.experimental_rerun() -> st.rerun()
            except requests.exceptions.ConnectionError:
                st.error("서버에 점수 업데이트 실패! server.py가 실행 중인지 확인하세요.")

# ----- Client 모드 (점수 확인) -----
elif mode == "Client 모드 (점수 확인)":
    st.title("Client 모드 (점수 확인)")
    st.header("실시간 점수판")
    st.write("Host가 점수를 업데이트하면 자동으로 반영됩니다.")

    # Client는 주기적으로 서버에서 최신 점수를 가져옵니다.
    # Streamlit은 자체적으로 실시간 푸시를 지원하지 않으므로, 폴링(polling) 방식을 사용합니다.
    try:
        response = requests.get(f"{SOCKET_IO_SERVER_URL}/get_scores")
        if response.status_code == 200:
            latest_scores = response.json()
            st.session_state.scores = latest_scores # 세션 상태 업데이트
        else:
            st.error("서버에서 점수를 가져오는 데 실패했습니다.")
    except requests.exceptions.ConnectionError:
        st.error("서버에 연결할 수 없습니다. server.py가 실행 중인지 확인하세요.")

    col1, col2 = st.columns(2)

    with col1:
        st.header("팀 A")
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.scores['team_a']}</h1>", unsafe_allow_html=True)

    with col2:
        st.header("팀 B")
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.scores['team_b']}</h1>", unsafe_allow_html=True)

    # 3초마다 자동으로 새로고침 (실시간 효과를 위한 폴링)
    time.sleep(3)
    st.rerun() # 변경: st.experimental_rerun() -> st.rerun()
