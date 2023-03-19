# Games_Recommendation_Algorithm

## How the project works:
![recommandation_diagram](https://user-images.githubusercontent.com/127619531/224561655-c6adcac4-3761-4b98-a2aa-1c485ca23007.png)



## How the project is made
### Introduction:
In this project, I made a game recommendation algorithm which follow these steps:<br>
1. The algorithm get the user's inputs
2. The algorithm access the database we made
3. The algorithm compare each game in the database to the input
4. The algorithm assign a score to each game depending of the number of common points they have
5. The algorithm return the games with the best scores

We can break down the making of the algorithm in 4 parts:<br><br>
1. Getting the data and clean it
2. Store the data somewhere we can access it
3. Make an algorithm to compare games and find equivalents
4. Access the data with the algorithm and provide an output to the user's inputs


### 1. Getting the data and clean it:
Firstly, we need to find an API to collect the data we will use. In this project, I used the rawg API, you can make your own profile and get your own key to access to the API here: https://rawg.io/apidocs. Now we need to get the data and clean it, here is a part of the code I made to get and clean the data:

<br><br><br>
![database_cleaning](https://user-images.githubusercontent.com/127619531/226173580-040ad8f6-ec3e-487d-a193-c00b72f4ecac.png)
<br><br><br>

### 2. Store the data somewhere we can access it:
Secondly, we need to store the data somewhere so we have a good and clean database. For this purpose, I used aws s3 using my own private bucket. This allowed me to use aws lambda and aws cloudwatch to get the data and clean it monthly. But before we make the code, we need to upload a starting csv file in the bucket, the one we used is in the S3_restart folder in the repository. After we have created the bucket and uploaded the csv file, we used this code to store the data in the bucket in the csv file:

<br><br><br>
METTRE UNE PARTIE DU CODE POUR METTRE LES DONNEES DANS LE BUCKET
<br><br><br>

We also need to allow access the bucket we made to the function so we need to use an aws IAM role so we can access the bucket and access the csv file in our code.

Now we can automate the call of the function so the function is called monthly, since the database needs to be up to date (and also because we can't do more than 20000 request to the rawg API since we use the free version). In order to do this, we put the code in a lambda function with the layer AWSDataWrangler-Python39 and use a trigger made with aws cloudwatch like this:

<br><br><br>
MONTRER CMNT FAIRE LE CLOUDWQTCH???????
<br><br><br>



### 3. Make an algorithm to compare games and find equivalents:
Finally, we can make our algorithm. We choosed a simple model which works like this:

<br><br><br>
![Algo_diagram](https://user-images.githubusercontent.com/127619531/226173683-0ee69bb2-3af2-4e27-be87-2896f2871eac.png)
<br><br><br>



### 4. Access the data with the algorithm and provide an output to the user's inputs:
We get the data from the database, get the user's input and then use the algorithm in order to display the results. Which bring us to the final section:


## Results

The programm will ask how many games the user want to input, then ask what are the names of the games the user want to find game alike.
Finally, the programm will display the first 50 games that have the best "matching score" according to the algorithm.
A game recommanded is display this way: [score, 'name of the game']
Here is an example with 1 game named Grand Theft Auto V as input:
<br><br><br>
![Capture_result](https://user-images.githubusercontent.com/127619531/224831232-05647360-d843-4939-a72e-d34dba8639a2.PNG)
<br><br><br>




