__author__ = 'Alex Beals'

import requests, re, urllib, shutil
from PIL import Image
requests.packages.urllib3.disable_warnings()

landingPage = 'https://login.dartmouth.edu/cas/login?service=https://banner.dartmouth.edu/banner/groucho/twbkwbis.P_WWWLoginWEBAUTH'
user = 'https://websso.dartmouth.edu:443/oaam_server/login.do'
passw = 'https://websso.dartmouth.edu:443/oaam_server/password.do'
finalLogin = 'https://banner.dartmouth.edu/banner/groucho/twbkwbis.P_ValLoginWEBAUTH'

cookie = {'domain':'banner.dartmouth.edu','name':'TESTID','value':'TESTID','path':'/banner/groucho','secure':False}

redirect = {"Referer": "https://banner.dartmouth.edu/banner/groucho/twbkwbis.P_GenMenu?name=bmenu.Z_UGSMainMenu"}
browser = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}

def write_text(text, string):
	with open(string + ".html", "w") as f:
		f.write(text.encode('utf-8'))

class BannerConnection:
	def __init__(self):
		with requests.Session() as c:
			init = c.get(landingPage, verify=False) # initializes the headers, cookies

			self.session = c
			self.loggedin = False

	# Attempts to log you into Banner.  If it works, the self variable 'loggedin' is set to True.  Else, it's set to False.
	def login(self, username, password):
		if not self.loggedin:
			payload={'userid':username,'clientOffset':-4}
			request = self.session.post(user, data=payload, verify=False)
			if 'login.do' in request.url:
				payload={'fk':re.search("name=\"fk\" value=\"(.*?)\"",request.text).group(1),'Bharosa_Password_PadDataField':password}
				request = self.session.post(passw, data=payload, verify=False)

				# Handles the challenge question
				if 'challenge' in request.url:
					print "Challenge!"
					question_url = "https://websso.dartmouth.edu/oaam_server/" + re.search("bImgLoc:\"(.*?)\"",request.text).group(1)

					# Download the challenge question as an image, and open it
					response = self.session.get(question_url, stream=True)
					with open("challenge.png", "wb") as out_file:
						shutil.copyfileobj(response.raw, out_file)

					i = Image.open("challenge.png")
					i.show()

					ans = raw_input("What's the answer?  ")
					i.close()

					# Handle response
					payload = {'Bharosa_Challenge_PadDataField':ans,'fk':re.search("name=\"fk\" value=\"(.*?)\"",request.text).group(1),"showView":"submitAnswer"}
					request = self.session.post(request.url, data=payload, verify=False)
					if 'ticket' in request.url:
						self.loggedin = True
						self.session.cookies.set(**cookie) # Fakes the javascript
						finalRequest = self.session.get(finalLogin, verify=False)
					else:
						self.loggedin = False
				else:
					self.loggedin = True
					self.session.cookies.set(**cookie) # Fakes the javascript
					finalRequest = self.session.get(finalLogin, verify=False)
			else:
				self.loggedin = False

	# Logs you out of banner.
	def logout(self):
		if self.loggedin:
			self.__init__() # Reinitialize

	# Returns your GPA as a float, or False if you're not logged in
	def gpa(self):
		if self.loggedin:
			page = self.session.get('https://banner.dartmouth.edu/banner/groucho/zwskogru.P_ViewTermGrde', headers=redirect)
			year = re.search("VALUE=\"(.*?)\" SELECTED",page.text).group(1)

			page2 = self.session.post('https://banner.dartmouth.edu/banner/groucho/zwskogru.P_ViewGrde', data={'term':year}, headers=redirect)

			return float(re.search("(?s).*<p class=\"rightaligntext\">\s*(.*?)</p>",page2.text).group(1))
		else:
			return False

	# Returns your DBA as a float, or False if you're not logged in
	def dba(self):
		if self.loggedin:
			page = self.session.get('https://banner.dartmouth.edu/banner/groucho/kap_ar_dash.entry_point', headers=redirect)
			return float(re.search("Dining DBA[\s\S]*?<TD>(.*?)</TD>",page.text).group(1))
		else:
			return False

	# Attempts to enroll you in a course.  Given various responses, it returns different things:
	#	You're not logged in : 0
	#	It worked! : 1
	#	You already have three courses : 2
	#	It's an incorrect id : 3
	#	You don't satisfy the banner prerequisites : 4
	#	The enrollment limit is reached : 5
	#	You're already in the class : 6
	#	Need instructor permission : 7
	#	Misc error : 8
	def addCourse(self, courseID):
		timetable = 'https://banner.dartmouth.edu/banner/groucho/zp_web_add_drop.pz_timetable'
		if self.loggedin:
			page = self.session.get(timetable, headers=redirect)
			term = re.search("<INPUT TYPE = \"radio\".*?ID=\"(.*?)\".*?CHECKED",page.text).group(1)
			term = "201606"
			page2 = self.session.post(timetable, headers=redirect, data={"term":term})

			classData = "term_in=" + term + "&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&RSTS_IN=RW&CRN_IN=" + str(courseID) + "&assoc_term_in=&start_date_in=&end_date_in=&regs_row=0&wait_row=0&add_row=1&REG_BTN=Submit+Changes"
			submit = self.session.post('https://banner.dartmouth.edu/banner/groucho/bwckcoms.P_Regs', data=classData, headers=redirect)

			if "Maximum number of courses exceeded" in submit.text:
				return 2 # already have three classes
			elif "Error occurred while processing registration changes" in submit.text:
				return 3 # invalid course ID
			elif "Prerequisite not met" in submit.text:
				return 4 # insufficient prerequisites
			elif "Enrollment Limit Reached" in submit.text:
				return 5 # filled up
			elif "DUPLICATE " in submit.text:
				return 6 # already enrolled
			elif "Instructor Permission Needed" in submit.text:
				return 7
			elif "Registration Add Errors" in submit.text:
				return 8 # misc error
			else:
				return 1 #success!
		else:
			return 0 # you're not logged in

	# Attempts to drop you from a course.  Given various responses, it returns different things:
	#	You're not logged in : 0
	#	It worked! : 1
	#	You're not enrolled in that class : 2
	#	Misc error : 3
	def dropCourse(self, courseID):
		timetable = 'https://banner.dartmouth.edu/banner/groucho/zp_web_add_drop.pz_timetable'
		if self.loggedin:
			page = self.session.get(timetable, headers=redirect)
			term = re.search("<INPUT TYPE = \"radio\".*?ID=\"(.*?)\".*?CHECKED",page.text).group(1)
			term = "201606"
			page2 = self.session.post(timetable, headers=redirect, data={"term":term})

			classData = "term_in=" + term + "&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&MESG=DUMMY&RSTS_IN=DW&assoc_term_in=" + term + "&CRN_IN=" + str(courseID) + "&regs_row=1&wait_row=0&add_row=0&REG_BTN=Submit+Changes"
			submit = self.session.post('https://banner.dartmouth.edu/banner/groucho/bwckcoms.P_Regs', data=classData, headers=redirect)

			if "Can not drop a course which has not been registered" in submit.text:
				return 2 # you're not enrolled
			elif "Registration Add Errors" in submit.text:
				return 3 # misc error
			else:
				return 1 # success!
		else:
			return 0 # not logged in