# Webscraper_IMDB

The program scrapes data about the current top 100 most popular movies on IMDB. We are particularly interested in year of appearance, IMDB score, increase/decrease in popularity and number of votes; this information is stored in a csv file (see [imdb_top100.csv](imdb_top100.csv) as an example).

## Tasks
- [x] **UML diagrams**
  - [class diagram](proofs/uml_klassendiagramm.PNG): shows the structure of the [two main classes](src/main/resources/Webscrap_IMDB_Library.py) used for this program: *Webscraper* and *TestWebscraper*
  - [object diagram](proofs/uml_objektdiagramm.PNG): shows the values of the attributes of the object *webscraper* after being instantiated
  - [use case diagram](proofs/uml_anwendungsfalldiagramm.png): shows how the script runs and what the expected result is
  
- [x] **Metrics** (via *SonarQube*, see [node definition](sonarqube-analysis))
  - [reliability](proofs/sonarqube_reliability.png)
  - [security](proofs/sonarqube_security.png)
  - [maintainability](proofs/sonarqube_maintainability.png)  
  - [duplications](proofs/sonarqube_duplications.png)
  - [coverage](proofs/sonarqube_coverage.png): *SonarQube* sets a high par when it comes to test coverage (min. 80%). Given that *TestWebscraper* is fairly small and only checks three test cases, my code only reached little over 9% coverage. [Here](src/test/resources/coverage.xml) is a link to the xml file of the generated coverage analysis. 
  - [others](proofs/sonarqube_others.png): such as lines of code, percent of comment lines, cyclomatic and cognitive complexity, number of (open) issues
  
  An overview of the metrics can be seen [here](proofs/sonarqube_overview_1.png) and [here](proofs/sonarqube_overview_2.png).
  
- [x] **Clean Code Development**

  Refer to the code for the [library](src/main/resources/Webscrap_IMDB_Library.py) and the [main script](src/test/resources/Webscrap_IMDB_Test.py):
  - there is no useless/commented out code
  - sufficient documentation at the library level, where user should get an insight into what each class does
  - readability: code can be read as plain English (e.g. lines 155 or 179 in library)
  - precise naming of variables (e.g. *top_url, list_csv, soup, row_pop, dict_row, title_col*) and functions/methods (e.g. *replace_brackets, get_table, iterate_films, add_films, test_shape, test_isnan*)
  - tests for states of variables: see class *TestWebscraper*
  - fields define state: temporary variables are only declared within local scope (e.g. *dict_row* on line 67)
  - correct exception handling: in method *add_films* of class *Webscraper* and testing methods of class *TestWebscraper*
  - avoid negative conditionals (e.g. line 95 in library)
  - DRY: there are no pieces of code that repeat themselves (no duplications in *SonarQube*)
  - KISS: simple function definitions (e.g. line 16 in library)
  - 'divide and conquer': no long method chaining (e.g. lines 76-79, 110-112)
  - assertions: in all the testing methods of *TestWebscraper*
  - split long methods: see methods *add_films* and *iterate_films* in class *Webscraper* (also definition of *replace_brackets* outside the class)
  - design and implementation do not overlap: there are two separate files for the classes and their instantiation
  - consistency: use of term 'webscraper' in the name of the class *TestWebscraper* to match the tested class *Webscraper*; also both methods that are applied on film data have the term 'film' in them: *add_films* and *iterate_films*
  
- [x] **Build Management**

  I used *Maven* (see successful built in *Jenkins* [here](proofs/jenkins_build_maven.png) and even more evidence in [pom.xml](pom.xml)).
  
- [x] **Unit Tests**

  Integrated in *Maven*, take a look at the [test script](src/test/resources/Webscrap_IMDB_Test.py).
  
- [x] **Continuous Delivery**

  See [Jenkinsfile](Jenkinsfile) and [Jenkins Pipeline](proofs/jenkins_build_pipeline.png). The building process was successful ([proof1](proofs/jenkins_build_sun.png)) and also the integration of *SonarQube* ([proof2](proofs/jenkins_build_sonarqube.png)).
