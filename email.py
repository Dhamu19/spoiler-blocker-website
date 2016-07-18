from smtplib import SMTP                        # for sending the email
from email.mime.multipart import MIMEMultipart  # for generating the message container
from email.mime.text import MIMEText            # for reading the html


from_addr = "EMAIL@EMAIL.COM"
PASSWORD = "PASSWORD"
to_addr = ["kabirk@live.com"]
HTML_TEMPLATE = """\
			<html>
			<body>
			<a href="{0}">Event page</a>
			</body>
			</html>
			""".format("VALUE")


# Sends an email using the SMTP protocol
def send_email(from_addr, to_addr, subject, content_html):
	msg = MIMEMultipart()
	msg['From'] = from_addr
	msg['To'] = ", ".join(to_addr)
	msg['Subject'] = subject
	msg.attach(MIMEText(content_html, 'html'))		# add the html body of the email to the msg container

	mail = SMTP('smtp.gmail.com', 587)
	mail.starttls()					# start a secure connection
	mail.login(from_addr, PASSWORD)
	mail.sendmail(from_addr, to_addr, msg.as_string())
	mail.quit()