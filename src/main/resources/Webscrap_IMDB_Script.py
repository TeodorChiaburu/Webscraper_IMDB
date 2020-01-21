""" Fortgeschrittene Softwaretechnik """
""" Teodor Chiaburu, 900526 """


# import libraries
import requests
import pandas as pd
import unittest
from numpy import isnan
from bs4 import BeautifulSoup


# lambda function to replace the brackets in a string with an empty string
replace_brackets = lambda s : s.replace("(", "").replace(")", "")  

class Webscraper:
    
    def __init__(self, top_url):
        
        # address of the IMDB page with most popular 100 films
        self.top_url = top_url
        # get html code of the page
        self.html = requests.get(top_url,
                                 headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        # create soup object to parse the html
        self.soup = BeautifulSoup(self.html.content, "html.parser")
        # store the rows for the csv in a list
        self.list_csv = []
                
    # get table with top films
    def get_table(self):
        
        return self.soup.find("tbody", {"class": "lister-list"})
    
    # iterate through all the rows in the table
    # function 'action' passed as argument
    def iterate_films(self, action):

        table = self.get_table()
        
        for row_pop in table.find_all("tr"):
            
            # every row info will be stored in a dictionary
            dict_row = {}
            
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
        
        # if there is no popularity span, then the popularity stayed the same
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
            
        self.list_csv.append(dict_row)
        
    # converts attribute 'list_csv' to a data frame and saves it locally as a csv
    def convert_to_df(self):
        
        # turn the list into a data frame to save it as csv
        df = pd.DataFrame(self.list_csv)
        # give a name to the id column and start at 1
        df.index.name = "Rank"
        df.index += 1
        df.to_csv("imdb_top100.csv")
        
        return df

        
class TestWebscraper(unittest.TestCase):

    def test_shape(self):
        self.assertEqual(df.shape, (100, 5))

    def test_isnan(self):
        self.assertFalse(any(isnan(df['Popularity'])))
        self.assertFalse(any(isnan(df['Rating'])))
        self.assertFalse(any(isnan(df['Votes'])))

    def test_start_index(self):
        self.assertEqual(df.index.start, 1)


if __name__ == '__main__':
    
    top_url = "https://www.imdb.com/chart/moviemeter?sort=rk,asc&mode=simple&page=1"
    webscraper = Webscraper(top_url)
    webscraper.iterate_films(webscraper.add_films)
    
    df = webscraper.convert_to_df()
    
    unittest.main()

