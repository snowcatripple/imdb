#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

#===============
# Python Script for getting info from IMDb links
# 
#
# Written in Python 2.7.6
#===============

import praw
import time  # for sleep
import signal  # for setting up signal handler and signal constant
import imdb
import sys
import re
import requests
import pdb
import os

version = 1.0

# Create the Reddit instance
reddit = praw.Reddit("bot1")
#subreddit
subreddit = reddit.subreddit("bottest")

keep_on = True

#keep on
def kill_handler(sig, frame):
	global keep_on
	keep_on = False
signal.signal(signal.SIGUSR1, kill_handler)

ia=imdb.IMDb(accessSystem="http",adultSearch=0)
def get_imdb_data(imdb_id):
    try:
        if (imdb_id[0] + imdb_id[1] == 'tt'):
            movies = ia.search_movie(imdb_id)
            movie = movies[0]
            ia.update(movie)
            #for debug
            #print('found')
            return(movie)

        elif (imdb_id[0] + imdb_id[1] == 'nm'):
            names = ia.search_person(imdb_id)
            name = names[0]
            ia.update(name)
            #for debug
            #print('found')
            return(name)

    except IndexError:
        #for debug
        #print('not found')
        return('No Data')

def get_imdb_search(term,search):
	try:
		if (search == "movie"):
			movies = ia.search_movie(term)
			movie=movies[0]
			ia.update(movie)
			return(movie)
		elif (search == "actor"):
			names = ia.search_person(term)
			name = names[0]
			ia.update(name)
			return(name)
	except IndexError:
		return("No Data")

def reply2(type, info):
    

    if (type == 'movie'):
        dl = [d['name'] for d in info['director']] if (len(info['director']) > 1) else [info['director'][0]['name']] if (len(info['director']) == 1) else ['None']
        pl = [p['name'] for p in info['producer']] if (len(info['producer']) > 1) else [info['producer'][0]['name']] if (len(info['producer']) == 1) else ['None']
        cl = [c['name'] for c in info['cast'][0:10]] if (len(info['cast']) > 1) else [info['cast'][0]['name']] if (len(info['cast']) == 1) else ['None']
        director = ', '.join(dl) if (len(dl) < 10) else ', '.join(dl) + '...'
        producer = ', '.join(pl) if (len(pl) < 10) else ', '.join(pl) + '...'
        cast = ', '.join(cl) if (len(cl) < 10) else ', '.join(cl) + '...'
        genre = ', '.join(info['genres'])
		
        com = ('***[' + info['long imdb canonical title'] + '](http://imdb.com/title/tt' + info.movieID + ')***\n\n'
         + '\n\n**IMDB Rating:** ' + str(info['rating']) + '/10\n\n**Director(s):** ' + director
         + '\n\n**Producer(s):** ' + producer
         + '\n\n**Cast:** ' + cast
         + '\n\n**Synopsis:** ' + info['plot outline']
         + '\n\n**Genre:** ' + genre)

        return(com)

    elif (type == 'actor'):
        dl = [str(d.get('title')) for d in info.get('director')[0:10]] if info.get('director') is not None else ['None']
        director = ', '.join(dl) if (len(dl) < 10) else ', '.join(dl) + '...'
        pl = [str(p.get('title')) for p in info.get('producer')[0:10]] if info.get('producer') is not None else ['None']
        producer = ', '.join(pl) if (len(pl) < 10) else ', '.join(pl) + '...'
        wl = [str(w.get('title')) for w in info.get('writer')[0:10]] if info.get('writer') is not None else ['None']
        writer = ', '.join(wl) if (len(wl) < 10) else ', '.join(wl) + '...'
        al = [str(a.get('title')) for a in info.get('actor')[0:10]] if info.get('actor') is not None else ['None']
        actor = ', '.join(al) if (len(al) < 10) else ', '.join(al) + '...'

        com = ('***[' + info['long imdb canonical name'] + '](http://imdb.com/name/nm' + info.personID + ')***\n\n'
         + '\n\n**Born:** ' + str(info.get('birth date'))
         + '\n\n**Directed:** ' + director
         + '\n\n**Produced:** ' + producer
         + '\n\n**Wrote:** ' + writer
         + '\n\n**Acted in:** ' + actor)

        return(com)

    else:
        com = ''
        return(com)

		
	

