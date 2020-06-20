
import datefinder
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait

from Amazon_Product import Amazon_Product
from Review_Question import Review_Question

import errno
import json
import os
from random import randint



#===================================================================
# Declaring variables
#===================================================================

timeout = 5

ASIN_ = 'B07MW4BR8D'  # this is a sample ASIN

Amazon_URL_ = 'https://www.amazon.com'

ASIN_baseURL_ = 'https://www.amazon.com/dp/'


full_URL = ASIN_baseURL_ + ASIN_

Rating_ = '★★★★★'

totalNumberOfReviews = 0

Positive_Reviews_Count = 0

Critical_Reviews_Count = 0

Amazon_Product_Data = []

Reviews_List = []

Questions_List = []

Questions_List = []

Amazon_Product_ = Amazon_Product()

Chrome_Driver_Path = r'.\chromedriver.exe'

headers_ = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}



# ==========================================================================================================
# Initiating Webdriver
# ==========================================================================================================
def initialize_WebDriver(Chrome_Driver_Path):

    print('- Initializing ...')

    options = webdriver.ChromeOptions()

    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_experimental_option("useAutomationExtension", True)
    options.add_argument('--disable-gpu')
    # to hide the browser
    options.add_argument('--headless')

    driver_ = webdriver.Chrome(executable_path = Chrome_Driver_Path, chrome_options=options)

    return driver_


# ==========================================================================================================
# Visiting main Link of a given ASIN
# ==========================================================================================================

def load_Procut_Page(url_,driver_):
    driver_.get(url_)

#==========================================================================================================
#bypassing nagging popup window for local country
#==========================================================================================================

