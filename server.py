from flask import Flask, jsonify, request # request를 import 합니다.
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
# 보안을 위한 비밀 키입니다. 실제 배포 시에는 복잡하고 예측 불가능한 문자열로 변경해야 합니다.
app.config['SECRET_KEY'] = 'my_super_secret_key_for_jct' 
# 개발 단계에서는 모든 오리진(도메인)에서 접속을 허용합니다. 배포 시에는 특정 도메인으로 제한해야 합니다.
socketio = SocketIO(app, cors_allowed_origins="*") 

# 현재 점수를 저장할 전역 변수
current_scores = {'team_a': 0, 'team_b': 0}

# ----- HTTP GET 요청 처리 (Streamlit Client가 점수 가져갈 때 사용) -----
@app.route('/get_scores', methods=['GET'])
def get_scores():
    """Streamlit 클라이언트가 현재 점수를 요청할 때 사용합니다."""
    return jsonify(current_scores)

# ----- HTTP POST 요청 처리 (Streamlit Host가 점수 업데이트할 때 사용) -----
@app.route('/update_score', methods=['POST'])
def update_score_http():
    """Streamlit Host가 점수를 업데이트할 때 사용합니다."""
    global current_scores
    data = request.json # POST 요청 바디에서 JSON 데이터를 파싱합니다.
    if data:
        # 받은 데이터로 점수를 업데이트합니다.
        if 'team_a' in data:
            current_scores['team_a'] = data['team_a']
        if 'team_b' in data:
            current_scores['team_b'] = data['team_b']
        
        # Socket.IO를 통해 모든 연결된 클라이언트에게 점수 업데이트를 알립니다.
        # Streamlit 클라이언트는 주로 /get_scores를 폴링하지만, 일반 웹 클라이언트가 있다면 이 메시지를 받습니다.
        socketio.emit('score_update', current_scores)
        
        return jsonify({"status": "success", "scores": current_scores}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

# ----- Socket.IO 이벤트 처리 (일반 웹 클라이언트를 위한) -----
@socketio.on('connect')
def test_connect():
    """클라이언트가 Socket.IO 서버에 연결되었을 때 호출됩니다."""
    print(f'클라이언트 연결됨: {request.sid}')
    # 연결된 클라이언트에게 현재 점수를 바로 전송합니다.
    emit('score_update', current_scores) 

@socketio.on('disconnect')
def test_disconnect():
    """클라이언트가 Socket.IO 서버에서 연결이 끊겼을 때 호출됩니다."""
    print(f'클라이언트 연결 끊김: {request.sid}')

# ----- 서버 시작 -----
if __name__ == '__main__':
    # 개발 환경에서는 debug=True로 설정 가능합니다. 실제 배포 시에는 False로 설정해야 합니다.
    # allow_unsafe_werkzeug=True는 개발용이며, 일부 환경에서 필요한 설정입니다.
    print(f"Socket.IO 서버 시작: http://localhost:5000")
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