def reply(type, info):
    ml = ''.join(m)

    if (type == 'tt'):
        dl = [d['name'] for d in info['director']] if (len(info['director']) > 1) else [info['director'][0]['name']] if (len(info['director']) == 1) else ['None']
        pl = [p['name'] for p in info['producer']] if (len(info['producer']) > 1) else [info['producer'][0]['name']] if (len(info['producer']) == 1) else ['None']
        cl = [c['name'] for c in info['cast'][0:10]] if (len(info['cast']) > 1) else [info['cast'][0]['name']] if (len(info['cast']) == 1) else ['None']
        director = ', '.join(dl) if (len(dl) < 10) else ', '.join(dl) + '...'
        producer = ', '.join(pl) if (len(pl) < 10) else ', '.join(pl) + '...'
        cast = ', '.join(cl) if (len(cl) < 10) else ', '.join(cl) + '...'
        genre = ', '.join(info['genres'])

        com = ('***[' + info['long imdb canonical title'] + '](http://imdb.com/' + ml + ')***\n\n'
         + '\n\n**IMDB Rating:** ' + str(info['rating']) + '/10\n\n**Director(s):** ' + director
         + '\n\n**Producer(s):** ' + producer
         + '\n\n**Cast:** ' + cast
         + '\n\n**Synopsis:** ' + info['plot outline']
         + '\n\n**Genre:** ' + genre)

        return(com)

    elif (type == 'nm'):
        dl = [str(d.get('title')) for d in info.get('director')[0:10]] if info.get('director') is not None else ['None']
        director = ', '.join(dl) if (len(dl) < 10) else ', '.join(dl) + '...'
        pl = [str(p.get('title')) for p in info.get('producer')[0:10]] if info.get('producer') is not None else ['None']
        producer = ', '.join(pl) if (len(pl) < 10) else ', '.join(pl) + '...'
        wl = [str(w.get('title')) for w in info.get('writer')[0:10]] if info.get('writer') is not None else ['None']
        writer = ', '.join(wl) if (len(wl) < 10) else ', '.join(wl) + '...'
        al = [str(a.get('title')) for a in info.get('actor')[0:10]] if info.get('actor') is not None else ['None']
        actor = ', '.join(al) if (len(al) < 10) else ', '.join(al) + '...'

        com = ('***[' + info['long imdb canonical name'] + '](http://imdb.com/' + ml + ')***\n\n'
         + '\n\n**Born:** ' + str(info.get('birth date'))
         + '\n\n**Directed:** ' + director
         + '\n\n**Produced:** ' + producer
         + '\n\n**Wrote:** ' + writer
         + '\n\n**Acted in:** ' + actor)

        return(com)

    else:
        com = ''
        return(com)

		

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))
		
# Get the top 5 values from our subreddit
while (keep_on):
	for comment in subreddit.comments(limit=10):
		#print(comment.title)

		# If we haven't replied to this post before
			
		if comment.id not in posts_replied_to:
			pattern1 = re.compile("http://www\.imdb\.com/(?:title/|name/)(?P<id1>tt|nm)(?P<id2>\d{7})/")
			match = pattern1.findall(comment.body)
			if not match:
				#continue
				# if re.search(r'linkimdb\((.*?)\)', comment.title, re.IGNORECASE):
				# search for linkimdb and search for names
					# print("linkimdb found : ", comment.title)
					# posts_replied_to.append(comment.id)
				#pattern2 = re.search(r'linkimdb\((.*?)\)', comment.body, re.IGNORECASE)
				#pattern2 = re.search('\((.*?)\)',pattern2.group(0),re.IGNORECASE)
				#pattern2 = re.search('\((.*?)\)',pattern2.group(0),re.IGNORECASE)
				
				#pattern2 = re.compile(r"\(([A-Za-z0-9_]+)\)") 
				pattern2 = re.compile(r"linkimdb(.*?)\)")
				match1 = pattern2.findall(comment.body)
				print(match1)
				if not match1:
					continue
				if match1:
					print("linkimdb found : ", comment)		
					coms = []
					posts_replied_to.append(comment.id)
					for m in match1:
						match3 = re.search("actor|movie",m)
						if (match3.group(0) == "actor"):
							searchterm = m.split("(")[1]
							info = get_imdb_search(searchterm,"actor")
							print("actor")
							if (info == "No Data"):
								print("No Data")
								continue
							else:
								com = reply2("actor",info)
								if (com == ""):
									continue
								else:
									coms.append(com)
						if (match3.group(0) == "movie"):
							searchterm = m.split("(")[1]
							info = get_imdb_search(searchterm,"movie")
							print("movie")
							if (info == "No Data"):
								print("No Data")
								continue
							else:
								com = reply2("movie",info)
								if (com == ""):
									continue
								else:
									coms.append(com)
						else:
							continue
						
					try:
						print("linkimdb coms")
						print(coms)
						if (len(coms) > 0):
							comment.reply('\n\n-----------------\n\n'.join(coms)
							+ '\n\n------------------------\n\n^^^[Questions/Comments/Suggestions?](http://www.reddit.com/message/compose/?to=kaevaeth&subject=IMDbBot) ^^^Version ^^^'
							+ str(version) + ' ^^^[Source](https://github.com)')
						else:
							with open("posts_replied_to.txt", "w") as f:
								for post_id in posts_replied_to:
									f.write(post_id + "\n")
					except requests.exceptions.HTTPError as err:
						if err.response.status_code in [502, 503, 504]:
				# these errors may only be temporary
							pass
						else:
				# assume other errors are fatal
							print str(err)
							print "Terminating"
						
			if match:
				print(comment)
				coms = []
				posts_replied_to.append(comment.id)
				for m in match:
					imdb = "".join(m)
					info = get_imdb_data(imdb)
					if (info == "No Data"):
						continue
					else:
						com = reply(m[0],info)
						if (com == ""):
							continue
						else:
							coms.append(com)
				try:
					if (len(coms) > 0):
						comment.reply('\n\n-----------------\n\n'.join(coms)
						+ '\n\n------------------------\n\n^^^[Questions/Comments/Suggestions?](http://www.reddit.com/message/compose/?to=kaevaeth&subject=IMDbBot) ^^^Version ^^^'
						+ str(version) + ' ^^^[Source](https://github.com)')
					else:
						with open("posts_replied_to.txt", "w") as f:
							for post_id in posts_replied_to:
								f.write(post_id + "\n")
				except requests.exceptions.HTTPError as err:
					if err.response.status_code in [502, 503, 504]:
			   # these errors may only be temporary
						pass
					else:
			   # assume other errors are fatal
						print str(err)
						print "Terminating"

	# Write our updated list back to the file
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")					
			time.sleep(5)
