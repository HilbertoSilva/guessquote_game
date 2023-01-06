
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictReader

BASE_URL = "http://quotes.toscrape.com"

def read_quotes(filename):
	with open(filename,"r") as file:
		csv_reader = DictReader(file)
		return list(csv_reader)

read_quotes("quotes.csv")		

def start_game(quotes):
	quote = choice(quotes)
	remaining_guesses = 4
	print("Here's a quote: ")
	print(quote["text"])
	#print(quote["author"])
	guess = ''
	while guess.lower() != quote["author"].lower() and remaining_guesses >0:
		guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses} \n")
		if guess.lower() == quote["author"].lower():
			print("You got it right. Congratulations!")
			break
		remaining_guesses -= 1
		if remaining_guesses == 3:
			res = requests.get(f"{BASE_URL}{quote['bio-link']}")
			soup = BeautifulSoup(res.text,"html.parser")
			birth_date = soup.find(class_="author-born-date").get_text()
			birth_place = soup.find(class_="author-born-location").get_text()
			print (f"Here's a hint: the author was born on {birth_date} {birth_place}.")
		elif remaining_guesses == 2:
			last_initial = quote["author"].split(" ")[-1][0]
			print (f"Here is another hint : The author first name starts with {quote['author'][0]} and the last name starts with {last_initial}.")	
		elif remaining_guesses == 1:
			res = requests.get(f"{BASE_URL}{quote['bio-link']}")
			soup = BeautifulSoup(res.text,"html.parser")
			description = soup.find(class_="author-description").get_text()
			d2 = description.replace(quote['author'],'*******')
			d3 = d2.replace(quote["author"].split(" ")[-1],'******')
			d4 = d3.split('.')[0]
			print (d4)
		
		else:
			print (f"Sorry, you ran out of guesses... The answer was {quote['author']}")

	again =""
	while again.lower() not in ('y','n','yes','no'):
		again = input("Would you like to play again? (y/n)")
	if again.lower() in ('yes','y'):
		print ("Ok. Let's play again!")
		return start_game()
	else:
		print ("Ok. Goodbye.")		

quotes = read_quotes("quotes.csv")
start_game(quotes)