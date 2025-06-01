import random

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
    random_int = random.randint(1,15)
    count = 0
    high_score = read_high_score()
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
            print("You won!!!")
            print("Number of guesses: "+str(count))
            if high_score is None or count < high_score:
                print ("New High Score!!!")
                save_high_score(count)
            break
#print(randon_int)

game()

