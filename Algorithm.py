import operator
import pandas as pd
import boto3
import sys

def format_str(old_str):
    '''Clean the string and return an array, we use this function in format_df'''
    new_string = old_str[2:(len(old_str)-2)] # First, we remove the edges of the strings
    return (new_string.split("', '"))   # Then we clean the in between and convert it into a list


def format_df(df, df_len):
    '''The dataframe has string which looks like array so we need to convert them into arrays before using the dataframe'''

    for i in range(df_len): # for each game 
        
        old_string = df["genres"][i] # The string looks like this: "['Action', 'Adventure']"
        genres = format_str(old_string)

        old_string = df["tags"][i]
        tags = format_str(old_string)

        old_string = df["platforms"][i]
        platforms = format_str(old_string)

        old_string = df["stores"][i]
        stores = format_str(old_string)

        df["genres"][i] = genres
        df["tags"][i] = tags
        df["platforms"][i] = platforms
        df["stores"][i] = stores

    return df


def algorithm(df, df_len, user_input):
    '''The algorithm used if there is only one input, we use the same system when there is multiple inputs
        The algorithm use a score value and compare every game  with this value
        We return the a dictionary of every games in the dataframe, the key is the slug and the value is the score of the game'''

    score = {}

    for i in range(df_len):
        # the df works like this: the current game = df["key to the value of the game (name,genres,...)"][index of the game (i)]
        current_score = 0

        for genre in (user_input["genres"]): # We verify if the genres are the same
            for j in range(len(df["genres"][i])):
                current_genre = df["genres"][i][j]
                if genre == current_genre:
                    current_score += 20             # And then we increase the score if it's true Il faut changer la valeur pour ajuster l'algorithm


        for tag in (user_input["tags"]): # We verify if the tags are the same
            for j in range(len(df["tags"][i])):
                current_tag = df["tags"][i][j]
                if tag == current_tag:
                    current_score += 6             # And then we increase the score if it's true Il faut changer la valeur pour ajuster l'algorithm


        rate = abs(user_input["rating"] - df["rating"][i])    # We store the gap between both rate


        if(rate == 0):  # Then we increase the score the more the gap is low        
            current_score += 100       # Il faut changer la valeur pour ajuster l'algorithm
        elif(rate <= 1):
            current_score += 75       # Il faut changer la valeur pour ajuster l'algorithm
        elif(rate <= 2):
            current_score += 50       # Il faut changer la valeur pour ajuster l'algorithm
        elif(rate <= 3):
            current_score += 25       # Il faut changer la valeur pour ajuster l'algorithm


        rate = abs(user_input["ratings_count"] - df["ratings_count"][i])  # We store the gap between both number of rate

        if(rate == user_input["ratings_count"]/5):  # Then we increase the score the more the gap is low        
            current_score += 100       # Il faut changer la valeur pour ajuster l'algorithm
        elif(rate <= user_input["ratings_count"]/4):
            current_score += 75       # Il faut changer la valeur pour ajuster l'algorithm
        elif(rate <= user_input["ratings_count"]/3):
            current_score += 50       # Il faut changer la valeur pour ajuster l'algorithm
        elif(rate <= user_input["ratings_count"]/2):
            current_score += 25       # Il faut changer la valeur pour ajuster l'algorithm

        # The score dicitonary has the slug of the game as key, the score of the game as first value and the name as second value
        score[df["slug"][i]] = [current_score, df["name"][i]]

    return score



def multiple_algorithm(df, df_len, user_inputs):
    '''The algorithm function work with one input, so we use the function multiple time,
        then we add the score of every iteration of the algorithm to know which game we should suggest'''

    scores = {} # a dictionary of score for each user inputs
    res = {}   # the dictionary of the sum
    firstloop = 1

    for i in range(len(user_inputs)):   # get every score for each inputs of the user
        scores[user_inputs[i]["slug"]] = algorithm(df, df_len, user_inputs[i])

    
    keys = list(scores.keys())
    for i in range(len(keys)):  # for every game of the user
        score = scores[keys[i]]    # sum all the scores into one dicitonnary
        slug_list = score.keys()

        for slug in slug_list:
            if(firstloop == 1):
                res[slug] = score[slug]
            elif(firstloop == 0):
                # now we increment only the score since the name doesn't change
                res[slug][0] += score[slug][0]  

        firstloop = 0

    return res

def search(df, df_len, user_input):
    '''Get the user_input and return the index in df of which game it correspond (work for a single input)'''
    
    res = {}

    for i in range(df_len):
        if (df["name"][i] == user_input):
            for key in df:
                res[key] = df[key][i]
        
    if(res == {}):
        sys.exit("The input is not in the dataframe")
        

    return res


def multiple_search(df, df_len, user_inputs):
    ''' Use the search function to return the index in df of every user_inputs'''
    
    games = []
    for user_input in user_inputs:
        games.append(search(df, df_len, user_input))

    return games


def display_res(scores):
    '''Sort and display the top 50 of the scores dicitonary in descending order'''

    # Sort the dict by score
    sorted_scores = sorted(scores.items(),key=operator.itemgetter(1),reverse=True)

    # Display the firsts 50 results
    loop = 0
    print("Firsts 50 results:")
    for score in sorted_scores:
        if loop < 50:
            print(score[1])
        loop += 1

# get the database / dataframe from s3
bucket = 'bucket-name' # put the name of your bucket (already created)
session = boto3.Session(
aws_access_key_id='key', # put your key
aws_secret_access_key='secret-key' # put your secret key
)
#Creating S3 Resource From the Session.
s3 = session.resource('s3')
df = s3.Object(bucket, 'file_name.csv') # put your csv file name here
df = pd.read_csv(df.get()['Body'])
df.drop('Unnamed: 0', inplace=True, axis=1)


obj = s3.Object(bucket, 'number_last.txt')
df_len = int(obj.get()['Body'].read()) # get the number of the last updated line of the df

df = format_df(df, df_len)

# get the inputs of the user

user_nbr = int(input("How many games do you wish to put in entry ?"))

user_str = []
for i in range(user_nbr):
    user_str.append(input("Write a game's name:"))

if(user_nbr > 1):
    user_games = multiple_search(df, df_len, user_str)
else:
    user_games = search(df, df_len, user_str[0])

if(user_nbr > 1):
    scores = multiple_algorithm(df, df_len, user_games)
else:
    scores = algorithm(df, df_len, user_games)

display_res(scores)

