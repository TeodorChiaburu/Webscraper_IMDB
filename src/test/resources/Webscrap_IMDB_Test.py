from Webscrap_IMDB_Script import Webscraper, TestWebscraper

if __name__ == '__main__':
    
    top_url = "https://www.imdb.com/chart/moviemeter?sort=rk,asc&mode=simple&page=1"
    webscraper = Webscraper(top_url)
    webscraper.iterate_films(webscraper.add_films)
    df = webscraper.convert_to_df()
    
    tester = TestWebscraper()
    tester.add_dataframe(df)
    tester.test_shape()
    tester.test_isnan()
    tester.test_start_index()