import time

def scroll(text):
	i = 0
	length = len(text)
	output = ""
	while length != i:
		output = output+text[i]
		print(output, end="\r")
		i = i+1
		time.sleep(0.03)
	print()