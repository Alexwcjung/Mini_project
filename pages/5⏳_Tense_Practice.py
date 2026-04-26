import streamlit as st

st.set_page_config(page_title="Tense Practice", layout="centered")

st.title("⏳ Tense Practice")
st.caption("문제를 풀고 각 문제의 정답 확인 버튼을 누르세요. 맞히면 폭죽이 터집니다.")

TOTAL_QUESTIONS = 20

quiz_data = [
    {
        "sentence": "She (     ) a book now.",
        "answer": "is reading",
        "choices": ["reads", "is reading", "read", "will read"]
    },
    {
        "sentence": "They (     ) soccer yesterday.",
        "answer": "played",
        "choices": ["play", "are playing", "played", "will play"]
    },
    {
        "sentence": "I (     ) breakfast every morning.",
        "answer": "eat",
        "choices": ["am eating", "ate", "will eat", "eat"]
    },
    {
        "sentence": "He (     ) his friend tomorrow.",
        "answer": "will meet",
        "choices": ["meets", "met", "will meet", "is meeting"]
    },
    {
        "sentence": "We (     ) English now.",
        "answer": "are studying",
        "choices": ["studied", "study", "are studying", "will study"]
    },
    {
        "sentence": "My father (     ) coffee every day.",
        "answer": "drinks",
        "choices": ["drinks", "is drinking", "drank", "will drink"]
    },
    {
        "sentence": "The students (     ) to the teacher now.",
        "answer": "are listening",
        "choices": ["listen", "listened", "will listen", "are listening"]
    },
    {
        "sentence": "I (     ) my homework last night.",
        "answer": "did",
        "choices": ["do", "am doing", "did", "will do"]
    },
    {
        "sentence": "She (     ) to school by bus every day.",
        "answer": "goes",
        "choices": ["is going", "went", "will go", "goes"]
    },
    {
        "sentence": "He (     ) TV now.",
        "answer": "is watching",
        "choices": ["watched", "watches", "is watching", "will watch"]
    },
    {
        "sentence": "We (     ) a movie tomorrow.",
        "answer": "will watch",
        "choices": ["watch", "watched", "are watching", "will watch"]
    },
    {
        "sentence": "They (     ) in the park last Sunday.",
        "answer": "walked",
        "choices": ["walked", "walk", "are walking", "will walk"]
    },
    {
        "sentence": "My brother (     ) computer games every weekend.",
        "answer": "plays",
        "choices": ["is playing", "played", "plays", "will play"]
    },
    {
        "sentence": "Look! The baby (     ).",
        "answer": "is sleeping",
        "choices": ["sleeps", "slept", "will sleep", "is sleeping"]
    },
    {
        "sentence": "I (     ) my grandmother next week.",
        "answer": "will visit",
        "choices": ["visit", "visited", "am visiting", "will visit"]
    },
    {
        "sentence": "She (     ) a letter yesterday.",
        "answer": "wrote",
        "choices": ["writes", "is writing", "wrote", "will write"]
    },
    {
        "sentence": "Tom (     ) up at seven every morning.",
        "answer": "gets",
        "choices": ["got", "gets", "is getting", "will get"]
    },
    {
        "sentence": "We (     ) lunch now.",
        "answer": "are having",
        "choices": ["have", "had", "are having", "will have"]
    },
    {
        "sentence": "It (     ) tomorrow.",
        "answer": "will rain",
        "choices": ["rains", "rained", "is raining", "will rain"]
    },
    {
        "sentence": "He (     ) a new bike last month.",
        "answer": "bought",
        "choices": ["buys", "is buying", "bought", "will buy"]
    },
]

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "stage" not in st.session_state:
    st.session_state.stage = 1

if "checked" not in st.session_state:
    st.session_state.checked = {}

if "first_answers" not in st.session_state:
    st.session_state.first_answers = {}

if "second_answers" not in st.session_state:
    st.session_state.second_answers = {}

if "wrong_indices" not in st.session_state:
    st.session_state.wrong_indices = []

if "final_wrong_indices" not in st.session_state:
    st.session_state.final_wrong_indices = []

if "first_score" not in st.session_state:
    st.session_state.first_score = 0

if "final_score" not in st.session_state:
    st.session_state.final_score = 0

