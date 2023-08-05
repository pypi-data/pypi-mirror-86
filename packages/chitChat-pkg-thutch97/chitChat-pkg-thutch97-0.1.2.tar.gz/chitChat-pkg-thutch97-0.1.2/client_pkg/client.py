import requests

# print("Please input the address for your server.")
# BASE = "http://" + input("http://")
BASE = 'http://127.0.0.1:5000/' # The endpoint of the API

''' Functions '''
def register():
	# Give username
	username = input('Please provide a username. ')
	if username == 'back': return False # To go back to previous layer

	# Give display name
	display_name = input('Please provide a display name. ')
	if display_name == 'back': return False # To go back to previous layer

	# Give password
	while True:
		password1 = input('Please provide a password. ')
		if password1 == 'back':
			return False # To go back to previous layer
		password2 = input('Please repeat the password. ')
		if password2 == 'back':
			return False # To go back to previous layer
		if password1 == password2:
			password = password1
			break
		else:
			print('Sorry, the passwords do not match, please try again.')

	# Giving friends names
	print('If applicable, please provide usernames for friends who already use chitChat.')
	print("Leave empty if you don't have any friends. ;(")
	response = input('Please leave a space between each username. ')
	if response == 'back':
		return False
	names = response.split()

	# Check friends exist in the database
	checked_names = []
	for friend_name in names:
		if requests.get(BASE + "display_name", {"username": friend_name}).json() != {
			'None': 'There is no user by this username.'
		}:
			checked_names.append(friend_name)
		else:
			print(f"The username {friend_name} does not exist.")

	# Create new friends' names string
	friends = " ".join(checked_names)

	# Make the register API call
	args = {
		"username": username,
		"password": password,
		"display_name": display_name,
		"friends": friends
	}
	result = requests.post(BASE + "register", args).json()

	''' If username taken, try again. If not, login '''
	if 'user_added' in result:
		print('')
		return True

	else:
		print('Sorry, this username is taken, please try a different username.')


def login():
	username = input('Please provide a username. ')
	if username == 'back': return ['back', None] # This will allow the login/register screen to reset

	password = input('Please provide a password. ')
	if password == 'back': return ['back', None] # This will allow the login/register screen to reset

	''' Creating arguments for register API call '''
	argKeys = ['username', 'password']
	argValues = [username, password]
	args = dict(zip(argKeys, argValues))

	''' Making the API call '''
	response = requests.get(BASE + "login", args)
	result = response.json()

	''' Respond appropriately '''
	if result == {'success': 'Passwords match.'}:
		return [True, username]

	elif result == {'error': 'Passwords do not match.'}:
		print('Sorry, your password is incorrect, please try again.')

	elif result == {'error': 'This user does not exist.'}:
		print('Sorry, this user does not exist, please try another username.')


def border(message, where='topAndBottom', border='-'):
	
	length = len(message)

	if where == 'top':
		print(length * border)
		print(message)

	elif where == 'bottom':
		print(message)
		print(length * border)

	else:
		print(length * border)
		print(message)
		print(length * border)
	

def home(username):

	''' Find conversations via API call '''
	response = requests.get(BASE + "home", {'username': username})
	result = response.json()

	''' Check if there are any conversations '''
	if 'None' in result:

		toPrint = ["You don't have any conversations, why don't you start a new one?", '']
		return [None, toPrint]

	else: 

		toPrint = ["Here are your ongoing conversations.", '']

		''' Present conversations nicely '''
		chatPoss = [] # This will be useful for chat_name API call

		for convo in result:
			friend = result[convo][0]
			friendUserName = convo
			chatPoss.append([friend, friendUserName])
			message = result[convo][1][:35]
			space_size = 15-len(friend)
			spaces = " " * space_size

			toPrint.append("{}{}{}".format(friend, spaces, message))

		return [chatPoss, toPrint]


def chat_name(username, friendUserName, friendDisplayName):
	''' API call to get chat messages '''
	response = requests.get(BASE + "chat_name", {'username':username, 'friend':friendUserName})
	result = response.json()

	convo = result['conversation']

	''' Present nicely '''
	border('Here is your conversation with {}'.format(friendDisplayName))
	[print("{}>> {}".format(message[0],message[1])) for message in convo]
	to_return = ["{}>> {}".format(message[0],message[1]) for message in convo]
	return to_return


