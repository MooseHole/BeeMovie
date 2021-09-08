import praw
from praw.models import MoreComments
import re

reddit = praw.Reddit(client_id='client_id',
user_agent='Bee Movie crawler by u/Moose_Hole',
client_secret='client_secret',
redirect_uri='http://localhost:8080')
print(reddit.auth.url(["identity"], "...", "permanent"))
	
submission = reddit.submission('ofiegh')
file = open("beemovie.txt", "r")
print("File loaded")

#startComment = "h4cpba4" # The beginning, number 1
#startCharNum = 1

#startComment = "h4gdmrg" # After a bunch of deletes, number 1800
#startCharNum = 1800

startComment = "h4i3y4x" # Used to have a double quote in the example after this, number 2500
startCharNum = 2500


charNumber = 0
char = ''

def getChar():
	global char
	global charNumber
	char = file.read(1)
	charNumber = charNumber + 1

for i in range(startCharNum):
	getChar()

lastComments = []
currentComments = []

def doComments(comment):
	done = False
	for reply in comment.replies:
		done = done or printIt(reply)
	if not done:
		for reply in comment.replies:
			if isinstance(reply, MoreComments):
				comment.replies.replace_more()
		for reply in comment.replies:
			done = done or printIt(reply)
	return done

def match(character, body):
	if character == body:
		return True
	m = re.search(r"\[([A-Za-z0-9_]+)\]", body)
	if m is not None and character == m.group(1):
		return True
	return False

def printIt(comment):
	global char
	global lastComment
	global charNumber
	if not isinstance(comment, MoreComments) and match(char, comment.body):
		author = "[deleted]"
		if comment.author is not None:
			author = comment.author.name
			
		print(comment.body + " by " + author + " at " + str(comment.created_utc) + " id " + comment.id + " #" + str(charNumber))
		currentComments.append(comment)
		return True
	return False

comment = reddit.comment(startComment)
comment.refresh()
printIt(comment)

lastComments = currentComments.copy()
currentComments = []

while 1:
	getChar()
	done = False
	for comment in lastComments:
		done = done or doComments(comment)
	if not done:
		for comment in lastComments:
			comment.refresh()
		for comment in lastComments:
			done = done or doComments(comment)
		if not done:
			lastCommentList = ""
			for c in lastComments:
				lastCommentList = lastCommentList + c.id + " "
			print("NO MATCH for character " + char + " in comment ids " + lastCommentList + ", end")
			break

	lastComments = currentComments.copy()
	currentComments= []


		