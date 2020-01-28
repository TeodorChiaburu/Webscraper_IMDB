# Webscraper_IMDB

The program scrapes data about the current top 100 most popular movies on IMDB. We are particularly interested in year of appearance, IMDB score, increase/decrease in popularity and number of votes; this information is stored in a csv file (see [imdb_top100.csv](imdb_top100.csv) as an example).

## Tasks
- [x] **UML diagrams**
  - [class diagram](proofs/uml_klassendiagramm.PNG): shows the structure of the [two main classes](src/main/resources/Webscrap_IMDB_Library) used for this program: *Webscraper* and *TestWebscraper*
  - [object diagram](proofs/uml_objektdiagramm.PNG): shows the values of the attributes of the object *webscraper* after being instantiated
  - [use case diagram](proofs/uml_anwendungsfalldiagramm.png): shows how the script runs and what the expected result is
  
- [x] **Metrics** (via *SonarQube*)
  - [reliability](proofs/sonarqube_reliability.png)
  - [security](proofs/sonarqube_security.png)
  - [maintainability](proofs/sonarqube_maintainability.png)  
  - [duplications](proofs/sonarqube_duplications.png)
  - [coverage](proofs/sonarqube_coverage.png): *SonarQube* sets a high par when it comes to test coverage (min. 80%). Given that *TestWebscraper* is fairly small and only checks three test cases, my code only reached little over 9% coverage. 
  - [others](proofs/sonarqube_others.png): such as lines of code, percent of comment lines, cyclomatic and cognitive complexity, number of (open) issues
  
  An overview of the metrics can be seen [here](proofs/sonaqube_overview1.png) and [here](proofs/sonaqube_overview2.png).
