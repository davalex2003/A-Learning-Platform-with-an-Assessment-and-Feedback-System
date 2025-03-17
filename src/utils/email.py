import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json


def send_verification_code(email: str, code: str) -> bool:
    with open('configs/email.json', 'r') as f:
        params = json.load(f)
        sender_email = params['email']
        password = params['password']
        user = params['user']
        f.close()
    mes = MIMEMultipart()
    mes['From'] = sender_email
    mes['To'] = email
    mes['Subject'] = 'Код подтверждения'
    msg_text = MIMEText(f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Подтверждение регистрации</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }}
        .email-container {{
            max-width: 600px;
            margin: 50px auto;
            background-color: #ffffff;
            border: 1px solid #dddddd;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .email-header {{
            background-color: #42A5F5;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            font-size: 24px;
        }}
        .email-body {{
            padding: 20px;
        }}
        .email-footer {{
            background-color: #f1f1f1;
            color: #555555;
            text-align: center;
            padding: 10px;
            font-size: 12px;
        }}
    </style>
</head>
<body>

<div class="email-container">
    <div class="email-header">
        Подтверждение регистрации
    </div>
    <div class="email-body">
        <p>Здравствуйте!</p>
        <p>Одноразовый код для подтверждения регистрации аккаунта в приложении SmartGrade:</p>
        <p style="font-size: 20px; font-weight: bold; color: #42A5F5;">{code}</p>
    </div>
    <div class="email-footer">
        Это автоматическое сообщение, пожалуйста, не отвечайте на него.
    </div>
</div>

</body>
</html>
""", 'html')
    mes.attach(msg_text)
    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.ehlo(email)
    server.login(user, password)
    server.auth_plain()
    try:
        server.sendmail(sender_email, email, mes.as_string())
        server.quit()
        return True
    except Exception as e:
        server.quit()
        return False
