import pymysql

from pymysql.cursors import Cursor

def show_menu() -> str:
    print("1. 일정 추가")  # insert
    print("2. 일정 보기")  # select
    print("3. 일정 완료")  # update
    print("4. 종료")
    return get_user_choice()

def get_user_choice() -> str:
    return input("선택: ")

def get_db_connection() -> pymysql.Connection:
    try:
        return pymysql.connect(host="localhost", port=3307, user="root", password='1234', database='schedule_db')
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        exit(1)

def add_schedule(cursor: Cursor):
    # 일정 정보를 입력
    title = input("제목: ")
    desc = input("설명: ")
    start_datetime = input("시작 시간(yyyymmddhhmmss)")
    end_datetime = input("종료 시간(yyyymmddhhmmss")
    
    # Insert 쿼리 작성
    sql = """
        INSERT INTO schedules(title, description, start_datetime, end_datetime)
        VALUES (%s, %s, %s, %s)
    """

    # Insert 쿼리 실행
    cursor.execute(sql, (title, desc, start_datetime, end_datetime))
    print("일정이 추가됨")

def get_schedules(cursor: Cursor):
    sql = """
        SELECT id, title, description, start_datetime, end_datetime, is_completed FROM schedules
    """
    
    # 쿼리 실행
    cursor.execute(sql)

    # 쿼리에서 실행된 튜플 가져오기
    schedules = cursor.fetchall()
    if not schedules:
        print("등록된 일정이 없습니다.")
        return
    
    # 가져온 정보 출력
    for schedule in schedules:
        id, title, description, start_datetime, end_datetime, is_completed = schedule
        status = "완료" if is_completed else "미완료"

        print(f"[{id}] {title}")
        print(f"    상태: {status}")
        print(f"    시작시간: {start_datetime}")
        print(f"    종료시간: {end_datetime}")
        if description:
            print(f"    설명: {description}")
        print()

def complete_schedule(cursor: Cursor):
    id = input("id값을 입력하세요: ")

    sql = """
        UPDATE schedules SET is_completed = true WHERE id = %s
    """

    cursor.execute(sql, id)
    print("일정을 완료함")

def main():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        while True:
            choice = show_menu()
            if choice == "1":
                add_schedule(cursor)
                conn.commit()
            elif choice == "2":
                get_schedules(cursor)
            elif choice == "3":
                complete_schedule(cursor)
                conn.commit()
            elif choice == "4":
                print("종료합니다.")
                break
            else:
                print("다시 선택해주세요")

    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()