#!/usr/bin/env python

import time, sys, inspect, os

path = os.path.dirname(inspect.getfile(inspect.currentframe()))
sys.path.insert(1, os.path.join(path, '..', '..', '..', 'Tools'))
sys.path.extend([os.path.join(path, '..', '..', 'DFE_Injector')])

from main.main import deterDFE
from MbedTools import MbedTools
from SendEmail import SendEmail

# Email class for send result of test
class BlinkyEmail(SendEmail):

	send_from = "martin.adamec@student.kuleuven.be"

	def addFiles(self, msg):
		self.addXlsxFile(
			msg, 
			"resultsDeterDFE.xlsx", 
			os.path.join(path, '..', '..', "..", "resultsDeterDFE.xlsx")
		)


# Copy file to target adn restart
inst = MbedTools(sys.argv[1:])
testFilename = inst.copy(True)
time.sleep(1)

try:
	deterDFE("Test", 1)
	mail = BlinkyEmail("Deter DFE test", "The result in XLSX file.")
	mail.send("martin.adamec@student.kuleuven.be")
except Exception as e:
	raise # re-raise the error
finally:
	try:
		os.remove(testFilename)
		inst.restartMbed()
		os.remove(os.path.join(path, '..', '..', "..", "resultsDeterDFE.xlsx"))
	except OSError:
		pass
