# Games_Recommendation_Algorithm

## Introduction:
In this project, I made a game recommendation algorithm which works like this:<br>
1. The algorithm get the user's inputs
2. The algorithm access the database we made
3. The algorithm compare each game in the database to the input
4. The algorithm assign a score to each game depending of the number of common points they have
5. The algorithm return the games with the best scores

<br><br><br>
METTRE UN SCHEMA
<br><br><br><br>

We can break down the making of the algorithm in 4 parts:<br><br>
1. Getting the data and clean it
2. Store the data somewhere we can access it
3. Make an algorithm to compare games and find equivalents
4. Access the data with the algorithm and provide an output to the user's inputs


## 1 Getting the data and clean it:
Firstly, we need to find an API to collect the data we will use. In this project, I used the rawg API, you can make your own profile and get your own key to access to the API here: https://rawg.io/apidocs. Now we need to get the data and clean it, here is the code I made to get and clean the data:

<br><br><br>
METTRE UN SCREEN DU CODE
<br><br><br>

## 2 Store the data somewhere we can access it:
Secondly, we need to store the data somewhere so we have a good and clean database. For this purpose, I used aws s3 using my own private bucket. This allowed me to use aws lambda and aws cloudwatch to get the data and clean it monthly. But before we make the code, we need to upload a starting csv file in the bucket, the one we used is in the S3_restart folder in the repository. After we have created the bucket and uploaded the csv file, we used this code to store the data in the bucket in the csv file:

<br><br><br>
METTRE UN SCREEN DU CODE
<br><br><br>

We also need to allow access the bucket we made to the function so we need to use an aws IAM role so we can access the bucket and access the csv file in our code. We made a role like this:

<br><br><br>
METTRE UN SCREEN DU CODE
<br><br><br>


Now we can automate the call of the function so the function is called monthly, since the database needs to be up to date (and also because we can't do more than 20000 request to the rawg API since we use the free version). In order to do this, we put the code in a lambda function with the layer AWSDataWrangler-Python39 and use a trigger made with aws cloudwatch like this:
<br><br><br>
METTRE UN SCREEN DU CODE
<br><br><br>



## 3 Make an algorithm to compare games and find equivalents:
Finally, we can make our algorithm. We choosed a simple model which works like this:

<br><br><br>
METTRE UN SCHEMA DU FONCTIONNEMENT DU CODE
<br><br><br>

It can be translated like this in python:
<br><br><br>
METTRE UN CODE
<br><br><br>




## 4 Access the data with the algorithm and provide an output to the user's inputs:
We need to get the data from the database, get the user's input and then use the algorithm in order to display the results.
We get the data and the input like this:
<br><br><br>
METTRE UN CODE
Then we display the results like this:
<br><br><br>
METTRE UN CODE





