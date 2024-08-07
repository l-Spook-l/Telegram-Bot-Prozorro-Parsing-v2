import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiofiles
import aiosmtplib
from dotenv import load_dotenv
from .create_HTML import create_HTML

load_dotenv()


async def send_email(data: list):
    await create_HTML(data)
    for i in range(len(data)):

        sender = os.getenv('EMAIL')
        recipient = data[i]['Пошта']
        password = os.getenv('PASSWORD')

        try:
            async with aiofiles.open(f"index_{i + 1}.html", encoding='utf-8', mode='r') as file:
                template = await file.read()
        except IOError:
            return "The template"

        message = MIMEMultipart("alternative")
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = "Список тендерів за вашими параметрами"
        message.attach(MIMEText(template, "html", "utf-8"))
        await aiosmtplib.send(message, hostname="smtp.gmail.com", port=465, use_tls=True, username=sender,
                              password=password)

        print('Message sent successfully')