def chat_new(username, friend_name):

	''' Create new conversation using API call '''
	requests.post(BASE + "chat_new", {'username':username, 'friend_name': friend_name})

	''' API call to find display name for friend '''
	response = requests.get(BASE + "display_name", {'username': friend_name})
	result = response.json()
	friend_display_name = result['display_name']
	return friend_display_name


def main():
	''' Pathway '''
	border('Welcome to chitChat!')

	while True: # Layer 1 - login/register/leave

		loggedIn = False

		print('Would you like to login, register or leave? ')
		print("(Type 'back' to return to previous stage at any time)")
		print('')
		response = input('')
		print('') # Line space

		''' Handling response '''
		if response == 'leave': break

		elif response != 'leave' and response != 'login' and response != 'register':

			print('Please choose from the following options.')
			print('')
			continue

		if response == 'register':

			''' Registering '''
			stillRegistering, registered = True, False
			while stillRegistering == True: # Keep users in loop while trying to register

				register_value = register()
				if register_value != None:
					if register_value == False:
						stillRegistering = False # If user pressed 'back', they restart process
						print('')

					else: # User successfully registers
						stillRegistering, registered = False, True

				else: print('') # If user entered incorrect values

			if registered == False: continue # Sends users back to login/register


		''' Logging in '''
		stillLoggingIn, loggedIn = True, False
		while stillLoggingIn == True: # Keep users in loop while trying to register

			try:
				success, username = login()

				if [success, username] == ['back', None]:
					stillLoggingIn = False
					print('')

				else: # User successfully logs in
					stillLoggingIn, loggedIn = False, True

			except: pass # If user entered incorrect values

		if loggedIn == False: continue # Sends users back to login/register


		border('Welcome {}, you are now logged in!'.format(username))

		while True: # Layer 2 - Home screen (view conversations)

			chatPoss, toPrint = home(username)

			for line in toPrint:
				print(line)

			if chatPoss != None: # User has ongoing conversations

				display_names = [poss[0] for poss in chatPoss] # Display names for friends user has conversations with

			else: # There are no ongoing conversations

				display_names = []

			print('')
			print("Chat with a friend in your conversations list by typing their display name,")
			print("start a new chat by typing 'new'")
			print("check for new messages with 'refresh'")
			print("or log-out of chat server by typing 'log-out'")
			print('')

			response = input('')

			if response == 'log-out':

				print('')
				break # Takes users back to login/registration

			elif response == 'refresh':

				print('')
				continue

			elif response not in display_names and response != 'new':

				print('Please choose from the following options.')
				print('')
				continue

			elif response == 'new': # User wants to start a new chat

				stillFindingFriend, foundFriend = True, False
				while stillFindingFriend == True: # Keep users in loop till they have found a friend to chat with

					''' Ask for friend's name '''
					maybeFriend = input('Please give the username for a friend you would like to chat to. ')
					print('')
					if maybeFriend == 'back': stillFindingFriend = False

					else: # Actual response

						''' Check if maybeFriend is actually a friend of their's '''
						result = requests.get(BASE + "friends_info", {'username': username}).json()
						friends = result['friends_info']

						if maybeFriend in friends:

							''' Create new conversation and jump into it '''
							friend_name = maybeFriend
							friend_display_name = chat_new(username, friend_name) # Create variable response so that it can be used in chat_name
							stillFindingFriend, foundFriend = False, True

						else: # User gave an invalid username

							print('You do not have a friend by that username, please try a different username.')
							print('')

				if foundFriend == False: continue # Sends user back to home screen
				if foundFriend == True: response = friend_display_name # Create variable response so that it can be used in chat_name


			''' Jump into an ongoing conversation '''
			chatPoss, toPrint = home(username) # Check if there are any new conversations added
			display_names = [poss[0] for poss in chatPoss] # Display names for friends user has conversations with
			user_names = [poss[1] for poss in chatPoss] # Display names for friends user has conversations with

			index = 0
			for name in display_names:
				if name == response:
					break
				index += 1
			friend_user_name = user_names[index] # Inelegant way of finding friend_user_name

			chat_name(username, friend_user_name, response)
			print('')


			while True: # Layer 3 - Sending messages

				''' Check for commands '''
				message = input('>> ')
				if message == 'back':

					print('')
					break # Send user back to home screen

				if message == 'refresh':

					chat_name(username, friend_user_name, response)
					print('')
					continue

				''' Send message '''
				requests.post(BASE + "send", {'username':username, 'friend_name':friend_user_name, 'message':message})
				chat_name(username, friend_user_name, response)
				print('')


if __name__ == "__main__":
	main()