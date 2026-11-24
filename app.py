import streamlit as st
import random
import calendar
from datetime import date, timedelta

# 함수 1: 공부 계획 생성 함수
def make_study_plan(start_date, exam_date, subjects, confidence, daily_hours):

    plan = {}
    current_date = start_date

    # 반복문: 오늘부터 시험 전날까지 날짜별 계획 생성
    while current_date < exam_date:

        # 자신감이 낮은 과목일수록 높은 가중치
        weights = [6 - confidence[s] for s in subjects]

        # 하루에 공부할 과목 수 결정
        count = min(2, len(subjects), daily_hours)

        # random을 이용해 과목 선택
        selected = []

        temp_subjects = subjects.copy()
        temp_weights = weights.copy()

        for i in range(count):
            chosen = random.choices(
                temp_subjects,
                weights=temp_weights,
                k=1
            )[0]

            selected.append(chosen)

            index = temp_subjects.index(chosen)
            temp_subjects.pop(index)
            temp_weights.pop(index)

        # 선택한 과목에 공부 시간 배분
        daily_plan = {}

        if count == 1:
            daily_plan[selected[0]] = daily_hours

        else:
            first_hours = random.randint(1, daily_hours - 1)
            second_hours = daily_hours - first_hours

            daily_plan[selected[0]] = first_hours
            daily_plan[selected[1]] = second_hours

        plan[current_date] = daily_plan

        current_date += timedelta(days=1)

    return plan


# 함수 2: 달력 출력 함수
def show_calendar(plan, start_date, exam_date):

    st.subheader("🗓️ 나의 시험 대비 공부 달력")

    # 시작 월과 마지막 월 계산
    current_month = start_date.replace(day=1)
    last_month = (exam_date - timedelta(days=1)).replace(day=1)

    weekdays = ["월", "화", "수", "목", "금", "토", "일"]

    # 반복문: 모든 달력 출력
    while current_month <= last_month:

        st.markdown(
            f"### {current_month.year}년 {current_month.month}월"
        )

        # 요일 출력
        cols = st.columns(7)

        for col, weekday in zip(cols, weekdays):
            with col:
                st.markdown(f"**{weekday}**")

        # 해당 월의 달력 생성
        month_data = calendar.monthcalendar(
            current_month.year,
            current_month.month
        )

        # 반복문: 주별 달력 출력
        for week in month_data:

            cols = st.columns(7)

            for col, day in zip(cols, week):

                with col:

                    if day == 0:
                        st.write(" ")
                    else:
                        current_date = date(
                            current_month.year,
                            current_month.month,
                            day
                        )

                        st.markdown(f"**{day}일**")

                        # 조건문: 공부 계획이 있는 날짜인지 확인
                        if current_date in plan:

                            for subject, hours in plan[current_date].items():
                                st.caption(
                                    f"📖 {subject}\n{hours}시간"
                                )

                        elif current_date == exam_date:
                            st.caption("📝 시험일")

                        elif current_date < start_date or current_date > exam_date:
                            st.write(" ")

                        else:
                            st.caption("공부 계획 없음")

        st.divider()

        # 다음 달로 이동
        if current_month.month == 12:
            current_month = date(
                current_month.year + 1, 1, 1
            )
        else:
            current_month = date(
                current_month.year,
                current_month.month + 1,
                1
            )


# ---------------------------------
# 메인 웹앱
# ---------------------------------

st.title("📚 시험 대비 공부 계획 달력")
st.write("시험 날짜에 맞춰 과목별 공부 계획을 달력으로 만들어 보세요!")

# 오늘 날짜 입력
st.subheader("📅 날짜 입력")

start_date = st.date_input(
    "오늘 날짜",
    value=date.today()
)

# 시험 날짜 입력
exam_date = st.date_input(
    "시험 날짜",
    value=date.today() + timedelta(days=14)
)

# 하루 공부 시간 입력
daily_hours = st.number_input(
    "하루 공부 가능 시간",
    min_value=1,
    max_value=24,
    value=5
)

# 과목 입력
st.subheader("📖 교과목 입력")

subjects_text = st.text_input(
    "과목을 쉼표로 구분해서 입력하세요.",
    "국어, 영어, 수학, 과학, 사회"
)

subjects = list(dict.fromkeys([
    s.strip() for s in subjects_text.split(",") if s.strip()
]))

# 자신감 입력
st.subheader("💪 과목별 자신감")

confidence = {}

# 반복문: 각 과목의 자신감 입력
for subject in subjects:

    confidence[subject] = st.slider(
        subject + " 자신감",
        min_value=1,
        max_value=5,
        value=3
    )


# 계획 생성 버튼
if st.button("🗓️ 공부 계획 만들기"):

    # 조건문: 입력값 검사
    if len(subjects) == 0:

        st.warning("교과목을 입력해주세요.")

    elif exam_date <= start_date:

        st.warning("시험 날짜는 오늘 날짜보다 뒤여야 합니다.")

    else:

        # 공부 계획 생성 함수 호출
        study_plan = make_study_plan(
            start_date,
            exam_date,
            subjects,
            confidence,
            daily_hours
        )

        st.success("공부 계획이 완성되었습니다!")

        # 달력 출력 함수 호출
        show_calendar(
            study_plan,
            start_date,
            exam_date
        )

        # 전체 공부 시간 계산
        total_hours = sum(
            sum(daily.values())
            for daily in study_plan.values()
        )

        st.info(
            f"시험 전까지 총 공부 시간: {total_hours}시간"
        )
