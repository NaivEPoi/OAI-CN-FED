#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *   http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *   contact@openairinterface.org
# */
#---------------------------------------------------------------------

import os
import re
import sys
import subprocess

class HtmlReport():
	def __init__(self):
		self.job_name = ''
		self.job_id = ''
		self.job_url = ''
		self.job_start_time = 'TEMPLATE_TIME'

	def generate(self):
		cwd = os.getcwd()
		self.file = open(cwd + '/ds_tester_results_oai_cn5g.html', 'w')
		self.generateHeader()

		finalStatus = self.testSummaryHeader()
		self.testSummaryDetails()
		self.testSummaryFooter()

		self.generateFooter()
		self.file.close()

		if finalStatus:
			sys.exit(0)
		else:
			sys.exit(-1)

	def generateHeader(self):
		# HTML Header
		self.file.write('<!DOCTYPE html>\n')
		self.file.write('<html class="no-js" lang="en-US">\n')
		self.file.write('<head>\n')
		self.file.write('  <meta name="viewport" content="width=device-width, initial-scale=1">\n')
		self.file.write('  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">\n')
		self.file.write('  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
		self.file.write('  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n')
		self.file.write('  <title>OAI 5G Core Network Test Results for ' + self.job_name + ' job build #' + self.job_id + '</title>\n')
		self.file.write('</head>\n')
		self.file.write('<body><div class="container">\n')
		self.file.write('  <table width = "100%" style="border-collapse: collapse; border: none;">\n')
		self.file.write('   <tr style="border-collapse: collapse; border: none;">\n')
		self.file.write('	<td style="border-collapse: collapse; border: none;">\n')
		self.file.write('	  <a href="http://www.openairinterface.org/">\n')
		self.file.write('		 <img src="http://www.openairinterface.org/wp-content/uploads/2016/03/cropped-oai_final_logo2.png" alt="" border="none" height=50 width=150>\n')
		self.file.write('		 </img>\n')
		self.file.write('	  </a>\n')
		self.file.write('	</td>\n')
		self.file.write('	<td style="border-collapse: collapse; border: none; vertical-align: center;">\n')
		self.file.write('	  <b><font size = "6">Job Summary -- Job: ' + self.job_name + ' -- Build-ID: <a href="' + self.job_url + '">' + self.job_id + '</a></font></b>\n')
		self.file.write('	</td>\n')
		self.file.write('   </tr>\n')
		self.file.write('  </table>\n')
		self.file.write('  <br>\n')

	def generateFooter(self):
		self.file.write('  <div class="well well-lg">End of Test Report -- Copyright <span class="glyphicon glyphicon-copyright-mark"></span> 2020 <a href="http://www.openairinterface.org/">OpenAirInterface</a>. All Rights Reserved.</div>\n')
		self.file.write('</div></body>\n')
		self.file.write('</html>\n')

	def testSummaryHeader(self):
		self.file.write('  <h2>DS Tester Summary</h2>\n')

		finalDsTesterSummaryFile = 'DS-TEST-RESULTS/status.txt'
		cwd = os.getcwd()
		if os.path.isfile(cwd + '/' + finalDsTesterSummaryFile):
			finalStatusOK = True
			with open(cwd + '/' + finalDsTesterSummaryFile, 'r') as finalLog:
				for line in finalLog:
					line = line.strip()
					result = re.search('FAILED', line)
					if result is not None:
						finalStatusOK = False
			finalLog.close()

			if finalStatusOK:
				self.file.write('  <div class="alert alert-success">\n')
				self.file.write('	<strong>Successful DsTester suite! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
				self.file.write('  </div>\n')
			else:
				self.file.write('  <div class="alert alert-danger">\n')
				self.file.write('	<strong>Failed DsTester suite! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
				self.file.write('  </div>\n')
		else:
			self.file.write('  <div class="alert alert-warning">\n')
			self.file.write('	<strong>LogFile not available! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
			self.file.write('  </div>\n')
		return finalStatusOK

	def testSummaryFooter(self):
		self.file.write('  <br>\n')

	def testSummaryDetails(self):
		self.file.write('  <br>\n')
		self.file.write('  <button data-toggle="collapse" data-target="#ds-tester-details">More details on DsTester results</button>\n')
		self.file.write('  <div id="ds-tester-details" class="collapse">\n')
		self.file.write('  <table class="table-bordered" width = "60%" align = "center" border = 1>\n')
		self.file.write('	 <tr bgcolor = "#33CCFF" >\n')
		self.file.write('	   <th>Test Name</th>\n')
		self.file.write('	   <th>Test Status</th>\n')
		self.file.write('	   <th>Test Details</th>\n')
		self.file.write('	 </tr>\n')
		dsTesterDetailsLog = 'archives/run-5g-dstester.log'
		cwd = os.getcwd()
		if os.path.isfile(cwd + '/' + dsTesterDetailsLog):
			testName = ''
			testDetails = '<pre style="background-color:white">\n'
			with open(cwd + '/' + dsTesterDetailsLog) as detailsLog:
				for line in detailsLog:
					line = line.strip()
					result = re.search('CHECKED condition|FAILED condition', line)
					if result is not None:
						details = line.replace('Result String: ', '')
						details = details.replace('CHECKED condition ', '')
						details = details.replace('FAILED condition ', '')
						result = re.search('FAILED condition', line)
						if result is not None:
							testDetails += '<b>' + details + '</b>\n'
						else:
							testDetails += details + '\n'
					result = re.search('Running ', line)
					if result is not None:
						testName = line.replace('Running ', '')
					result = re.search('status:', line)
					if result is not None:
						self.file.write('	 <tr>\n')
						self.file.write('	   <td>' + testName + '</td>\n')
						result = re.search('FAILED', line)
						if result is not None:
							self.file.write('	   <td bgcolor = "Red"><b><font color="white">KO</font></b></td>\n')
						else:
							self.file.write('	   <td bgcolor = "DarkGreen"><b><font color="white">OK</font></b></td>\n')
						testDetails += '</pre>\n'
						self.file.write('	   <td>' + testDetails + '</td>\n')
						self.file.write('	 </tr>\n')
						testDetails = '<pre style="background-color:white">\n'
			detailsLog.close()
		else:
			print ('no details???')
		self.file.write('  </table>\n')
		self.file.write('  </div>\n')

def Usage():
	print('----------------------------------------------------------------------------------------------------------------------')
	print('dsTestGenerateHTMLReport.py')
	print('   Generate an HTML report for the Jenkins pipeline on oai-cn5g-fed.')
	print('----------------------------------------------------------------------------------------------------------------------')
	print('Usage: python3 generateHtmlReport.py [options]')
	print('  --help  Show this help.')
	print('---------------------------------------------------------------------------------------------- Mandatory Options -----')
	print('  --job_name=[Jenkins Job name]')
	print('  --job_id=[Jenkins Job Build ID]')
	print('  --job_url=[Jenkins Job Build URL]')

#--------------------------------------------------------------------------------------------------------
#
# Start of main
#
#--------------------------------------------------------------------------------------------------------

argvs = sys.argv
argc = len(argvs)

HTML = HtmlReport()

while len(argvs) > 1:
	myArgv = argvs.pop(1)
	if re.match('^\-\-help$', myArgv, re.IGNORECASE):
		Usage()
		sys.exit(0)
	elif re.match('^\-\-job_name=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-job_name=(.+)$', myArgv, re.IGNORECASE)
		HTML.job_name = matchReg.group(1)
	elif re.match('^\-\-job_id=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-job_id=(.+)$', myArgv, re.IGNORECASE)
		HTML.job_id = matchReg.group(1)
	elif re.match('^\-\-job_url=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-job_url=(.+)$', myArgv, re.IGNORECASE)
		HTML.job_url = matchReg.group(1)
	else:
		sys.exit('Invalid Parameter: ' + myArgv)

if HTML.job_name == '' or HTML.job_id == '' or HTML.job_url == '':
	sys.exit('Missing Parameter in job description')

HTML.generate()