def remove_Nagging_Window(driver_):
    while True:
        try:
            if driver_.switch_to.active_element:
                if WebDriverWait(driver_, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-main"]/div[1]/div[2]/div/div[3]/span[1]/span/input'))):
                    driver_.find_element_by_xpath('//*[@id="nav-main"]/div[1]/div[2]/div/div[3]/span[1]/span/input').click()
                    print('- Passed Nagging window for Country')
                    return True
                    # break

        except TimeoutException: #TimeoutException:
            print('- Still trying to pass Nagging window for Country')
            pass
            # print ("- ===> Timed out waiting for page to load")

#===========================================================================
# Now use the Main Product Page to get all teh Fields of Amazon_Product Object
# meaning all URLs required to visit , to save time going back and forth, or trying to find them using Selenium
#===========================================================================
# Loading the Product Page !!!
#===========================================================================
# scroll to the bottom in order to load all the page contents




def get_Product_Profile(driver_,ASIN_):

    driver_.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    _delay_(3)

    amazon_page_ = driver_.page_source

    Amazon_Product_ = Amazon_Product()


    if amazon_page_:
        # ===========================================================================
        # get Product Title
        # ===========================================================================
        soup_Main = BeautifulSoup(amazon_page_ ,"html.parser")
        Product_Title = soup_Main.find('div' , {'id':'title_feature_div'}).text.rstrip().lstrip()
        print('- got Product Title Successfully')

        # ===========================================================================
        # get All_reviews_link
        # ===========================================================================
        All_reviews_link = soup_Main.find('div', {'id': 'reviews-medley-footer'}).find('a')['href']
        All_reviews_link = Amazon_URL_ + All_reviews_link
        print('- got All_reviews_link Successfully , from Main Page of the product using Soup')

        # ===========================================================================
        # get All_Questions_link
        # ===========================================================================
        # All_Questions_link = soup_Main.find('div', {'class': 'a-section askTopQandALoadMoreQuestions'}).find('a')['href']
        # All_Questions_link = Amazon_URL_ + All_Questions_link
        All_Questions_link = 'https://www.amazon.com/ask/questions/asin/' + ASIN_ + '/'

        print('- got All_Questions_link Successfully , from Main Page of the product using Soup')

        # ===========================================================================
        # Passing collected Data about teh Product to Amazon_Product Object
        # ===========================================================================
        Amazon_Product_.Product_ASIN = ASIN_

        Amazon_Product_.Product_Title = Product_Title
        # Main Product URL
        Amazon_Product_.Product_URL = ASIN_baseURL_ + ASIN_
        # All Reviews URL
        Amazon_Product_.Product_All_Reviews_URL = All_reviews_link  # driver.current_url
        # All Product Questions
        Amazon_Product_.Product_Questions_URL = All_Questions_link

        print('- Product Profile has been updated ...')

        return Amazon_Product_

#===========================================================================
# 5- Loading the Page of All Reviews of the Product !!!
#===========================================================================
def get_All_Product_Reviews(driver_,Amazon_Product_):
    # ===========================================================================
    # Loading the Page of All Reviews of the Product !!!
    # ===========================================================================

    Reviews_List = []

    print('- Getting All Product Reviews ...')

    driver_.get(Amazon_Product_.Product_All_Reviews_URL)

    # scroll to the bottom in order to load all the page contents
    driver_.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    _delay_(3)

    amazon_Review_page_ = driver_.page_source

    # ===========================================================================
    # Read Total Number of reviews , Positive and Critical Reviews , and URLs for both pages
    # & Passing collected Data about teh Product to Amazon_Product Object
    # ===========================================================================

    soup_Reviews = BeautifulSoup(amazon_Review_page_, "html.parser")

    # for Positive and Critical Reviews
    _Reviews_Links = soup_Reviews.findAll('a', {'class': 'a-size-base a-link-normal see-all'})

    Amazon_Product_.Product_No_Of_Postivie_Reviewes = _Reviews_Links[0].contents[0].strip('See all').strip(
        ' positive reviews')
    Amazon_Product_.Product_Positive_Reviews_URL = Amazon_URL_ + _Reviews_Links[0]['href']

    print('- There are ', Amazon_Product_.Product_No_Of_Postivie_Reviewes, 'Positive Reviews ...')

    Amazon_Product_.Product_No_Of_Critical_Reviewes = _Reviews_Links[1].contents[0].strip('See all').strip(
        ' critical reviews')
    Amazon_Product_.Product_Critical_Reviews_URL = Amazon_URL_ + _Reviews_Links[1]['href']

    print('- There are ', Amazon_Product_.Product_No_Of_Critical_Reviewes, 'Critical Reviews ...')

    # ===========================================================================
    # Saving Amazon_Product_ in Amazon_Product_Data
    # ===========================================================================
    # adding .__dict__ saves my object from errors when saving in json formats
    Amazon_Product_Data.append({'Amazon Product Information': Amazon_Product_.__dict__})

    # ===========================================================================
    # Loading the Page of All Positive Reviews of the Product !!!
    # ===========================================================================

    driver_.get(Amazon_Product_.Product_Positive_Reviews_URL)

    # ==============================================================================
    # here , you have to make sure that page finished loading then read its source

    # use below trick to make sure that page has been loaded successfully, by searching for the item that you will check later after page is loaded

    # and don't go any way until you make sure your item exist !!

    delay_ = 3  # seconds

    while True:
        try:
            myElem = WebDriverWait(driver_, delay_).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="cm_cr-rvw_summary-viewpoints"]')))

            if myElem:
                print('- Positive Reviews Page is ready!')
                break

        except TimeoutException:

            print('- Reviews Page loading took too much time!.. but am still trying for it !')

    # ==============================================================================
    print('- Getting All Positive Reviews ...')
    # loop here for all positive reviews pages

    NoMoreReviewPages = False

    while True:

        try:
            if NoMoreReviewPages:
                NoMoreReviewPages = False  # Exit from the While loop when NoMoreReviewPages
                break
            # delay(2)
            # get the results of the first page
            webPageSource = driver_.page_source

            # parse and get the urls for the results

            soup = BeautifulSoup(webPageSource, "html.parser")

            Reviews_Data_Set_ = data_ = soup.findAll('div', {'class': 'a-section review aok-relative'})

            for i in range(0, len(Reviews_Data_Set_)):

                Review_tmp = Review_Question.Review_()
                Review_tmp.Review_ASIN_ = ASIN_
                Review_tmp.Review_type = 'Positive'

                try:
                    Review_tmp.Reviewer_Name = Reviews_Data_Set_[i].findAll('div', {'class': 'a-profile-content'})[
                        0].text
                    Review_tmp.Review_Rating = Rating_[:int(
                        Reviews_Data_Set_[i].findAll('a', {'class': 'a-link-normal'})[0].text[0])]
                    Review_tmp.Review_Title = Reviews_Data_Set_[i].findAll('a', {
                        'class': 'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'})[
                        0].text.rstrip().lstrip()

                    tempDate = \
                    Reviews_Data_Set_[i].findAll('span', {'class': 'a-size-base a-color-secondary review-date'})[0].text
                    tempDate_ = list(datefinder.find_dates(tempDate))
                    Review_tmp.Review_Date = tempDate_[0].strftime("%d-%m-%Y")

                    Review_tmp.Review_Text = \
                    Reviews_Data_Set_[i].findAll('span', {'class': 'a-size-base review-text review-text-content'})[
                        0].text.rstrip().lstrip()

                    # adding .__dict__ saves my object from errors when saving in json formats

                    if Review_tmp not in Reviews_List:
                        Reviews_List.append(Review_tmp.__dict__)


                except:
                    pass

            # now you finished results of the first page, please click next and fetch results of the next paga and so on until you reach the number of pages you set

            while True:
                try:
                    time.sleep(1)
                    # delay(2)
                    if WebDriverWait(driver_, timeout).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.a-last > a:nth-child(1)'))):
                        driver_.find_element_by_css_selector('.a-last > a:nth-child(1)').click()
                        break

                    # else:
                    #     NoMoreReviewPages = True
                    #     break # No More Pages for Positive Reviews

                # except NoSuchElementException:
                #     break
                except:
                    # you can put here timer for timeout operation and exit this loop
                    NoMoreReviewPages = True
                    # No More Pages for Positive Reviews
                    print("- ===> Timed out waiting for page to load")
                    break
        except:
            pass

    print('- All Positive Reviews had been collected !')
    # As all reviews for positive and critical will be saved in this object at he end
    # Amazon_Product_.Product_Reviews = Reviews_List
    # ===========================================================================

    # ===========================================================================
    # Loading the Page of All Critical Reviews of the Product !!!
    # ===========================================================================

    driver_.get(Amazon_Product_.Product_Critical_Reviews_URL)

    # ==============================================================================
    # here , you have to make sure that page finished loading then read its source

    # use below trick to make sure that page has been loaded successfully, by searching for the item that you will check later after page is loaded

    # and don't go any way until you make sure your item exist !!

    delay_ = 3  # seconds

    while True:
        try:
            myElem = WebDriverWait(driver_, delay_).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="cm_cr-rvw_summary-viewpoints"]')))

            if myElem:
                print('- Critical Reviews Page is ready!')
                break

        except TimeoutException:

            print('- Reviews Page loading took too much time!.. but am still trying for it !')

    # ==============================================================================
    # loop here for all critical reviews pages
    print('- Getting All Critical Reviews ...')

    NoMoreReviewPages = False

    while True:

        try:
            if NoMoreReviewPages:
                NoMoreReviewPages = False  # Exit from the While loop when NoMoreReviewPages
                break
            # delay(2)
            # get the results of the first page
            webPageSource = driver_.page_source

            # parse and get the urls for the results

            soup = BeautifulSoup(webPageSource, "html.parser")

            Reviews_Data_Set_ = data_ = soup.findAll('div', {'class': 'a-section review aok-relative'})

            for i in range(0, len(Reviews_Data_Set_)):

                Review_tmp = Review_Question.Review_()

                Review_tmp.Review_ASIN_ = ASIN_
                Review_tmp.Review_type = 'Critical'

                try:
                    Review_tmp.Reviewer_Name = Reviews_Data_Set_[i].findAll('div', {'class': 'a-profile-content'})[
                        0].text
                    Review_tmp.Review_Rating = Rating_[:int(
                        Reviews_Data_Set_[i].findAll('a', {'class': 'a-link-normal'})[0].text[0])]
                    Review_tmp.Review_Title = Reviews_Data_Set_[i].findAll('a', {
                        'class': 'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'})[
                        0].text.rstrip().lstrip()

                    tempDate = \
                    Reviews_Data_Set_[i].findAll('span', {'class': 'a-size-base a-color-secondary review-date'})[0].text
                    tempDate_ = list(datefinder.find_dates(tempDate))
                    Review_tmp.Review_Date = tempDate_[0].strftime("%d-%m-%Y")

                    Review_tmp.Review_Text = \
                    Reviews_Data_Set_[i].findAll('span', {'class': 'a-size-base review-text review-text-content'})[
                        0].text.rstrip().lstrip()

                    # adding .__dict__ saves my object from erros when saving in json formats

                    if Review_tmp not in Reviews_List:
                        Reviews_List.append(Review_tmp.__dict__)

                except:
                    pass

            # now you finished results of the first page, please click next and fetch results of the next paga and so on until you reach the number of pages you set

            while True:
                try:
                    time.sleep(1)
                    # delay(2)
                    if WebDriverWait(driver_, timeout).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.a-last > a:nth-child(1)'))):
                        driver_.find_element_by_css_selector('.a-last > a:nth-child(1)').click()
                        break

                    # else:
                    #     NoMoreReviewPages = True
                    #     break # No More Pages for Positive Reviews

                # except NoSuchElementException:
                #     break
                except:
                    # you can put here timer for timeout operation and exit this loop
                    NoMoreReviewPages = True
                    # No More Pages for Positive Reviews
                    print("- ===> Timed out waiting for page to load")
                    break
        except:
            pass

    print('- All Critical Reviews had been collected !')

    return Reviews_List

