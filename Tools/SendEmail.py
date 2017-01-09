#!/usr/bin/env python

import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

class SendEmail:

	# E-mail variables
	subject = None
	text = None
	send_from = "noreply@kuleuven.be"

	# SMTP setting
	localhost = False
	username = 'remikuleuven@gmail.com'
	password = 'Remi2016'
	smtp_server = 'smtp.gmail.com:587'


	## Constructor
	# @param  string  subject  The subject of the e-mail
	# @param  string  text     The text of the e-mail
	def __init__(self, subject = None, text = None):
		self.subject = subject
		self.text = text

	## Setter for variable 'subject'
	# @param  string  subject 
	def setSubject(self, subject):
		self.subject = subject


	## Setter for variable 'text'
	# @param  string  text 
	def setText(self, text):
		self.text = text


	## Attach XLSX file to mail
	# @param  object  msg       Object of 'MIMEMultipart'
	# @param  string  filename  Name of the file in email
	# @param  string  path      Full path to the file
	def addXlsxFile(self, msg, filename, path):
		part = MIMEBase('application', "octet-stream")
		part.set_payload(open(path, "rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="' + filename + '"')
		msg.attach(part)


	## Method for create new email and send
	# @param  string  send_to  E-mail address of recipient
	def send(self, send_to):
		msg = MIMEMultipart()
		msg['From'] = self.send_from
		msg['To'] = send_to
		msg['Date'] = formatdate(localtime = True)
		msg['Subject'] = self.subject
		msg.attach(MIMEText(self.text))

		# Add attachemnts
		self.addFiles(msg)

		# establish SMTP
		smtp = self.establishSMTP()
		smtp.sendmail(self.send_from, send_to, msg.as_string())
		smtp.quit()


	## Method for attach files
	# @param  object  msg  Object of 'MIMEMultipart'
	def addFiles(self, msg):
		pass


	## Establish SMTP connection
	def establishSMTP(self):
		if self.localhost:
			return smtplib.SMTP("localhost")
		else:
			server = smtplib.SMTP(self.smtp_server)
			server.ehlo()
			server.starttls()
			server.login(self.username, self.password)
			return server
