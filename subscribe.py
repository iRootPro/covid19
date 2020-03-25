def add_member(chat_id):
	with open('members.txt', 'w') as file:
		file.write(str(chat_id))
