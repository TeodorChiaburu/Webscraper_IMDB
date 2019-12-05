node {
    stage('SCM Checkout') {
        git 'https://github.com/TeodorChiaburu/Webscraper_IMDB'
    }
    stage('Compile-Package') {
        // get maven home path
        def mvnHome = tool name: 'maven-3', type: 'maven'
        bat "${mvnHome}/bin/mvn package"  
    }
}
