#!/home/oceanw/anaconda3/bin/python


highest = 10
answer = 2
guess = input ("Guess a number from 0 to %d: " %highest)
while (int(guess) != answer):
	if(int(guess) < answer):
		print("Answer is higher")
		guess = input ("Guess a number from 0 to %d: " %highest)
	else:
		print("Answer is lower")
		guess = input ("Guess a number from 0 to %d: " %highest)
		
print("Correct!")