#===========================================================================
# 6- Loading the Page of All Questions about the Product !!!
#===========================================================================
def get_All_PrdocutQuestions(driver_,Amazon_Product_):
    # ===========================================================================
    # Loading the Page of All Questions about the Product !!!
    # ===========================================================================

    Questions_List = []

    driver_.get(Amazon_Product_.Product_Questions_URL)

    # ==============================================================================
    # here , you have to make sure that page finished loading then read its source

    # use below trick to make sure that page has been loaded successfully, by searching for the item that you will check later after page is loaded

    # and don't go any way until you make sure your item exist !!

    delay_ = 3  # seconds

    while True:
        try:
            myElem = WebDriverWait(driver_, delay_).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.celwidget:nth-child(5)')))

            if myElem:
                print('- Questions Page is ready!')
                break

        except TimeoutException:

            print('- Questions Page loading took too much time!.. but am still trying for it !')

    # ==============================================================================
    # ==============================================================================
    # loop here for all Questions pages
    print('- Getting All Questions ...')

    NoMoreQuestionsPages = False

    while True:

        try:
            if NoMoreQuestionsPages:
                NoMoreQuestionsPages = False  # Exit from the While loop when NoMoreReviewPages
                break
            # delay(2)
            # get the results of the first page
            webPageSource = driver_.page_source

            # parse and get the urls for the results

            soup = BeautifulSoup(webPageSource, "html.parser")

            Questions_Data_Set_ = soup.findAll('div', {'class': 'a-fixed-left-grid a-spacing-base'})

            for i in range(0, len(Questions_Data_Set_)):

                if i % 2 == 0:
                    Question_Answer_tmp = Review_Question.Quesion_()
                    Question_Answer_tmp.Question_ASIN_ = ASIN_

                try:

                    Questions_Data_Set_Sub_ = Questions_Data_Set_[i].findAll('span')

                    if i % 2 == 0:
                        Question_Answer_tmp.Question_ = Questions_Data_Set_Sub_[6].text.rstrip().lstrip()
                        # print( Questions_Data_Set_Sub_[6].text.rstrip().lstrip())

                    else:
                        if len(Questions_Data_Set_Sub_) > 1:
                            Question_Answer_tmp.Answer_ = fixed_longAnswer(
                                Questions_Data_Set_Sub_[1].text.rstrip().lstrip())
                        else:
                            Question_Answer_tmp.Answer_ = 'Would You please Answer this Question.'

                        # print(fixed_longAnswer(Questions_Data_Set_Sub_[1].text.rstrip().lstrip()))
                    if i % 2 != 0 and i > 0:
                        if Question_Answer_tmp not in Questions_List:
                            Questions_List.append(Question_Answer_tmp.__dict__)

                except:
                    pass

            # now you finished results of the first page, please click next and fetch results of the next paga and so on until you reach the number of pages you set

            while True:
                try:
                    time.sleep(1)
                    # delay(2)
                    if WebDriverWait(driver_, timeout).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.a-last > a:nth-child(1)'))):
                        driver_.find_element_by_css_selector('.a-last > a:nth-child(1)').click()
                        break


                except:
                    # you can put here timer for timeout operation and exit this loop
                    NoMoreQuestionsPages = True
                    # No More Pages for Positive Reviews
                    print("- ===> Timed out waiting for page to load")
                    break
        except:
            pass

    print('- All Questions regarding the Product had been collected !')

    return Questions_List



