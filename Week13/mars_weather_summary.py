import csv
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os


class MySQLHelper:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def executemany(self, query, data):
        self.cursor.executemany(query, data)
        self.conn.commit()

    def fetchall(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


# DB 설정
config = {
    'user': 'root',
    'password': '1427',
    'host': 'localhost',
    'port': 3306,
    'database': 'mars_db',
}

csv_file_path = r'C:\Codessey\Week13\mars_weathers_data.CSV'
save_path_all = r'C:\Codessey\Week13\mars_summary.png'
save_path_avg = r'C:\Codessey\Week13\mars_monthly_avg.png'

insert_data = []

try:
    # CSV 읽기
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mars_date = datetime.strptime(row['mars_date'], "%Y-%m-%d")
            temp = int(float(row['temp']))
            storm = int(row['stom'])  # stom 컬럼명 그대로 처리
            insert_data.append((mars_date, temp, storm))

    db = MySQLHelper(config)
    db.connect()

    # 기존 데이터 초기화
    db.execute("TRUNCATE TABLE mars_weather")

    # INSERT
    insert_query = """
        INSERT INTO mars_weather (mars_date, temp, storm)
        VALUES (%s, %s, %s)
    """
    db.executemany(insert_query, insert_data)
    print("✅ CSV 데이터가 DB에 성공적으로 삽입되었습니다.")

    # === 1. 전체 데이터 시각화 ===
    results = db.fetchall("SELECT mars_date, temp, storm FROM mars_weather ORDER BY mars_date")
    dates = [row['mars_date'] for row in results]
    temps = [row['temp'] for row in results]
    storms = [row['storm'] for row in results]

    fig, ax1 = plt.subplots(figsize=(14, 7))
    ax1.set_title('Mars Weather Summary')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (℃)', color='tab:blue')
    ax1.plot(dates, temps, color='tab:blue', label='Temperature (℃)')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Storm Index', color='tab:orange')
    ax2.plot(dates, storms, color='tab:orange', label='Storm Index')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.grid(True)
    plt.savefig(save_path_all)
    print(f"✅ 전체 그래프 저장 완료: {save_path_all}")
    plt.close()

    # === 2. 월별 평균 시각화 ===
    monthly_avg_query = """
        SELECT
            DATE_FORMAT(mars_date, '%Y-%m') AS month,
            AVG(temp) AS avg_temp,
            AVG(storm) AS avg_storm
        FROM mars_weather
        GROUP BY month
        ORDER BY month;
    """
    monthly_results = db.fetchall(monthly_avg_query)
    months = [datetime.strptime(row['month'], "%Y-%m") for row in monthly_results]
    avg_temps = [row['avg_temp'] for row in monthly_results]
    avg_storms = [row['avg_storm'] for row in monthly_results]

    fig2, ax1 = plt.subplots(figsize=(14, 7))
    ax1.set_title('Monthly Average Mars Weather')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Avg Temperature (℃)', color='tab:blue')
    ax1.plot(months, avg_temps, color='tab:blue', marker='o', label='Avg Temp')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Avg Storm Index', color='tab:orange')
    ax2.plot(months, avg_storms, color='tab:orange', marker='x', label='Avg Storm')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig2.autofmt_xdate()
    fig2.tight_layout()
    plt.grid(True)
    plt.savefig(save_path_avg)
    print(f"✅ 월별 평균 그래프 저장 완료: {save_path_avg}")
    plt.close()

except Exception as e:
    print(f"❌ 오류 발생: {e}")

finally:
    if 'db' in locals():
        db.close()
