Amazon-Products
=============================

take Amazon Product ASIN and retrieve , Product Profile , Reviews and Questions
Introduction:

this project takes Amazon Product ASIN ( something like Product reference for Amazon),

and get all details about the product Reviews and Questions about it from the customers

Amazon_Asin_V1.0.py:
=============================

I could read all the product reviews ( Positive and Critical ) ones, using selenium

I created Review Items

I created Product Items

=============================

Amazon_Asin_V1.2.py
=============================

I will use direct links extracted rather than extracting them using selenim actions, for Positive and Critical Reviews

=============================

Amazon_Asin_V1.4.py
=============================

I fixed the json format output by adding .dict for each object before appending to the Data_ variable that will be used later to output the json file.

=============================

Amazon_Asin_V1.5.py
=============================

I could from main page extract all links for Reviews pag , and Question page ( actually it is a fixed URL for questions)

then use these links to go for each page and fetch the data for each scope

rather than doing automation form main page to get the links then click on them, I think this faster !!

I work now on fetching questions !!.............. Done

=============================

Amazon_Asin_V1.6.py
=============================

I will enhance the code and remove un-necessary lines
in in Amazon_Asin_V1.7.py

=============================


Amazon_Asin_V1.7.py
=============================
created class for Amzon Function to be called from Amazon_Asin_V1.7.py

=============================


Amazon_Asin_V1.8.py
=============================

created class for Amzon FunctionV3 to be called from Amazon_Asin_V1.8.py

updated finding elements as per Amazon updates

=============================


Amazon_Asin_V1.9.py
=============================

created class for Amzon FunctionV4 to be called from Amazon_Asin_V1.9.py

Added Product Price in Amazon Product Class "Amazon_Product.py"

Added command line to get ASIN number as an input form the command line

Added ASIN availability checker

=============================


Amazon_Asin_V2.0.py
=============================

created class for Amzon FunctionV5 to be called from Amazon_Asin_V2.0.py

will work on specifying number of customers' reviews (option)

will work on specifying number of customers' questions (option)

=============================
