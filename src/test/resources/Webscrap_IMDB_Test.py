""" Fortgeschrittene Softwaretechnik """
""" Teodor Chiaburu, 900526 """

""" Script for testing the class Webscraper """


# classes from the webscraping library
from Webscrap_IMDB_Library import Webscraper, TestWebscraper


if __name__ == '__main__':
    
    # define address of the site to be scraped
    top_url = "https://www.imdb.com/chart/moviemeter?sort=rk,asc&mode=simple&page=1"
    
    # instantiate webscraper
    webscraper = Webscraper(top_url)
    
    # collect data
    webscraper.iterate_films(webscraper.add_films)
    
    # save results as csv file
    df = webscraper.convert_to_df()
    
    
    ### TESTS ###
    
    # instantiate tester and add previously obtained data frame
    tester = TestWebscraper()
    tester.add_dataframe(df)
    
    # test dimensions (should be 100 rows by 5 columns)
    tester.test_shape()
    
    # test for NaN values
    tester.test_isnan()
    
    # check the starting index
    tester.test_start_index()