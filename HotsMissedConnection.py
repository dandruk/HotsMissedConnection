#Title: HOTS Missed Connection
#Description: find games where two given players were present
#Author: dandruk (https://github.com/dandruk)

import PySimpleGUI as sg	#GUI
import requests as rq		#HTTP requests
import json

from datetime import datetime, timedelta

#opens dialog window for input values
def run_GUI():
	layout = [
		[sg.Text('First Player Name: ', auto_size_text=True, justification='right'), sg.InputText('')],
		[sg.Text('Second Player Name: ', auto_size_text=True, justification='right'), sg.InputText('')],
		[sg.Text('Search how many days? ', auto_size_text=True, justification='right'), sg.InputText('30')],
		[sg.Submit()]
		]
		
	window = sg.Window('HOTS Missed Connection', auto_size_text=True, default_element_size=(40, 1)).Layout(layout)
	event, values = window.Read()
	window.Close()
	
	return values #return first input, which is the selected directory

#get start date for hotsapi url
# -- should this have a max value to keep requests small?
def get_start(minus_days):
	#get date for today
	dt_today = datetime.now()
	#get date for start of time period
	dt_start = dt_today - timedelta(days=int(minus_days))
	#convert to format for hotsapi
	start = dt_start.strftime("%Y-%m-%d")
	
	return start

# request list of replay IDs for a player
def get_ids(player, start_date):
	page_n = 1
	r_json = []
	replay_ids = []
	
	#loop through incrementing pages of requests for replays (100 per page)
	replays_exist = True
	while replays_exist:
		#create request string
		r_string = 'https://hotsapi.net/api/v1/replays/paged?page=' + str(page_n) + '&start_date=' + start_date + '&player=' + player
		
		#make request
		r = rq.get(r_string)
		if (r):
			r_text = r.json()
		else:
			print ("Request error")
			break
		
		#exit loop when there are no replays on this page
		if not r_text["replays"]:
			replays_exist = False
		#if replays found, increment page number and add replay ids to list
		else:
			page_n += 1
			for replay in r_text["replays"]:
				replay_ids.append(replay['id'])
		
	return replay_ids
		
# return a list of ids shared by a and b
def get_shared_ids(ids_1, ids_2): 
	#create sets
	set_1 = set(ids_1)
	set_2 = set(ids_2)
	
	shared_ids = set_1.intersection(set_2)
	
	# check length  
	if len(shared_ids) > 0:
		return(shared_ids)
	else: 
		return([])
		
# output shared IDs
def window_output(list):
	if not list:
		sg.Popup("No shared replay IDs were found")
	else:
		out_str = ", ".join(map(str, list))
		sg.Popup("Shared replay IDs:\n\n" + out_str)

	
#PROGRAM START

values = run_GUI()

player_1 = values[0]
player_2 = values[1]
start = get_start(values[2])

ids_1 = get_ids(player_1, start)
ids_2 = get_ids(player_2, start)

shared_list = get_shared_ids(ids_1, ids_2)

window_output(shared_list)