# ---------------------------
# 다시 시작
# ---------------------------
if st.button("처음부터 다시 시작"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")


# ---------------------------
# 1차 풀이
# ---------------------------
if st.session_state.stage == 1:
    st.subheader("1차 풀이")
    st.caption("각 문제를 풀고, 바로 아래의 정답 확인 버튼을 누르세요.")

    for i, item in enumerate(quiz_data):
        st.write(f"### {i+1}. {item['sentence']}")

        user_answer = st.radio(
            "정답을 고르세요.",
            item["choices"],
            key=f"q1_{i}",
            index=None
        )

        if st.button("정답 확인", key=f"check1_{i}"):
            if user_answer is None:
                st.warning("먼저 답을 고르세요.")
            else:
                st.session_state.first_answers[i] = user_answer
                st.session_state.checked[f"q1_{i}"] = True

                if user_answer == item["answer"]:
                    st.success("정답입니다! 🎉")
                    st.balloons()
                else:
                    st.error("오답입니다. 이 문제는 2차에서 다시 풀게 됩니다.")

        if st.session_state.checked.get(f"q1_{i}", False):
            saved_answer = st.session_state.first_answers.get(i)

            if saved_answer == item["answer"]:
                st.success("정답 완료")
            else:
                st.error("오답 기록됨")

        st.markdown("---")

    if st.button("1차 완료하고 2차로 넘어가기"):
        wrong_indices = []
        correct_count = 0

        for i, item in enumerate(quiz_data):
            user_answer = st.session_state.first_answers.get(i)

            if user_answer == item["answer"]:
                correct_count += 1
            else:
                wrong_indices.append(i)

        st.session_state.first_score = correct_count
        st.session_state.wrong_indices = wrong_indices

        if len(wrong_indices) == 0:
            st.session_state.final_score = TOTAL_QUESTIONS
            st.session_state.stage = 3
        else:
            st.session_state.stage = 2

        st.rerun()


# ---------------------------
# 2차 풀이
# ---------------------------
elif st.session_state.stage == 2:
    st.subheader("2차 풀이")
    st.write(f"1차 점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.warning(f"다시 풀 문제: {len(st.session_state.wrong_indices)}문제")

    st.markdown("---")

    for idx in st.session_state.wrong_indices:
        item = quiz_data[idx]

        st.write(f"### {idx+1}. {item['sentence']}")

        user_answer = st.radio(
            "다시 정답을 고르세요.",
            item["choices"],
            key=f"q2_{idx}",
            index=None
        )

        if st.button("2차 정답 확인", key=f"check2_{idx}"):
            if user_answer is None:
                st.warning("먼저 답을 고르세요.")
            else:
                st.session_state.second_answers[idx] = user_answer
                st.session_state.checked[f"q2_{idx}"] = True

                if user_answer == item["answer"]:
                    st.success("2차에서 정답입니다! 🎉")
                    st.balloons()
                else:
                    st.error("아쉽습니다. 최종 오답으로 기록됩니다.")

        if st.session_state.checked.get(f"q2_{idx}", False):
            saved_answer = st.session_state.second_answers.get(idx)

            if saved_answer == item["answer"]:
                st.success("2차 정답 완료")
            else:
                st.error("최종 오답 기록됨")

        st.markdown("---")

    if st.button("2차 완료하고 결과 보기"):
        additional_correct = 0
        final_wrong_indices = []

        for idx in st.session_state.wrong_indices:
            item = quiz_data[idx]
            retry_answer = st.session_state.second_answers.get(idx)

            if retry_answer == item["answer"]:
                additional_correct += 1
            else:
                final_wrong_indices.append(idx)

        st.session_state.final_score = st.session_state.first_score + additional_correct
        st.session_state.final_wrong_indices = final_wrong_indices
        st.session_state.stage = 3

        st.rerun()


# ---------------------------
# 최종 결과
# ---------------------------
elif st.session_state.stage == 3:
    st.subheader("최종 결과")

    st.write(f"1차 점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.write(f"최종 점수: **{st.session_state.final_score} / {TOTAL_QUESTIONS}**")

    if st.session_state.final_score == TOTAL_QUESTIONS:
        st.success("만점입니다! 아주 잘했습니다! 🎉")
        st.balloons()
    elif st.session_state.final_score >= 16:
        st.success("아주 잘했습니다!")
    elif st.session_state.final_score >= 12:
        st.info("잘했습니다.")
    else:
        st.warning("조금 더 연습해 봅시다.")

    st.markdown("---")
    st.subheader("정답 확인")

    for i, item in enumerate(quiz_data):
        first_answer = st.session_state.first_answers.get(i, "미응답")
        second_answer = st.session_state.second_answers.get(i, None)

        st.write(f"### {i+1}. {item['sentence']}")
        st.write(f"- 정답: **{item['answer']}**")
        st.write(f"- 1차 선택: {first_answer}")

        if i in st.session_state.wrong_indices:
            st.write(f"- 2차 선택: {second_answer if second_answer else '미응답'}")

            if i in st.session_state.final_wrong_indices:
                st.error("최종 오답")
            else:
                st.success("2차에서 정답")
        else:
            st.success("1차에서 정답")

        st.markdown("---")
