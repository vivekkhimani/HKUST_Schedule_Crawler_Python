# HKUST_Schedule_Crawler_Python

## Purpose of the Project:
- General/JustForFun/Personal

## Problem Description:
- HKUST (Hong Kong University of Science and Technology) is one of the most popular technical and business institute in Asia and entire world. As a result, all the classes are almost filled and it's not uncommon that students have to spend a lot of time tracking the waitlist quota and schedules on the website. Even I faced the similar problems while deciding on my classes. 

## Solution:
- As a result of the above problem, I decided to make a web crawler using Python that requires TERM and CLASS as an input and provides all details that a website would provide. This code can be integrated with any one of the HKUST apps (m.HKUST, HKUSThing) and can be used by the students to check the details of their classes instead of going to the website, finding the class, and manually checking it everytime. 

## Error Handling:
- As the code is extremely modular and divided in various functions, extensive ERROR HANDLING and ERROR CATCHING has been done inside the functions itself while taking the inputs from the users. Also, different kind of data in different courses and subjects have been considered and the code is written in such a way that it won't crash in any of those scenarios. Conditional testing and case-wise testing has been done and the screenshots can be found in the 'Screenshots' directory.

## Tools Used:
- The crawler has been primarily coded in Python3.6. The libraries included are - BeautifulSoup(v4) for crawling, requests, and validators for fetching and validating the webpage.

## Modules Required (can be installed using pip):
- requests
- validators
- bs4
## Time Required/Versions:
- This is the second version of the project and it's complete with most of the testing done by myself. I will keep on testing and updating the app as and when I get reviews from my fellow classmates and students. This entire version is put together in less than 4 hours.

## Next Steps:
- Once I am confident about the bug fixes and get positive reviews from the students, the next step is to demonstrate this concept to one of the HKUST application things. If they like it and find it usable in their respective apps, I would be happy to optimize it according to their needs and provide it to them.
