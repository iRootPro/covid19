

def add_member(chat_id):
	with open('members.txt', 'a') as file:
		file.write(str(chat_id))
		file.write('\n')

def check_member(chat_id):
	with open('members.txt', 'r') as file:
		members = file.read().splitlines()
	print(members)
	if str(chat_id) in members:
		return True
	return False


# def main():
# 	chat_id = 40001
# 	if check_member(chat_id):
# 		print('Вы уже подписаны')
# 	else:
# 		add_member(chat_id)
# 		print('Вы успешно подписаны. Спасибо.')

# if __name__ == '__main__':
# 	main()