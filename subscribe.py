def add_member(chat_id):
	with open('members.txt', 'a') as file:
		file.write(chat_id)
		