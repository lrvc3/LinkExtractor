from selenium import webdriver
from bs4 import BeautifulSoup
import os

# load the driver
browser = webdriver.Chrome("C:\\Users\\I518730\\Downloads\\chromedriver_win32\\chromedriver.exe")

# url
login_url = "https://idp.bits-pilani.ac.in/idp/Authn/UserPassword"

# credentials
user_name = os.environ.get('B_USERNAME')
user_password = os.environ.get('B_PASSWORD')

browser.get(login_url)

# Fetch input fields and submit button
username_field = browser.find_element_by_id("username")
password_field = browser.find_element_by_id("pass")
submit_btn = browser.find_element_by_id("submitbtn")

# send input
username_field.send_keys(user_name)
password_field.send_keys(user_password)
submit_btn.click()

# Access the dashboard
browser.get("http://taxila-aws.bits-pilani.ac.in/my/")

# Get the source code of the page
dashboard = browser.page_source

#
soup = BeautifulSoup(dashboard, 'html.parser')

# Finding all divs with class course_title
course_list = soup.find_all('div',{"class":"course_title"})

# courses = ["Courseware - Data Warehousing", "Courseware - Software Testing Methodologies", "Courseware - Software Architectures",
#            "Courseware - Secure Software Engineering"]

# list of courses
course_titles = ["Courseware - Data Warehousing", "Courseware - Software Testing Methodologies", "Courseware - Software Architectures",
                 ]

# A list to store the course links
course_links = []

# Retrieve the links present on the page for each course
for c in course_list:
    try:
        if c.find('a').get("title") in course_titles:
            course_links.append(c.find('a').get('href'))
    except TypeError:
        pass

# v = []
with open("links.txt", "a") as f:
    for index, val in enumerate(course_links):

        # Write course title to the file
        f.write(course_titles[index] + "\n")

        browser.get(val)

        course_page = browser.page_source

        s2 = BeautifulSoup(course_page, 'html.parser')
        topics = s2.find('ul', {'class': 'topics'})

        main_modules = topics.find_all('li', {'class': 'activity page modtype_page'})
        modules = []
        for mm in main_modules:
            modules.append(mm.find('div', {'class': 'activityinstance'}))

        mlinks = []
        for m in modules:
            mlinks.append(m.find('a').get('href'))

        for l in mlinks:
            browser.get(l)
            s3 = browser.page_source
            t = BeautifulSoup(s3, 'html.parser')

            # Writing to the file in the format:- title - link
            heading = t.find('span', {'class': 'nolink'}).find_next('strong').text.split(':')[0]
            url = t.find('iframe')['src']
            string = heading + " - " + url + "\n"
            f.write(string)

            # v.append([t.find('span', {'class': 'nolink'}).find_next('strong').text, t.find('iframe')['src']])


browser.close()





# # SSE
# browser.get(course_links[3])
#
# coursepage = browser.page_source
#
# s2 = BeautifulSoup(coursepage, 'html.parser')
# topics = s2.find('ul', {'class': 'topics'})
#
# main_modules = topics.find_all('li', {'class': 'activity page modtype_page'})
# modules = []
# for mm in main_modules:
#     modules.append(mm.find('div', {'class': 'activityinstance'}))
#
# mlinks = []
# for m in modules:
#     mlinks.append(m.find('a').get('href'))
#
# v = []
# for l in mlinks:
#     browser.get(l)
#     s3 = browser.page_source
#     t = BeautifulSoup(s3, 'html.parser')
#     print(t.prettify())
#     v.append([t.find('span', {'class': 'item-content-wrap'}).text, t.find('iframe')['src']])
#
# for a in v:
#     print(a)

# browser.get(mlinks[0])
# s3 = browser.page_source
# t = BeautifulSoup(s3, 'html.parser')
# print(t.prettify())
# print(t.find('span', {'class': 'nolink'}).find_next('strong').text)
# l = t.find_all('iframe')['src']
# print(l)



# sem2 = []
# for c in course_list:
#     if len(sem2) == 4:
#         break
#     else:
#         sem2.append(c)

# browser.close()
# id - course_list
# course-202 - Data Warehousing
# course-127 - Software Testing Methodologies
# course-199 - Software Architectures
# course-1584 -  Secure Software Engineering


# section-content-ul (section img-text)- div (activityinstance) -a

# ytp-large-play-button ytp-button