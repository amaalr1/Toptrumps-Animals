import random
import requests

def random_dog():

    #Fetches random dog breed info from DogAPI

    dog_id =random.randint(1, 264) # randomly selects ID of dog breed
    url = f'https://api.thedogapi.com/v1/breeds/{dog_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        animal = response.json()

        # Check if the necessary data fields are present
        if 'height' in animal and 'weight' in animal and 'life_span' in animal:
            height_metric = animal['height']['metric']
            weight_metric = animal['weight']['metric']
            lifespan = animal['life_span']

            # Extract min and max values from the string and convert to integers

            if len(height_metric.split()) >= 3 and len(weight_metric.split()) >= 3 and len(lifespan.split()) >= 3:
                min_height = int(height_metric.split()[0])
                max_height = int(height_metric.split()[2])
                min_weight = int(weight_metric.split()[0])
                max_weight = int(weight_metric.split()[2])
                min_lifespan = int(lifespan.split()[0])
                max_lifespan = int(lifespan.split()[2])

                #calculated average values

                avg_height = (min_height + max_height) / 2
                avg_weight = (min_weight + max_weight) / 2
                avg_lifespan = (min_lifespan + max_lifespan) / 2

                # returns a dictionary with the dog's name and average stats

                return {
                    'name': animal['name'],
                    'life_span': avg_lifespan,
                    'average_height': avg_height,
                    'average_weight': avg_weight,
                }
            # handles any errors occuring with the data
            else:
                print("Incomplete data in response. Skipping...")
                return None
        else:
            print("Incomplete data in response. Skipping...")
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching animal data:", e)
        return None


def run(your_score, opponent_score, rounds):
    # function runs through the rounds of the game preset by user
    while rounds>0:
        my_breed = random_dog() #Fetch random breed for the player
        opponent_breed = random_dog()  # Fetch random breed for the opponent

        if my_breed and opponent_breed:
            print(f'You were given the {my_breed["name"]}')
            print(
                f'Lifespan = {my_breed["life_span"]}, height = {my_breed["average_height"]} cm, weight = {my_breed["average_weight"]} kg')
            # Prompt user for a state choice

            stat_choice = input("Which stat would you like to use (lifespan, height, or weight)? ").lower()

            #validate the user input with state choice
            while stat_choice not in ['lifespan', 'height', 'weight']:
                stat_choice = input("Invalid choice,Try again! Which stat would you like to use (lifespan, height, or weight)? ").lower()

            #prepare the stats for comparison
            stat_choices = {
                'lifespan': (my_breed['life_span'], opponent_breed['life_span']),
                'height': (my_breed['average_height'], opponent_breed['average_height']),
                'weight': (my_breed['average_weight'], opponent_breed['average_weight']),
            }

            #Retrieve the chosen stats

            my_stat = stat_choices[stat_choice][0]
            opponent_stat = stat_choices[stat_choice][1]

            #output the player and opponent choice

            print(f'Your opponent has the {opponent_breed["name"]}')
            print(f'Your {stat_choice} is {my_stat}, your opponents {stat_choice} is {opponent_stat}')

            #Compare the stats and update the scores

            if my_stat > opponent_stat:
                print('You win')
                your_score += 1
            elif my_stat < opponent_stat:
                print('Opponent wins')
                opponent_score += 1
            else:
                print('Draw!')
            print("Your score is now: ", your_score)
            print("Opponent score is now: ", opponent_score)
            rounds -= 1
            print(f'round:{rounds}')

        else:
            # handling error where the dog date couldn't be fetched
            print("Failed to fetch animal data. Skipping this round.")

        if rounds <=0:
            break



    return your_score, opponent_score


def update_score(your_score, opponent_score,rounds):
    # Function Checks the current score to no. of rounds
    if your_score >= rounds:
        print("You won the game!")
    elif opponent_score >= rounds:
        print("Opponent won the game!")

def rounds_count():
    while True:
        try:
            # Allows the user to pick how many rounds to play
            rounds = int(input("how many rounds would you like you play?:"))
            if rounds <=0:
                print(" please enter a number higher than 0")
            else:
                return rounds
        except ValueError:
            print("Invalid input. please enter a number!")



# initialise scores
your_score = 0
opponent_score = 0

rounds = rounds_count()

# Main game loop
while your_score < rounds and opponent_score < rounds:
    your_score, opponent_score = run(your_score, opponent_score, rounds)
    update_score(your_score, opponent_score, rounds)

input("Press Enter to exit...")