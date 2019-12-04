node {
    stage('SCM Checkout') {
        git 'https://github.com/TeodorChiaburu/Webscraper_IMDB'
    }
    stage('Compile-Package') {
        sh 'mvn package'   
    }
}
