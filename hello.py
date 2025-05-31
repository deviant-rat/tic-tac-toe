import random

print("hello")
random_int = random.randint(1,15)
count = 0
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
        break
#print(randon_int)