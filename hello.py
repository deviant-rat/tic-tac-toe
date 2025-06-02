import random
import time
import json

def open_archive():
    try:
        with open('archive.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        data = []
        return data


def add_record(name, time, score):
    new_record = { 
        "name": name,
        "time": time,
        "score": score
    }
    archive = open_archive()
    archive.append(new_record)
    with open('archive.json', 'w') as file:
        json.dump(archive, file, indent=4)

def archive_print():
    print(open_archive())


def read_high_score():
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read().strip())
            return high_score
    except FileNotFoundError:
        return None #nothing to return
    except ValueError:
        return None #non numeric value check
    
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def game():
    print("Hello")
    player_name = input("What's your name\n")
    random_int = random.randint(1,15)
    count = 0
    high_score = read_high_score()
    time_start = time.time()
    while True:
        try:
            user_guess = int(input('Plese enter a number between 1 and 15: '))
        except ValueError:
            print("That's not a valid number! Please type a number ")
            continue  # Skip the rest of the loop and ask for input again
        if user_guess < 1 or user_guess > 15:
            print("Your number is not in the range!")
            continue
        count+=1
        if user_guess>random_int:
            print("Aim lower")
        elif user_guess<random_int:
            print("Aim higher")
        else:
            final_time = round(time.time() - time_start, 2)
            print("You won!!!")
            print("Number of guesses: "+str(count))
            print(f"Time played: {final_time}")
            add_record(player_name, str(final_time), str(count))
            if high_score is None or count < high_score:
                print ("New High Score!!!")
                save_high_score(count)
            break
#print(randon_int)

game()

