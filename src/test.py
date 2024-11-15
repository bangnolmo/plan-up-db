import sqlite3
from crawl_department_code import get_all_hakgwa_code


def test_for_crawling_department_and_save():
    try:
        conn = sqlite3.connect("campus_schedule.sqlite")
        cursor = conn.cursor()

        data = []
        get_all_hakgwa_code(data)

        query = "INSERT INTO department VALUES(?,?);"
        cursor.executemany(query, data)

        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
