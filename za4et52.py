import smtplib
import schedule
import time
from email.message import EmailMessage
import json

CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "your_email@gmail.com",
    "password": "your_app_password",
    "schedule_time": "09:00"
}

with open('users.json', 'r') as f:
    users = json.load(f)

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg['From'] = CONFIG['email']
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)
    
    with smtplib.SMTP(CONFIG['smtp_server'], CONFIG['smtp_port']) as server:
        server.starttls()
        server.login(CONFIG['email'], CONFIG['password'])
        server.send_message(msg)
    print(f"Отправлено: {to_email}")

def send_notifications():
    print(f"Начало рассылки в {time.strftime('%H:%M')}")
    
    for user in users:
        name = user.get('name', 'Пользователь')
        email = user['email']
        
        subject = "Ежедневное уведомление"
        body = f"Здравствуйте, {name}!\n\nЭто автоматическое уведомление.\n\nС уважением,\nСистема"
        
        try:
            send_email(email, subject, body)
        except Exception as e:
            print(f"Ошибка для {email}: {e}")

schedule.every().day.at(CONFIG['schedule_time']).do(send_notifications)

print(f"Сервис запущен. Рассылка в {CONFIG['schedule_time']}")

while True:
    schedule.run_pending()
    time.sleep(60)