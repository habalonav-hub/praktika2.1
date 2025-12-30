import smtplib
import schedule
import time
from email.message import EmailMessage
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class EmailNotifier:
    def __init__(self):
        self.load_settings()
        
    def load_settings(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        with open('users.json', 'r') as f:
            self.users = json.load(f)
    
    def test_connection(self):
        try:
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['email'], self.config['password'])
            server.quit()
            return True
        except Exception as e:
            logging.error(f"Connection error: {e}")
            return False
    
    def send_email(self, recipient_email, recipient_name):
        try:
            msg = EmailMessage()
            msg['From'] = self.config['email']
            msg['To'] = recipient_email
            msg['Subject'] = f"Ежедневное уведомление - {datetime.now().strftime('%d.%m.%Y')}"
            
            body = f"""Уважаемый(ая) {recipient_name},

Это автоматическое уведомление.
Время отправки: {datetime.now().strftime('%H:%M')}

С уважением,
Автоматическая система"""
            msg.set_content(body)
            
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['email'], self.config['password'])
                server.send_message(msg)
            
            logging.info(f"Email sent to {recipient_email}")
            return True
        except Exception as e:
            logging.error(f"Failed to send to {recipient_email}: {e}")
            return False
    
    def send_bulk_emails(self):
        logging.info("Starting bulk email sending...")
        success_count = 0
        total_count = len(self.users)
        
        for user in self.users:
            if self.send_email(user['email'], user['name']):
                success_count += 1
            time.sleep(1) 
            
        logging.info(f"Completed: {success_count}/{total_count} emails sent")
        return success_count
    
    def scheduled_task(self):
        logging.info("Executing scheduled task")
        self.send_bulk_emails()
    
    def show_menu(self):
        print("\n" + "="*50)
        print("EMAIL NOTIFICATION SYSTEM")
        print("="*50)
        print("\n1. Send test email")
        print("2. Send to all users")
        print("3. Start scheduled service")
        print("4. Test SMTP connection")
        print("5. Exit")
    
    def run(self):
        while True:
            self.show_menu()
            choice = input("\nSelect option: ")
            
            if choice == '1':
                email = input("Enter email: ")
                name = input("Enter name: ")
                self.send_email(email, name)
            
            elif choice == '2':
                self.send_bulk_emails()
            
            elif choice == '3':
                schedule_time = self.config.get('schedule_time', '09:00')
                schedule.every().day.at(schedule_time).do(self.scheduled_task)
                
                print(f"\nService started. Sending at {schedule_time} daily")
                print("Press Ctrl+C to stop\n")
                
                self.scheduled_task()
                
                try:
                    while True:
                        schedule.run_pending()
                        time.sleep(60)
                except KeyboardInterrupt:
                    print("\nService stopped")
            
            elif choice == '4':
                if self.test_connection():
                    print("✓ SMTP connection successful")
                else:
                    print("✗ SMTP connection failed")
            
            elif choice == '5':
                print("Goodbye!")
                break
            
            else:
                print("Invalid option")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    notifier = EmailNotifier()
    notifier.run()