""" _save_Data_to_JSON  : function that takes data list (array) and save it in JSON file """
def _save_Data_to_JSON(JSON_filename_, *DataSet):
    """ save_Data_to_JSON: function that takes data list (array) and save it in JSON file """

    if not os.path.exists(os.path.dirname(JSON_filename_)):
        try:
            os.makedirs(os.path.dirname(JSON_filename_))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(JSON_filename_, "w", encoding='utf-8') as f:
        json.dump(DataSet, f, ensure_ascii=False, indent=4)

    f.close()






# function to trim Amazon Question's answer
def fixed_longAnswer(answerText):

    if ' see more' in answerText or ' see less' in answerText:
        zz = answerText.replace('\n\n', '\n').replace(' see less', '').replace(' see more', ' $$$$').replace('                ',' ')

        qq = slicer(zz, ' $$$$').replace('$$$$', '').rstrip().lstrip()

        return qq

    else: return answerText

# function to cut string starting from a specific index of string
def slicer(my_str,sub):
    index=my_str.find(sub)
    if index !=-1 :
        return my_str[index:]
    else :
        raise Exception('Sub string not found!')


#=======================================================
""" _get_WebPage_Source_Using_Request_Get : this function is used to get the webPage source of a given URL using Request and Get Methods """

def _get_WebPage_Source_Using_Request_Get(url):

    session_requests = requests.session()

    result = session_requests.get(url, headers=headers_)
    # result = session_requests.get(url)

    return result.text


def _get_WebPage_Source_Using_Chrome_WebDriver(url, webPage_filename=None, savePage=False):
    """ get the webpage source and save it in a folder with the datetime attribute """
    # options to start Chrome in headless mode.
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--disable-gpu')

    #If you want chrome and chromedriver to stay open afterward, you can add the detach option when starting chromedriver:

    options.add_experimental_option("detach", True)
    # to hide the broswer
    # options.add_argument('--headless')

    browser = webdriver.Chrome(executable_path = Chrome_Driver_Path, chrome_options=options)

    # browser = webdriver.Chrome() #executable_path=os.path.abspath(“chromedriver"), chrome_options = chrome_options)
    # browser = webdriver.Chrome()
    browser.get(url)

    webPage = browser.page_source

    # browser.quit()

    # option to save the webpage to file

    if savePage:

        if not os.path.exists(os.path.dirname(webPage_filename)):
            try:
                os.makedirs(os.path.dirname(webPage_filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        with open(webPage_filename, "w", encoding='utf-8') as f:
            f.write(webPage)

    return webPage

# ==========================================================================================================
def _delay_(n):
    time.sleep(randint(2, n))

#=======================================================
