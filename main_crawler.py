import requests
from bs4 import BeautifulSoup
import validators
from datetime import date

#ALREADY TESTED - DO MORE TESTING LATER ON
#We will get inputs for the TERM and YEAR from the users so that we can fetch the webpage accordingly.
#Based on the way in which the term pages are stored, we will use it for error handling.


def gettingTermInput():
	valid = False

	while valid != True:
		complete_url = ""
		seasonal_dict = {'FALL':'10','WINTER':'20','SPRING':'30','SUMMER':'40'}
		yearValid = False
		seasonValid = False
		urlExist = False
		dataExist = False

		term_input = input("Please Enter Your Term of Interest in the following format (FALL-2018):\n")
			
		
		if "-" not in term_input:
			print("Badly Formatted. Check for the -")
			continue

		term_input_split = term_input.split("-")

		if term_input_split[1].isdigit() and len(term_input_split[1])==4:
			yearValid = True
			if term_input_split[0].upper() in seasonal_dict:
				seasonValid = True 
				complete_url = "https://w5.ab.ust.hk/wcq/cgi-bin/"+str(term_input_split[1][-2:])+str(seasonal_dict.get(term_input_split[0].upper()))+"/"
					
				if validators.url(complete_url):
					urlExist = True
		try:
			source_code = requests.get(complete_url)
			if dataExist:
				valid = True
				return complete_url
		except:
			if not yearValid:
				print("INVALID URL. Seems like a problem with the year entry.\n")
				continue
			if not seasonValid:
				print('INVALID URL. Seems like a problem with the season entry.\n')
				continue
			if not urlExist:
				print('INVALID URL. Please check it again. Reason unknown.\n')
				continue

		plain_text = source_code.text
		soup_object = BeautifulSoup(plain_text)

		check_url = "/wcq/cgi-bin/"+str(term_input_split[1][-2:])+str(seasonal_dict.get(term_input_split[0].upper()))+"/"
		for terms in soup_object.findAll('div',{'class': 'termselect'}):
			terms = str(terms)
			if check_url in terms:
				dataExist = True
				valid = True
				return complete_url
			else:
				print("Entered entry is valid but data doesn't exist.\n")
				break

	
#print(gettingTermInput())

#ALREADY PRIMARY TESTS DONE. Definitely test more towards the end.
#Now we will get the inputs for the class of interest once the term is validated. The validated term will provide us a url for the appropriate term. 
def gettingClassInput(term_url):
	valid = False
	class_input = ""

	while valid != True:
		class_input = input("Please Enter Your Class of interest in the following format(ACCT 2010):\n")

		if " " not in class_input:
			print("Badly formatted input. Check for spaces.")
			continue

		class_split = class_input.split(" ")
		new_term_url = term_url+"subject/"+class_split[0]
		#print(new_term_url)
		try:
			source_code = requests.get(new_term_url)
		except:
			print("INVALID SUBJECT SELECTION.")

		appended_class_name = class_split[0]+class_split[1]
		#print(appended_class_name)
		plain_text = source_code.text
		soup_object = BeautifulSoup(plain_text)
		
		section_headers = ""
		for section_headers in soup_object.findAll('a',{'name': appended_class_name}):
			section_headers = str(section_headers)
			print("Class Found!")
			valid = True
			return new_term_url,appended_class_name

		if section_headers == "":	
			print("Class Not Found! There might be some error with the COURSE NUMBER. Either it isn't provided this term or doesn't exist at all.\n")


#gettingClassInput(gettingTermInput())

#A NEW FUNCTION TO FURTHER PARSE THE DETAILS OF THE CLASS
#THIS FUNCTION is only executed if the course is available in the required term. We already check that in the previous function.

def getClassDetails(updated_class_url,class_name):
	source_code = requests.get(updated_class_url)
	plain_text = source_code.text
	soup_object = BeautifulSoup(plain_text)

	for courses in soup_object.findAll('div',{'class': 'course'}):
		print(type(courses))
		#print(str(courses))
		#print("************")


url,classN = gettingClassInput(gettingTermInput())
getClassDetails(url,classN)
