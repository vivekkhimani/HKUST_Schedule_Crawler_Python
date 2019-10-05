import requests
from bs4 import BeautifulSoup
import validators



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
		soup_object = BeautifulSoup(plain_text,"html.parser")

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

		plain_text = source_code.text
		soup_object = BeautifulSoup(plain_text,"html.parser")
		
		section_headers = ""
		for section_headers in soup_object.findAll('a',{'name': appended_class_name}):
			section_headers = str(section_headers)
			print("Class Found!")
			valid = True
			return new_term_url,appended_class_name

		if section_headers == "":	
			print("Class Not Found! There might be some error with the COURSE NUMBER. Either it isn't provided this term or doesn't exist at all.\n")


def getClassDetails(updated_class_url,class_name):
	course_dict = {}
	source_code = requests.get(updated_class_url)
	plain_text = source_code.text
	soup_object = BeautifulSoup(plain_text,"html.parser")


	sect_head = soup_object.find('a',{'name': class_name})
	main_course_div = sect_head.parent.parent

	#Item 3 gives course description table
	#Item 5 gives course header -- DICT DONE
	#Item 7 gives sections table

	#course_name added to dictionary
	course_name = str(list(main_course_div.children)[5].string)
	course_dict['course_name'] = course_name

	#course_info added to dictionary
	course_info_in_list = list(main_course_div.children)[3].table.findAll('th')
	course_info_op_list = list(main_course_div.children)[3].table.findAll('td')
	course_dict['course_info'] = {} 
	for i in range(len(course_info_in_list)):
		loc_key = str(course_info_in_list[i].string)
		course_dict['course_info'][loc_key] = str(course_info_op_list[i].string)

	#course sections added to dictionary
	sections_details_list = list(main_course_div.children)[7].findAll('td')
	course_dict['course_sections']={}
	curr_section = None

	for i in range(len(sections_details_list)):
		req_str = str(sections_details_list[i].string)

		if (req_str[0] == "L" or req_str[0] == "T") and ((req_str[1] == "A" and req_str[2].isdigit()) or req_str[1].isdigit()):
			course_dict['course_sections'][req_str] = []
			curr_section = req_str
			continue

		else:
			if len(course_dict['course_sections'][curr_section]) >= 7:
				continue
			course_dict['course_sections'][curr_section].append(req_str)

	#returned course_dict
	#print(course_dict)
	return course_dict

def printDict(course_dictionary):
	section_corr_list = ["Day & Time","Room","Instructor","Quota","Enrolled","Avail","Waitlist"]
	print("**** PLEASE FIND YOUR REQUIRED INFO****\n\n")
	for vals in course_dictionary.keys():
		if vals == 'course_name':
			print("Course Name:",course_dictionary[vals],"\n")

		if vals == 'course_info':
			for lols in course_dictionary[vals].keys():
				print(lols,course_dictionary[vals][lols],"\n")

		if vals == 'course_sections':
			for items in course_dictionary[vals].keys():
				counter = 0
				print("\n")
				print("Section :",items)
				for more_lols in course_dictionary[vals][items]:
					print(section_corr_list[counter],":",more_lols,end=" ")
					counter+=1

url,classN = gettingClassInput(gettingTermInput())
#getClassDetails('https://w5.ab.ust.hk/wcq/cgi-bin/1910/subject/COMP','COMP4900')

printDict(getClassDetails(url,classN))
