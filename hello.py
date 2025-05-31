import random

print("hello")
randon_int = random.randint(1,15)
count = 0
while(True):
    user_guess = int(input('Plese enter a number: '))
    count+=1
    if (user_guess>randon_int):
        print("Aim lower")
    elif(user_guess<randon_int):
        print("Aim higher")
    else:
        print("You won!!!")
        print("Number of guesses: "+str(count))
        break
print(randon_int)