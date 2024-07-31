import random
import requests

def random_dog():
    dog_id =random.randint(1, 264)
    url = f'https://api.thedogapi.com/v1/breeds/{dog_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        animal = response.json()

        if 'height' in animal and 'weight' in animal and 'life_span' in animal:
            height_metric = animal['height']['metric']
            weight_metric = animal['weight']['metric']
            lifespan = animal['life_span']

            if len(height_metric.split()) >= 3 and len(weight_metric.split()) >= 3 and len(lifespan.split()) >= 3:
                min_height = int(height_metric.split()[0])
                max_height = int(height_metric.split()[2])
                min_weight = int(weight_metric.split()[0])
                max_weight = int(weight_metric.split()[2])
                min_lifespan = int(lifespan.split()[0])
                max_lifespan = int(lifespan.split()[2])

                avg_height = (min_height + max_height) / 2
                avg_weight = (min_weight + max_weight) / 2
                avg_lifespan = (min_lifespan + max_lifespan) / 2

                return {
                    'name': animal['name'],
                    'life_span': avg_lifespan,
                    'average_height': avg_height,
                    'average_weight': avg_weight,
                }
            else:
                print("Incomplete data in response. Skipping...")
                return None
        else:
            print("Incomplete data in response. Skipping...")
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching animal data:", e)
        return None



def run(your_score, opponent_score):
    my_breed = random_dog()
    opponent_breed = random_dog()  # Move opponent animal fetching here

    if my_breed and opponent_breed:
        print(f'You were given the {my_breed["name"]}')
        print(
            f'Lifespan = {my_breed["life_span"]}, height = {my_breed["average_height"]} cm, weight = {my_breed["average_weight"]} kg')

        stat_choice = input("Which stat would you like to use (lifespan, height, or weight)? ").lower()

        while stat_choice not in ['lifespan', 'height', 'weight']:
            stat_choice = input("Invalid choice,Try again! Which stat would you like to use (lifespan, height, or weight)? ").lower()

        stat_choices = {
            'lifespan': (my_breed['life_span'], opponent_breed['life_span']),
            'height': (my_breed['average_height'], opponent_breed['average_height']),
            'weight': (my_breed['average_weight'], opponent_breed['average_weight']),
        }

        my_stat = stat_choices[stat_choice][0]
        opponent_stat = stat_choices[stat_choice][1]

        print(f'Your opponent has the {opponent_breed["name"]}')
        print(f'Your {stat_choice} is {my_stat}, your opponents {stat_choice} is {opponent_stat}')

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
    else:
        print("Failed to fetch animal data. Skipping this round.")

    return your_score, opponent_score


def update_score(your_score, opponent_score):
    if your_score >= 10:
        print("You won the game!")
    elif opponent_score >= 10:
        print("Opponent won the game!")


your_score = 0
opponent_score = 0

while your_score < 10 and opponent_score < 10:
    your_score, opponent_score = run(your_score, opponent_score)
    update_score(your_score, opponent_score)

input("Press Enter to exit...")