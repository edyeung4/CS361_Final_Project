from socket import SOCK_DGRAM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


class WebDriver:

	location_data = {}

	def __init__(self):
		self.PATH = "C:/Users/Edwardnese/Downloads/chromedriver_win32/chromedriver.exe"
		self.options = Options()
		# self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
		self.options.add_argument("--headless")
		self.driver = webdriver.Chrome(self.PATH, options=self.options)

		self.location_data["rating"] = "NA"
		self.location_data["reviews_count"] = "NA"
		self.location_data["location"] = "NA"
		self.location_data["contact"] = "NA"
		self.location_data["website"] = "NA"
		self.location_data["Time"] = {"Monday": "NA", "Tuesday": "NA", "Wednesday": "NA",
		    "Thursday": "NA", "Friday": "NA", "Saturday": "NA", "Sunday": "NA"}
		self.location_data["Reviews"] = []
		self.location_data["Popular Times"] = {"Monday": [], "Tuesday": [
		    ], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}

	def click_open_close_time(self):

		if(len(list(self.driver.find_elements_by_class_name("cX2WmPgCkHi__section-info-hour-text"))) != 0):
			element = self.driver.find_element_by_class_name(
			    "cX2WmPgCkHi__section-info-hour-text")
			self.driver.implicitly_wait(5)
			ActionChains(self.driver).move_to_element(element).click(element).perform()

	def click_all_reviews_button(self):

		try:
			WebDriverWait(self.driver, 20).until(
			    EC.presence_of_element_located((By.CLASS_NAME, "allxGeDnJMl__button")))

			element = self.driver.find_element_by_class_name("allxGeDnJMl__button")
			element.click()
		except:
			self.driver.quit()
			return False

		return True

	def get_location_data(self):

		try:
			avg_rating = self.driver.find_element_by_class_name("section-star-array")
			# total_reviews = self.driver.find_element_by_class_name("section-rating-term")
			address = self.driver.find_element_by_css_selector("[data-item-id='address']")
			# phone_number = self.driver.find_element_by_css_selector("[data-tooltip='Copy phone number']")
			# website = self.driver.find_element_by_css_selector("[data-item-id='authority']")
			print('hello')
			print(address.get_attribute('innerText'))

		except:
			# print('here')
			pass
		try:
			print('update is working?')
			# print(address.get_attribute('innerText'))
			# x = address.get_attribute('innerText')
			# print(x)
			self.location_data["rating"] = avg_rating.text
			# self.location_data["reviews_count"] = total_reviews.text[1:-1]
			self.location_data["location"] = address.get_attribute('innerText')
			print(self.location_data["location"])
			# self.location_data["contact"] = phone_number.text
			# self.location_data["website"] = website.text
		except:
			pass


	def get_location_open_close_time(self):

		try:
			days = self.driver.find_elements_by_class_name("lo7U087hsMA__row-header")
			times = self.driver.find_elements_by_class_name("lo7U087hsMA__row-interval")

			day = [a.text for a in days]
			open_close_time = [a.text for a in times]

			for i, j in zip(day, open_close_time):
				self.location_data["Time"][i] = j
		
		except:
			pass

	def get_popular_times(self):
		try:
			a = self.driver.find_elements_by_class_name("section-popular-times-graph")
			dic = {0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday"}
			l = {"Sunday":[], "Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[]}
			count = 0

			for i in a:
				b = i.find_elements_by_class_name("section-popular-times-bar")
				for j in b:
					x = j.get_attribute("aria-label")
					l[dic[count]].append(x)
				count = count + 1

			for i, j in l.items():
				self.location_data["Popular Times"][i] = j
		except:
			pass

	def scroll_the_page(self):
		try:
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))

			pause_time = 2
			max_count = 5
			x = 0

			while(x<max_count):
				scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
				try:
					self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
				except:
					pass
				time.sleep(pause_time)
				x=x+1
		except:
			self.driver.quit()

	def expand_all_reviews(self):
		try:
			element = self.driver.find_elements_by_class_name("section-expand-review")
			for i in element:
				i.click()
		except:
			pass

	def get_reviews_data(self):
		try:
			review_names = self.driver.find_elements_by_class_name("section-review-title")
			review_text = self.driver.find_elements_by_class_name("section-review-review-content")
			review_dates = self.driver.find_elements_by_css_selector("[class='section-review-publish-date']")
			review_stars = self.driver.find_elements_by_css_selector("[class='section-review-stars']")

			review_stars_final = []

			for i in review_stars:
				review_stars_final.append(i.get_attribute("aria-label"))

			review_names_list = [a.text for a in review_names]
			review_text_list = [a.text for a in review_text]
			review_dates_list = [a.text for a in review_dates]
			review_stars_list = [a for a in review_stars_final]

			for (a,b,c,d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
				self.location_data["Reviews"].append({"name":a, "review":b, "date":c, "rating":d})

		except Exception as e:
			pass

	def scrape(self, url):
		try:
			self.driver.get(url)
			print('im here')
		except Exception as e:
			self.driver.quit()
			# continue
		time.sleep(10)

		# self.click_open_close_time()
		self.get_location_data()
		# self.get_location_open_close_time()
		# self.get_popular_times()
		# if(self.click_all_reviews_button()==False):
			# continue
		    # time.sleep(5)
		# self.scroll_the_page()
		# self.expand_all_reviews()
		# self.get_reviews_data()
		self.driver.quit()

		return(self.location_data)

url = "https://www.google.com/maps/place/AF+Supply/@40.1408595,-74.4915335,8z/data=!4m9!1m2!2m1!1splumbers+near+07029!3m5!1s0x89c25387d0144d67:0xc278946f870c671c!8m2!3d40.7382148!4d-74.1597072!15sChNwbHVtYmVycyBuZWFyIDA3MDI5WhUiE3BsdW1iZXJzIG5lYXIgMDcwMjmSARVwbHVtYmluZ19zdXBwbHlfc3RvcmU"
x = WebDriver()
print(x.scrape(url))

# import sys
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import requests
# import time
# import pandas as pd
# from bs4 import BeautifulSoup


# #making a chrome drive and adding chrome driver options
# options = Options()
# options.page_load_strategy = 'eager'
# options.add_argument("--headless")
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# browser = webdriver.Chrome("C:/Users/Edwardnese/Downloads/chromedriver_win32/chromedriver.exe", options=options)


# all_page_urls = []     #to save the page urls
# business_pages =[]     #to save the business page url

# search_item = 'Hotel'  #you can change what your wanna search for
# location = 'London'    #change in which loaction you want to search

# base_url = "https://www.yelp.com/search?find_desc=" +search_item + "&find_loc="+location+"&start="  #main search page urls pattern

# def yelp_search_link():
#   for i in range(0,200,10):       #change here for your requirement
#     main_url = base_url+str(i)
#     all_page_urls.append(main_url)
#     print(main_url)
# yelp_search_link()

# def find_items_page():               #finding all business pages urls from main search page
#     for urls in all_page_urls:
#         browser.get(urls)
#         time.sleep(1)
#         soup = BeautifulSoup(browser.page_source, 'html.parser')
#         time.sleep(0.30)
#         mains = soup.find_all('div', class_ = 'container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')
#         main_url = 'https://www.yelp.com'
#         for main in mains:
#             a_tag = main.find('a', class_ = 'css-166la90').get('href')
#             a_tag_formated = main_url + str(a_tag)
#             items_pages.append(a_tag_formated)
#             print(a_tag_formated)
# find_items_page()

# Names = []            #Name of the business profile
# Reviews = []          #No of reviews recieved
# Open_Hour = []        #Open hours
# Price_range = []      #Price range
# Address = []          #Address of the business
# Websites = []         #Wbsites of the business
# Phones = []           #Phone number of the business


# def scrape_and_save():
#     for url in business_pages:
#         browser.get(url)
#         ss = BeautifulSoup(browser.page_source, 'html.parser')
#         mainPage = ss.find('div', class_ = 'main-content-wrap main-content-wrap--full')    #main content

#         try:
#             name = mainPage.find('h1', class_ = 'css-11q1g5y').get_text()
#             Names.append(name)
#         except AttributeError:
#             name = 'NUll'
#             Names.append(name)

#         try:
#             review = mainPage.find('span', class_ = 'css-bq71j2').get_text()
#             Reviews.append(review)
#         except AttributeError:
#             review = 'Null'
#             Reviews.append(review)

#         try:
#             price = mainPage.find('span', class_ = 'css-1xxismk').get_text()
#             Price_range.append(price)
#         except AttributeError:
#             price = 'Null'
#             Price_range.append(price)

#         try:
#             opens = mainPage.find('div', class_="display--inline-block__373c0__2de_K margin-r1-5__373c0__1Vie3 border-color--default__373c0__2oFDT")
#             find_next('span', class_ = 'css-bq71j2').get_text()
#             Open_Hour.append(opens)
#         except AttributeError:
#             opens = 'Null'
#             Open_Hour.append(opens)

#         try:
#             address = mainPage.find('div', class_ = 'css-1vhakgw border--top__373c0__19Owr border-color--default__373c0__2oFDT')
#             find_next('p', class_ = 'css-1h1j0y3').find_next('p', class_ = 'css-e81eai').get_text()
#             Address.append(address)
#         except AttributeError:
#             address = 'Null'
#             Address.append(address)
#         except TypeError:
#             address = 'Null'
#             Address.append(address)

#         try:
#             website = mainPage.find('a', class_ = 'css-ac8spe').get_text()
#             website = 'https://www.'+ str(website)
#             Websites.append(website)
#         except AttributeError:
#             website = 'Null'
#             Websites.append(website)

#         try:
#             phone = mainPage.find('div', class_ = 'stickySidebar__373c0__3PY1o border-color--default__373c0__2oFDT')
#             find('p', class_ = 'css-1h1j0y3').find_next('p', class_ = 'css-1h1j0y3').get_text()
#             Phones.append(phone)
#         except AttributeError:
#             phone = 'Null'
#             Phones.append(phone)

#         print('Scraping Compeleted',url)

#     df = pd.DataFrame({'Names':Names, 'Price Range': Price_range, 'Reviews': Reviews,
#                        'Address':Address, 'Website': Websites,'Phone Number': Phones})  #making a pandas dataframe
#     print(df)
#     # df.to_csv('Business Data.csv')   #Saving the data as csv
    
# scrape_and_save()
    
