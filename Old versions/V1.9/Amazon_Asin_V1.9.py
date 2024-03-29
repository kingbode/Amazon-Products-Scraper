from AmazonFunctionsV4 import load_Procut_Page, remove_Nagging_Window, get_Product_Profile, \
    get_All_Product_Reviews, get_All_PrdocutQuestions, _save_Data_to_JSON , _check_ASIN_Existance, initialize_WebDriver

from Amazon_Product import Amazon_Product

from selenium import webdriver
import time

from webdriver_manager.chrome import ChromeDriverManager



# ASIN Search Website
# https://amazon-asin.com/asincheck/?product_id=BO7GKK5FQT

#===================================================================
# Declaring variables
#===================================================================

timeout = 5

# ASIN_ = 'B07W8YTDDR' #'B07MW4BR8D'  #'B082B597Y6' #'B07KNHQ8NZ' # this is a sample ASIN

ASIN_ = input('Please Input Amazon Product ASIN : ')

Amazon_URL_ = 'https://www.amazon.com'

ASIN_baseURL_ = 'https://www.amazon.com/dp/'


full_URL = ASIN_baseURL_ + ASIN_

_ASIN_Validity = False

Rating_ = '★★★★★'

totalNumberOfReviews = 0

Positive_Reviews_Count = 0

Critical_Reviews_Count = 0

Amazon_Product_Data = []

Reviews_List = []

Questions_List = []

Questions_List = []

Amazon_Product_ = Amazon_Product()

# Chrome_Driver_Path = r'.\chromedriver.exe'

headers_ = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}


#==========================================================================================================
# Process time measuring
start_time = time.time()
#==========================================================================================================
#==========================================================================================================
#=============================================== Main Application =========================================
#==========================================================================================================

# 0- Checking ASIN Validity:

_ASIN_Validity = _check_ASIN_Existance(full_URL)



# 1- Initialize Web Driver:

if _ASIN_Validity:
    print('- Valid Product ASIN is being processed')

    driver_ = initialize_WebDriver()

# driver.get(URL_)
# driver_ = initialize_WebDriver(Chrome_Driver_Path)

#==========================================================================================================
# 2- Visiting main Link of a given ASIN
#==========================================================================================================

    load_Procut_Page(full_URL,driver_)


#==========================================================================================================
# 3- bypassing nagging popup window for local country
#==========================================================================================================

    remove_Nagging_Window(driver_)

#===========================================================================
# Now use the Main Product Page to get all teh Fields of Amazon_Product Object
# meaning all URLs required to visit , to save time going back and forth, or trying to find them using Selenium
#===========================================================================
# 4- Get Amazon Product Profile
#===========================================================================

    Amazon_Product_ = get_Product_Profile(driver_,ASIN_)


    Amazon_Product_Data.append({'Amazon Product Profile':Amazon_Product_.__dict__})
#===========================================================================
#Starting Scrapping
#===========================================================================

#===========================================================================
# 5- Loading the Page of All Reviews of the Product !!!
#===========================================================================

    Reviews_List = get_All_Product_Reviews(driver_,Amazon_Product_)

#===========================================================================
# Saving All Reviews details about the Product in Amazon_Product_Data !!!
#===========================================================================

    Amazon_Product_Data.append({'Amazon Product Reviews':Reviews_List})
#===========================================================================

#===========================================================================
# 6- Loading the Page of All Questions about the Product !!!
#===========================================================================

    Questions_List = get_All_PrdocutQuestions(driver_,Amazon_Product_)

#==============================================================================

#===========================================================================
# Saving All Questions details about the Product in Amazon_Product_Data !!!
#===========================================================================

    Amazon_Product_Data.append({'Amazon Product Questions':Questions_List})

#===========================================================================

#===========================================================================
# output the data as json file
#===========================================================================
    _save_Data_to_JSON('.\ASINs\\' + ASIN_+ '.json', Amazon_Product_Data)

#===========================================================================
# here we get how much time is taken to execute this process

    driver_.close()

    print("--- %s seconds ---" % (time.time() - start_time))


else:
    print('- Product ASIN seems to be invalid or no longer exists in Amazon database')

    print('hi')

