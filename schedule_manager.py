import pandas as pd
import random
from datetime import datetime, timedelta

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["Day", "Evening", "Night"]

class ScheduleRules:
    """ 스케줄 규칙을 정의하는 클래스 """

    @staticmethod
    def get_starting_saturday(selected_date):
        """ 선택한 날짜에서 속한 주의 토요일을 반환 """
        weekday = selected_date.weekday()
        return selected_date - timedelta(days=weekday - 5 if weekday >= 5 else weekday + 2)

    @staticmethod
    def is_valid_shift(shift):
        """ 유효한 근무 시간인지 확인 """
        return shift in SHIFTS

    @staticmethod
    def check_max_workdays(nurse_days, nurse):
        """ 간호사가 주당 최대 근무일을 초과하는지 확인 """
        return nurse_days[nurse]['work'] < 5  # 5일 초과 근무 금지

    @staticmethod
    def check_night_shift_restriction(nurse_days, nurse, current_date):
        """ Night 근무 제한 규칙 적용 """
        if nurse_days[nurse]['night_count'] >= 2:
            return False
        if nurse_days[nurse]['last_night'] and nurse_days[nurse]['last_night'] == current_date - timedelta(days=1):
            return False
        return True


class ShiftAssigner:
    """ 근무 배정을 담당하는 클래스 """

    @staticmethod
    def assign_shifts(nurses, shifts, available_nurses):
        """ 주어진 간호사 리스트와 가능한 근무자 중에서 시프트를 배정 """
        shift_assignments = {}
        for shift in shifts:
            if len(available_nurses) >= 2:
                selected = random.sample(sorted(available_nurses), 2)
                shift_assignments[shift] = selected
                for nurse in selected:
                    available_nurses.remove(nurse)
        return shift_assignments


class ScheduleGenerator:
    """ 근무 스케줄을 생성하는 클래스 """

    SHIFTS = ["Day", "Evening", "Night"]

    @staticmethod
    def generate_schedule(nurses):
        """ 주어진 간호사 리스트로 주간 스케줄 생성 """
        start_date = datetime.today()
        schedule = {}

        for i in range(14):  # 2주치 일정 생성
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            schedule[date] = {}

            available_nurses = nurses.copy()
            for shift in ScheduleGenerator.SHIFTS:
                if len(available_nurses) >= 2:
                    assigned_nurses = random.sample(available_nurses, 2)  # 한 시프트당 2명 배정
                    schedule[date][shift] = assigned_nurses
                    for nurse in assigned_nurses:
                        available_nurses.remove(nurse)

        return schedule



class ScheduleStatistics:
    """ 근무 스케줄 통계를 생성하는 클래스 """

    @staticmethod
    def generate_statistics(schedule_data):
        """ 근무 배정 통계를 생성하여 반환 """

        # 데이터를 pandas DataFrame으로 변환
        records = []
        for date, shifts in schedule_data.items():
            for shift, nurse in shifts.items():
                records.append({"Date": date, "Shift": shift, "Nurse": nurse})

        df = pd.DataFrame(records)

        stats = df.groupby("Nurse").agg(
            total_shifts=pd.NamedAgg(column="Shift", aggfunc="count"),
            day_shifts=pd.NamedAgg(column="Shift", aggfunc=lambda x: (x == "Day").sum()),
            evening_shifts=pd.NamedAgg(column="Shift", aggfunc=lambda x: (x == "Evening").sum()),
            night_shifts=pd.NamedAgg(column="Shift", aggfunc=lambda x: (x == "Night").sum())
        )

        stats["workload_ok"] = stats["total_shifts"].apply(lambda x: 5 <= x <= 10)
        return stats
