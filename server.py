import discord
from discord.ext import commands
from flask import Flask, render_template, request, Response
from threading import Thread

users_list = []

app = Flask('')

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'GET':
		print("get req")
		return render_template("index.html")
	if request.method == 'POST':
		print("post")
	global users_list

	authorization = request.headers.get("Authorization")
	print(request.content_type)

	if authorization == "abcd":

		users_list.append(request.json)
		print(request.json)

	else:

		print("bruh")

	return render_template("index.html")

def run():
  app.run(host='0.0.0.0',port=5000)

def keep_alive():  
    t = Thread(target=run)
    t.start()