import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ReviewEmailNotifier:
    def __init__(self, smtp_config):
        self.smtp_config = smtp_config

    def send_review_notification(self, team_members, review_date):
        subject = f"Scheduled System Review - {review_date}" 
        body = f"Team,

We have a bi-weekly system review scheduled for {review_date} at 10:00 AM UTC.

Agenda:
1. Performance baseline update
2. Security configuration audit
3. Debt triage
4. Next steps planning

Please come prepared with relevant system metrics and observations.

Best regards,
Your Review Bot" 
        
        message = MIMEMultipart()
        message['From'] = self.smtp_config['from_email']
        message['To'] = ', '.join(team_members)
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(self.smtp_config['smtp_host'], self.smtp_config['smtp_port'])
            server.starttls()
            server.login(self.smtp_config['from_email'], self.smtp_config['from_password'])
            server.sendmail(self.smtp_config['from_email'], team_members, message.as_string())
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")