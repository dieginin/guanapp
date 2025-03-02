import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import G_PASSWORD
from models import Quote, Response

email = "guanas.mb@gmail.com"
password = G_PASSWORD or ""


def attach_file(msg: MIMEMultipart, filepath: str) -> None:
    filename = filepath.split("/")[-1]
    with open(filepath, "rb") as file:
        part = MIMEApplication(file.read(), Name=filename)
        part["Content-Disposition"] = f"attachment; filename={filename}"
        msg.attach(part)


class Email:
    @staticmethod
    def send_email(quote: Quote, filepath: str) -> Response:
        customer_email = quote.customer.email

        if customer_email:
            body = f"""Buenas Tardes {quote.customer.name.split()[0]},

Te hago llegar la cotización solicitada, quedo a tus ordenes

Saludos"""

            msg = MIMEMultipart()
            msg["From"] = email
            msg["To"] = customer_email
            msg["Subject"] = f"Cotización {quote.folio} - {quote.customer.name}"
            msg.attach(MIMEText(body))
            attach_file(msg, filepath)

            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                    smtp.login(email, password)
                    smtp.sendmail(email, customer_email, msg.as_string())
                return Response("Success", f"Correo enviado a {customer_email}")
            except:
                return Response("Error", f"Error al enviar el correo")
        else:
            return Response("Error", f"El cliente no tiene correo registrado")
