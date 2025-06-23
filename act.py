import streamlit as st
import time
import random

# 초기 상태 설정 함수
def initialize_state():
    defaults = {
        'started': False,
        'value_intro_done': False,
        'age_index': 0,
        'timeline': [],
        'show_result': False,
        'latest_result': None,
        'transitioning': False,
        'final_transition': False,
        'in_progress': False,
        'child_preview': None,
        'child_result': None,
        'show_child_result': False,
        'show_progress_screen': False,
        'show_transition_screen': False,
        'next_page': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# CSS 적용 함수
def set_styles():
    st.markdown("""
    <style>
    html, body, [class*='css']  {
        font-size: 24px !important;
        background: #fffbe6;
        color: #333;
        text-align: center;
    }
    div.stButton > button {
        padding: 1.2rem 2.5rem;
        font-size: 24px !important;
        margin: 20px auto;
        display: block;
        border-radius: 10px;
        background-color: #f9a825;
        color: white !important;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #f57f17;
        color: white !important;
        transform: scale(1.05);
    }
    .centered {
        margin: auto;
        padding: 10px 40px;
        max-width: 800px;
        font-size: 30px;
    }
                
    .full-screen-center {
        justify-content: center;
        align-items: center;
        height: 100vh; 
                          
    .result-body + .result-body {
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 자녀 구성 미리보기 함수
def get_child_preview(decision):
    if "1명" in decision:
        gender = random.choice(["아들", "딸"])
        return f"👶 {gender} 탄생!"
    elif "2명" in decision:
        genders = random.sample(["아들", "딸"], 2)
        return f"👶 {'과 '.join(genders)} 탄생!"
    elif "3명" in decision:
        genders = random.choices(["아들", "딸"], k=3)
        return f"👶 {' · '.join(genders)} 탄생!"
    return None

# 예시용 선택지 (추후 전체 나이대 및 선택지 구성 필요)
ages = [21, 22, 23, 24, 27, 29, 30, 32, 35, 38, 40, 45, 60, 65]
choices = {
    21: ("대학 입학 후, 본격적으로 프로그래밍을 배워보기로 하는데 어떤 언어가 좋을까?",
         [("파이썬 마스터하기", "문제 해결력과 자동화 기술을 익혔어!"),
          ("C언어 도전하기", "메모리와 알고리즘의 깊은 이해를 얻게 되었어!")]),
     22: ("공대로 복수전공을 하려고 하는데 어떤 과가 끌려?",
         [("그래도 근본은 '소프트웨어'지", "기초부터 탄탄히 실력을 다졌어."),
          ("요즘 대세는 'AI'지", "미래 기술에 대한 통찰을 얻게 되었어.")]),
    23: ("교환학생 신청 기간이야!",
         [("대학생의 로망 교환학생, 가보자!", "새로운 문화와 친구들을 만나며 시야가 넓어졌어."),
          ("졸업도 늦어지고, 여행으로 가는 게 나아. 가지 말자.", "국내에서 깊이 있는 경험과 관계를 쌓았어.")]),
    24: ("졸업이 얼마 안 남았어. 대학원, 가 말아?",
         [("학사로는 부족해! 대학원 진학하기", "연구의 즐거움을 알게 되었어."),
          ("난 취업하고 싶어!", "실무 경험을 쌓으며 빠르게 성장했어.")]),
    27: ("첫 직장으로 어느 기업에 지원할까?",
         [("무조건 대기업이지!", "안정적인 환경에서 다양한 프로젝트를 경험했어"),
          ("중소기업부터 차근차근 할래!", "작은 조직에서 주도적으로 일하며 성장했어.")]),
    29: ("긴 휴가를 냈어! 어디로 여행갈까?",
         [("미국", "광활한 대지와 자유로운 문화를 경험했어."),
          ("영국", "고풍스러운 분위기 속에서 깊은 역사와 문화를 체험했어.")]),
    30: ("결혼할 상대를 찾고 있어! 어떤 사람이 좋아?",
         [("다정한 연상", "항상 따뜻한 말과 행동으로 위로를 받았어."),
          ("재미있는 동갑", "함께 있는 것만으로도 즐거운 시간을 보냈어."),
          ("귀여운 연하", "활기찬 에너지와 웃음을 가득 안겨주었어.")]),
    32: ("자녀 계획을 세워보자! 몇 명이 좋을까?",
         [("엄마아빠 사랑 독차지, 1명", "집중적인 사랑을 줄 수 있었어."),
          ("혼자는 외로워, 2명", "형제자매와 함께 자라는 기쁨을 누렸어."),
          ("많을수록 좋지, 3명", "분주하지만 웃음이 끊이지 않는 집이 되었어.")]),
    35: ("커리어적으로 고민되는 시기야.",
         [("내 능력을 더 알아주는 기업으로 가겠어, 이직하기", "새로운 환경에서 성장의 기회를 얻었어."),
          ("지금 있는 곳에서 최고가 되겠어, 계속 다니기", "익숙한 곳에서 전문성을 더욱 강화했어.")]),
    38: ("꿈꿔왔던 내 집 마련! 어느 지역이 좋아?",
         [("집의 크기보단 주변 인프라가 중요하지, 서울", "서울에 내 집 마련 성공!"),
          ("직장에선 멀지만 한적하고 여유로운 경기도", "경기도에 내 집 마련 성공!")]),
    40: ("자동차를 장만하려고 해. 어떤 브랜드가 좋을까?",
         [("BMW", "스포티한 주행감에 매료되었어."),
          ("벤츠", "고급스러운 승차감과 안정감을 느꼈어.")]),
    45: ("자녀들이 크고 있어. 어떤 방식으로 교육할까?",
         [("학업이 중요해, 교육 중심", "엄격하지만 성취 중심적인 환경을 만들었어."),
          ("창의성이 중요해, 자유 방임", "스스로의 선택을 존중하는 유연한 환경을 만들었어.")]),
    60: ("벌써 아이의 결혼식 날이야.",
         [("울기", "눈물 속에 지난 세월이 주마등처럼 스쳐갔어."),
          ("안울기", "묵묵히 미소 지으며 마음으로 축복했어.")]),
    65: ("노후 대비를 완료하고 은퇴했어. 남은 삶을 어디에서 보낼까?",
         [("서울", "문화생활과 편리함 속에서 활기찬 노년을 보냈어."),
          ("제주도", "자연과 함께 여유롭고 평화로운 시간을 보냈어.")])
}

custom_progress_messages = {
    "파이썬 마스터하기": "파이썬 마스터 중...",
    "C언어 도전하기": "C언어 도전 중...",
    "그래도 근본은 '소프트웨어'지": "소프트웨어 전공수업 듣는 중...",
    "요즘 대세는 'AI'지": "AI 전공수업 듣는 중...",
    "대학생의 로망 교환학생, 가보자!": "외국 대학에서 공부 중...",
    "졸업도 늦어지고, 여행으로 가는 게 나아. 가지 말자.": "중앙대에서 공부 중...",
    "학사로는 부족해! 대학원 진학하기": "대학원에서 공부 중...",
    "난 취업하고 싶어!": "취업 준비 중...",
    "무조건 대기업이지!": "대기업 입사 준비 중...",
    "중소기업부터 차근차근 할래!": "중소기업 입사 지원 중...",
    "미국": "자유의 여신상 감상 중...",
    "영국": "피쉬앤칩스 먹는 중...",
    "다정한 연상": "다정한 사람과의 연애 중...",
    "재미있는 동갑": "동갑내기와의 데이트 중...",
    "귀여운 연하": "연하남과 데이트 중...",
    "엄마아빠 사랑 독차지, 1명": "첫 아이 기다리는 중...",
    "혼자는 외로워, 2명": "자녀 둘 계획 중...",
    "많을수록 좋지, 3명": "세 아이 준비 중...",
    "내 능력을 더 알아주는 기업으로 가겠어, 이직하기": "이직 준비 중...",
    "지금 있는 곳에서 최고가 되겠어, 계속 다니기": "기존 직장에서 노력 중...",
    "집은 크기보단 인프라가 중요하지, 서울": "서울 집 계약 진행 중...",
    "직장에선 멀지만 한적하고 여유로운 경기도": "경기도 주택 계약 준비 중...",
    "BMW": "BMW 시승 중...",
    "벤츠": "벤츠 시승 중...",
    "학업이 중요해, 교육 중심": "교육 중심으로 아이 지도 중...",
    "창의성이 중요해, 자유 방임": "자유롭게 아이를 지도 중...",
    "울기": "눈물 흘리며 결혼식 감상 중...",
    "안울기": "미소 지으며 결혼식 참석 중...",
    "서울": "서울에서 노년 생활 즐기는 중...",
    "제주도": "제주에서 은퇴 생활 시작..."
}

# 시작
initialize_state()
set_styles()

if st.session_state.get('show_progress_screen') and not st.session_state.get('show_result'):
    decision = st.session_state.latest_result.get('decision', '')
    progress_message = custom_progress_messages.get(decision, "선택 진행 중...")
    st.markdown(f"""
    <div class='full-screen-center'>
        <h4 style='font-size:40px; margin-top:50px;'>⏳ {progress_message} 결과는?</h4>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.show_progress_screen = False
    st.session_state.show_result = True
    st.rerun()

elif st.session_state.get('show_transition_screen'):
    time.sleep(1)
    st.session_state.show_transition_screen = False
    st.session_state.age_index += 1
    st.session_state.show_result = False
    st.session_state.latest_result = {}
    st.rerun()

elif not st.session_state.next_page:
    st.markdown("<div class='centered' style='font-size:40px;'><strong>✨ 나의 인생 가치관</strong></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='centered' style='font-size:27px;'>
    <p>제 인생에서 가장 중요한 가치는 <strong>"행복"</strong> 입니다.</p>
    <p>그리고 행복한 삶을 살기 위해 가장 중요한 것은</p>
    <p><strong>"과거에 얽매이지 않는 것"</strong> 이라고 생각합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("다음으로"):
        st.session_state.next_page = True
        st.rerun()

elif not st.session_state.started:
    time.sleep(1.5)
    st.markdown("<div class='centered' style='font-size:40px;'><strong>✨ 나의 인생 가치관</strong></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='centered' style='font-size:27px;'>
    <p>누군가 말했듯이 인생은 <strong>"선택"</strong>의 연속입니다.</p>
    <p>행복하게 살기 위해 저는, 모든 <strong>"선택"</strong>에 최선을 다할 것이고</p>
    <p>행복하게 살기 위해 저는, 지난 <strong>"선택"</strong>을 후회하지 않을 것입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 시작하기"):
        st.session_state.started = True
        st.rerun()

else:
    idx = st.session_state.age_index
    if idx >= len(ages):
        st.balloons()
        time.sleep(2.5)
        st.title("📜 나의 인생 연출안")
        for age, decision, result in st.session_state.timeline:
            st.markdown(f"<div class='timeline-entry'><strong>{decision}</strong><br>{result}</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("🧾 인생 요약")
        for i, (_, _, r) in enumerate(st.session_state.timeline, 1):
            st.markdown(f"{i}. {r}")
        if st.button("🔁 다시 시작하기"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    else:
        age = ages[idx]
        context, options = choices.get(age, ("질문 없음", []))

        if st.session_state.get('show_result'):
            decision = st.session_state.latest_result.get('decision', '')
            result = st.session_state.latest_result.get('result', '')
            st.markdown("<h3 div class='result-header' style='font-size:30px;'>✅ 당신의 선택</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-body' style='font-size:30px; margin-top: 20px;'><strong>👉{decision}</div>", unsafe_allow_html=True)
            
            if age == 30:
                st.markdown(f"<div class='result-body'style='font-size:40px;'><strong> 💑{decision}과 결혼!</div>", unsafe_allow_html=True)

            if age == 32 and st.session_state.show_child_result and st.session_state.child_result:
                st.markdown(f"<div class='result-body'style='font-size:40px;'><strong>{st.session_state.child_result}</div>", unsafe_allow_html=True)
                st.session_state.show_child_result = False

            st.markdown(f"<div class='result-body' style='font-size:40px; margin-top: 45px;'><strong>\"{result}\"</div>", unsafe_allow_html=True)

            if st.button("다음 선택으로 넘어가기"):
                st.session_state.show_result = False
                st.session_state.show_transition_screen = True
                st.rerun()

        else:
            st.markdown(f"<h3 style='font-size:30px;'>📅 {age}살</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='centered' style='font-size:37px;'><strong>{context}</strong></div>", unsafe_allow_html=True)
            for i, (label, result) in enumerate(options):
                if st.button(f"👉 {label}", key=f"choice_{age}_{i}"):
                    st.session_state.timeline.append((age, label, result))
                    st.session_state.latest_result = {"decision": label, "result": result}
                    st.session_state.show_progress_screen = True
                    st.session_state.show_result = False
                    if age == 32:
                        preview = get_child_preview(label)
                        st.session_state.child_result = preview
                        st.session_state.show_child_result = True
                    st.rerun()





# streamlit run act.py



# 마지막 결론.



# 설명
# 제 인생에서 가장 중요한 가치는 "행복" 입니다. 
# 그리고 행복한 삶을 살기 위해 가장 중요한 것은
# "자신의 과거에 대해 후회하지 않는 것"이라고 생각합니다.

# 누군가 말했듯이 인생은 "선택"의 연속입니다. 
# 행복한 삶을 위해 저는 항상 현재의 상황에서 최선의 "선택"을 하기 위해 노력할 것이고, 
# 행복한 삶을 위해 저는 지나간 "선택"을 후회하지 않고 이를 통해 성장할 것 입니다.

# 인생의 전체적인 흐름과 그에 따른 선택지는 예상해볼 수 있지만, 
# 그 시기의 제 상황에 따라 선택의 방향은 달라질 수 있습니다. 
# 그렇기 때문에, 제 선택에 따라 달라지는 인생을 표현하고자 이러한 양자택일 형식을 선택했습니다.
# 또, 저의 인생에서 가장 중요한 부분 중 하나가 커리어이고,
# 현재 저는 컴퓨터 엔지니어를 꿈꾸고 있기 때문에, 이를 파이썬을 활용한 웹앱으로 구현해보았습니다.