from schedule_manager import ScheduleGenerator, ScheduleStatistics
from gui_results import display_schedule_calendar, save_schedule_to_excel

def format_schedule(schedule):
    """스케줄 데이터를 문자열 형태로 변환"""
    formatted_schedule = {}
    for date, shifts in schedule.items():
        formatted_schedule[date] = {}
        for shift, nurses in shifts.items():
            # 간호사 리스트를 쉼표로 구분된 문자열로 변환
            formatted_schedule[date][shift] = ', '.join(nurses)
    return formatted_schedule

def format_schedule_for_stats(schedule):
    """통계 분석을 위한 스케줄 데이터 포맷 변환"""
    formatted_data = {}
    for date, shifts in schedule.items():
        formatted_data[date] = {}
        for shift, nurses in shifts.items():
            # 각 간호사를 개별 레코드로 변환
            for nurse in nurses:
                if nurse not in formatted_data[date]:
                    formatted_data[date][nurse] = shift
    return formatted_data

def main():
    # 19명의 간호사 리스트 생성 (간호사1 ~ 간호사19)
    nurses = [f"간호사{i}" for i in range(1, 20)]
    
    # 스케줄 생성
    print("🔄 스케줄 생성 중...")
    schedule_generator = ScheduleGenerator()
    schedule = schedule_generator.generate_schedule(nurses)
    
    # 통계 생성
    print("\n📊 스케줄 통계 분석 중...")
    stats_schedule = format_schedule_for_stats(schedule)
    stats = ScheduleStatistics.generate_statistics(stats_schedule)
    print("\n=== 근무 통계 ===")
    print(stats)
    
    # GUI 표시 및 엑셀 저장을 위한 스케줄 포맷 변환
    formatted_schedule = format_schedule(schedule)
    
    # 엑셀 파일로 저장
    save_schedule_to_excel(formatted_schedule)
    
    # GUI로 스케줄 표시
    print("\n🖥️ 스케줄 캘린더를 표시합니다...")
    display_schedule_calendar(formatted_schedule)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {str(e)}")