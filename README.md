# Games_Recommendation_Algorithm

## How the project works:
In this project, I made a game recommandation algorithm using a content-based mode, it means the algorithm doesn't use neural network and use instead a database to find similar results to the input he have. <br><br>
Here is a diagram explaining in a more simple way how the algorithm works: <br><br>
![recommandation_diagram](https://user-images.githubusercontent.com/127619531/226174855-2faee863-542f-4266-a91d-15245510d41f.png)



## How the project is made
### Introduction:

We can break down the making of the algorithm in 4 parts:<br><br>
1. Getting the data and clean it
2. Store the data somewhere we can access it
3. Make an algorithm to compare games and find equivalents
4. Access the data with the algorithm and provide an output to the user's inputs
<br><br>

### 1. Getting the data and clean it:
Firstly, we need to find an API to collect the data we will use. In this project, I used the rawg API, you can make your own profile and get your own key to access to the API here: https://rawg.io/apidocs. Now we need to get the data and clean it, here is a diagram to show what was made by now:

<br><br>
![cleaned_data](https://user-images.githubusercontent.com/127619531/226175705-940ddfc9-46a0-4997-ba75-908a3cb9bbcc.png)
<br><br><br><br>

### 2. Store the data somewhere we can access it:
Secondly, we need to store the data somewhere so we have a clean database the algorithm can use.<br>
For this purpose, I used aws s3 using my own private bucket. 
This allowed me to use aws lambda and aws cloudwatch to get the data and clean it monthly.<br><br>
But before we make the code, we need to upload a starting csv file in the bucket, the one we used is in the S3_restart folder in the repository, so we can store the data into an already existing csv file in the bucket. <br>
Once the bucket and the csv file are made, we need to put the data into the bucket. <br>
In order to update the csv file into the bucket, we need to make a IAM role which will allow the account using it to get and upload data into the bucket.<br><br>
Now we can use the program we made to clean the data and put it in a lambda function, you will need to put a layer to the lambda function otherwise every import you use won't work, personally, I used the AWSDataWrangler-Python39 because it was the one that worked with my program.
<br><br>
Here is an updated version of the previous diagram to see what has changed:

<br><br>
![database_cleaning](https://user-images.githubusercontent.com/127619531/226175713-eaf2d5e2-781f-47ac-be73-cd55b809e937.png)
<br><br><br>

Now we can automate the call of the function so the function is called monthly, since the database needs to be up to date (and also because we can't do more than 20000 request to the rawg API since we use the free version). In order solve this probelm, we add a trigger made with aws cloudwatch to the lambda function so it calls the function monthly.<br><br>
Here is what the final version of our diagram looks like:

<br><br>
![database_cleaning_cloudwatch](https://user-images.githubusercontent.com/127619531/226174946-aaec8f5d-a368-4be3-8257-fb859b27b9c3.png)
<br><br><br>

### 3. Make an algorithm to compare games and find equivalents:
Finally, we can make our algorithm. We choosed a simple model which use a score system.
The score of a game depends on parameters choosed because we can get it from the API and we think they are parameters to take in count when searching for similar games. <br><br>
The way the system works is quite simple, if the game we are comparing the input to share genres, tags or popularity with the input, it will increase the score of the game so it will have more chance to be in the list of recommended games.<br><br>
Here is a diagram to show what types of question the algorithm is trying to answer with the score system:

<br><br>
![Algo_diagram](https://user-images.githubusercontent.com/127619531/226177673-614f83a3-2fe0-4788-83ba-c96fb477628b.png)
<br><br><br><br>



### 4. Access the data with the algorithm and provide an output to the user's inputs:
At last, we can get the data from the database, get the user's input and then use the algorithm in order to display the results.<br>
Here is a quick diagram to sum up how it is done:

<br><br>
![result](https://user-images.githubusercontent.com/127619531/226176732-2c70d68f-1fd9-467a-b757-ba267b7ef228.png)
<br><br><br><br>

## How to use

The programm will ask how many games the user want to input, then ask what are the names of the games the user want to find game alike.
The user need to spell exactly the name of the game (if the game is in the database) with the uppercase and spaces right, else the algorithm won't find the game the user is trying to input.
As a result, the programm will display the first 50 games that have the best "matching score" according to the algorithm.
A game recommanded is display this way: [score, 'name of the game']
Here is an example with 1 game named Grand Theft Auto V as input:
<br><br><br>
![Capture_result](https://user-images.githubusercontent.com/127619531/224831232-05647360-d843-4939-a72e-d34dba8639a2.PNG)
<br><br><br>




