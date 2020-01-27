""" Fortgeschrittene Softwaretechnik """
""" Teodor Chiaburu, 900526 """

""" Library containing classes for creating the webscraper and testing it """



# relevant libraries
import requests
import pandas as pd
import unittest
from numpy import isnan
from bs4 import BeautifulSoup

# lambda function to replace the brackets in a string with an empty string
replace_brackets = lambda s : s.replace("(", "").replace(")", "")  

""" 
Class for creating webscraping objects

Attributes: - top_url  = address of website to scrap
            - html     = the html code of the relevant page(s)
            - soup     = object of type BeautifulSoup to scrape the data
            - list_csv = list where the interesting rows of data are to be stored
            
Methods:    - get_table() = get the data from the webpages as a table
            - iterate_films(action) = apply the operation 'action' iteratively on each row of data
            - add_films(dict_row, row_pop) = adds the relevant features of the films to the list attribute;
                                             features from row_pop will fist be stored in the dictionary dict_row
            - convert_to_df() = converts the attribute list_csv into a data frame 
                                and saves the info as a csv file in the local directory
"""
class Webscraper:
    
    # factory method
    def __init__(self, top_url):
        
        # address of the IMDB page with most popular 100 films
        self.top_url = top_url
        
        # get html code of the page
        self.html = requests.get(top_url,
                                 headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        
        # create BeautifulSoup object to parse the html
        self.soup = BeautifulSoup(self.html.content, "html.parser")
        
        # store the rows for the csv file in a list
        self.list_csv = []
                
    # get table with top films
    def get_table(self):
        
        return self.soup.find("tbody", {"class": "lister-list"})
    
    # iterate through all the rows in the table
    # function 'action' passed as argument
    def iterate_films(self, action):

        # initialize data table
        table = self.get_table()
        
        # each new film is shown on a table row -> tag <tr>
        for row_pop in table.find_all("tr"):
            
            # every row info will be first stored in a dictionary
            dict_row = {}
            
            # apply operation passed as parameter
            action(dict_row, row_pop)
                            
    # add movie data to the csv list       
    def add_films(self, dict_row, row_pop):
        
        # get section with title, year and increase/drop in popularity
        title_col = row_pop.find("td", {"class": "titleColumn"})
        
        # get title 
        dict_row["Title"] = title_col.find("a").text
        
        # get span containing release year and popularity increase/drop
        year_and_pop = title_col.find_all("span")
        dict_row["Year"] = replace_brackets(year_and_pop[0].text) 
        
        # if there is no popularity span, then the popularity was constant (0 increase/decrease)
        try:        
            pop = replace_brackets(year_and_pop[1].text)
            pop = int(pop.replace("\n", " ").replace(",", ""))
            
            # pop is an absolute value -> find out whether it's an increase or decrease
            titlemeter = year_and_pop[1].find("span", {"class": "up"})
            
            # if the titlemeter span doesn't have class 'up', then it has class 'down'
            # this is a sign of drop in popularity
            if titlemeter is None:
                pop = -pop
        except:
            pop = 0
        dict_row["Popularity"] = pop
    
        # get section with IMDB score and number of ratings
        rating_col = row_pop.find("td", {"class": "imdbRating"})
        
        # extract rating and number of users who graded the film
        try:
            dict_row["Rating"] = float(rating_col.text)
            
            # number of voting users is mentioned in the title attribute
            # start index of number is 13 and it ends where the next white space occurs
            title_attribute = rating_col.find("strong")["title"]
            end_index = title_attribute.find(" ", 13)
            dict_row["Votes"] = int(title_attribute[13 : end_index].replace(",", ""))
        except:
            dict_row["Rating"] = 0.0
            dict_row["Votes"]  = 0
            
        # add newly created dictionary to the list
        self.list_csv.append(dict_row)
        
    # converts attribute 'list_csv' to a data frame and saves it locally as a csv
    def convert_to_df(self):
        
        # turn the list into a data frame to save it as csv
        df = pd.DataFrame(self.list_csv)
        
        # give a name to the id column and start at 1
        df.index.name = "Rank"
        df.index += 1
        
        # save csv file
        df.to_csv("imdb_top100.csv")
        
        return df

"""
Testing class for Webscraper
Inherited from unittest.TestCase

Attributes: - df = movie data frame

Methods:    - add_dataframe(df) = adds the data frame to be tested to the object
            - test_shape() = check whther the data frame has the expected number of examples and features
            - test_isnan() = check if the columns 'Popularity', 'Rating' and 'Votes' have NaNs
            - test_start_index() = check if the first index in the data frame was correctly set to 1
"""
class TestWebscraper(unittest.TestCase):
    
    # set attribute df to the inputed data frame
    def add_dataframe(self, df):
        self.df = df

    # check the dimensions of the data
    def test_shape(self):
        try: 
            self.assertEqual(self.df.shape, (100, 5))
            print('Shape test passed!')
        except AssertionError as err:
            print('Shape test failed!')
            print(str(err))

    # check whether there are NaNs in the numeric columns
    def test_isnan(self):
        try:
            # remember the current column name (in case of exception)
            current_col = 'Popularity'
            self.assertFalse(any(isnan(self.df[current_col])))
            current_col = 'Rating'
            self.assertFalse(any(isnan(self.df[current_col])))
            current_col = 'Votes'
            self.assertFalse(any(isnan(self.df[current_col])))
            print('NaN test passed!')
        except AssertionError:
            print('NaN test failed!')
            print(current_col + ' column has NaN values!')

    # check if the starting index was set to 1
    def test_start_index(self):
        try:
            self.assertEqual(self.df.index.start, 1)
            print('Start index test passed!')
        except AssertionError as err:
            print('Start index test failed!')
            print(str(err))

