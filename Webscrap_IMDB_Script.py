""" Fortgeschrittene Softwaretechnik """
""" Teodor Chiaburu, 900526 """


# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# get the address of the IMDB page with most popular 100 films
top_url = "https://www.imdb.com/chart/moviemeter?sort=rk,asc&mode=simple&page=1"

# get html code of the page
r = requests.get(top_url,
    headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
cont = r.content
#print(cont) # raw html

# create soup object to parse the html
soup = BeautifulSoup(cont, "html.parser")
#print(soup.prettify()) # structured html

# store the rows for the csv in a list
list_csv = []

# get table with top films
table_pop = soup.find("tbody", {"class": "lister-list"})
#print(table_pop)

# iterate through all the rows in the table
for row_pop in table_pop.find_all("tr"):
    
    # every row info will be stored in a dictionary
    dict_row = {}
    
    # get section with title, year and increase/drop in popularity
    title_col = row_pop.find("td", {"class": "titleColumn"})
    #print(title_col.text.replace("\n", " "))
    
    # get title 
    dict_row["Title"] = title_col.find("a").text
    #print(title)
    
    # get span containing release year and popularity increase/drop
    year_and_pop = title_col.find_all("span")
    dict_row["Year"] = year_and_pop[0].text.replace("(", "").replace(")", "")
    
    # if there is no popularity span, then the popularity stayed the same
    try:
        pop = int(year_and_pop[1].text.replace("(", "").replace(")", "").replace("\n", " ").replace(",", ""))
        
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
        
    list_csv.append(dict_row)
    
#print(list_csv)

# turn the list into a data frame to save it as csv
df = pd.DataFrame(list_csv)
# give a name to the id column and start at 1
df.index.name = "Rank"
df.index += 1
df.to_csv("imdb_top100.csv")
print(df)