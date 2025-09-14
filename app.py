import streamlit as st

st.title("JCT Volleyball Scoreboard")
st.write("Welcome to the new app!")

import streamlit as st

st.title("Host 모드 (점수 입력)")
st.write("---")

# 점수를 저장할 세션 상태를 초기화합니다.
if 'scores' not in st.session_state:
    st.session_state.scores = {'team_a': 0, 'team_b': 0}

col1, col2 = st.columns(2)

with col1:
    st.header("팀 A")
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.scores['team_a']}</h1>", unsafe_allow_html=True)
    st.button("팀 A +1점", on_click=lambda: st.session_state.scores.update({'team_a': st.session_state.scores['team_a'] + 1}))

with col2:
    st.header("팀 B")
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.scores['team_b']}</h1>", unsafe_allow_html=True)
    st.button("팀 B +1점", on_click=lambda: st.session_state.scores.update({'team_b': st.session_state.scores['team_b'] + 1}))
  st.write("---")
st.title("Client 모드 (점수 확인)")
st.header("실시간 점수판")

col1, col2 = st.columns(2)

with col1:
    st.header("팀 A")
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.scores['team_a']}</h1>", unsafe_allow_html=True)

with col2:
    st.header("팀 B")
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.scores['team_b']}</h1>", unsafe_allow_html=True)
