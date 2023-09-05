#!/usr/bin/python3
import requests
import json
import sys
import argparse
import traceback
import re
from termcolor import colored
from pyfiglet import Figlet

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"} 			# Spoof UA
proxies={"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}										# proxy settings
line_width = 170
#	

def fetchdata():
	global mediaflag,postsflag,usersflag,mediaID,postID,userID
	print("[+] Fetching endpoints from WP-JSON...")
	r = requests.get(url,headers=headers)
	if r.status_code != 200:
		print("WP-JSON does not seem to be accessible :( \nExiting...")
		sys.exit()
	print("[+] REST Endpoints successfully fetched.")
	if usersflag or (not postsflag and not mediaflag and not usersflag):
		try:
			print("[+] Fetching a valid user ID...")
			usersR = requests.get(url+'/wp/v2/users',headers=headers)
			userID = int(usersR.text[usersR.text.index(':')+1:usersR.text.index(',')])
			print("[+] Valid user ID -> " + str(userID))
		except:
			print("Unable to fetch user ID.")
		
	if mediaflag or (not postsflag and not mediaflag and not usersflag):
		try:
			print("[+] Fetching a valid media ID...")
			mediaR = requests.get(url+'/wp/v2/media',headers=headers)
			mediaID = int(mediaR.text[mediaR.text.index(':')+1:mediaR.text.index(',')])
			print("[+] Valid media ID -> " + str(mediaID))
		except:
			print("Unable to fetch media ID.")
	if postsflag or (not postsflag and not mediaflag and not usersflag):
		try:
			print("[+] Fetching a valid post ID...")
			postsR = requests.get(url+'/wp/v2/posts',headers=headers)
			postID = int(postsR.text[postsR.text.index(':')+1:postsR.text.index(',')])
			print("[+] Valid post ID -> " + str(postID))
			
		except:
			print("Unable to fetch post ID.")
	print('[+] Initiating scan...')
	return r
	
def banner():
	banner = Figlet(font='standard')
	print(banner.renderText('WP-REST-SCAN'))
	

def output(method,url,status):
	global users,media,posts
	if '/users' in url and users==1:
		print(colored("USERS ENDPOINTS",'blue'))
		users=0
	if '/media' in url and media==1:
		print(colored("MEDIA ENDPOINTS",'blue'))
		media=0
	if '/posts' in url and posts==1:
		print(colored("POSTS ENDPOINTS",'blue'))
		posts=0
	if status == 200:
		print(str(method) + "\t" + str(url).ljust(line_width) + "\t",colored(str(status),'green'))
	elif status == 400:
		print(str(method) + "\t" + str(url).ljust(line_width) + "\t",colored(str(status),'yellow'))
	elif status == 401:
		print(str(method) + "\t" + str(url).ljust(line_width) + "\t",colored(str(status),'red'))
	elif status == 500:
		print(str(method) + "\t" + str(url).ljust(line_width) + "\t",colored(str(status),'blue'))
	else:
		print(str(method) + "\t" + str(url).ljust(line_width) + "\t",colored(str(status),'white'))

def main():

	
	global mediaflag,postsflag,usersflag
	r = fetchdata()
	jsondata=r.json()
	routes = jsondata['routes']
	for route in routes:
		if mediaflag and not usersflag and not postsflag:
			if not '/media' in route:
				continue
		if usersflag and not mediaflag and not postsflag:
			if not '/users' in route:
				continue
		if postsflag and not mediaflag and not usersflag:
			if not '/posts' in route:
				continue
		if postsflag and mediaflag and usersflag:
			if not '/posts' in route or not '/media' in route or not '/posts' in route:
				continue
		if postsflag and mediaflag and not usersflag:
			if not '/posts' in route and not '/media' in route:
				continue
		if postsflag and usersflag and not mediaflag:
			if not '/posts' in route and not '/users' in route:
				continue
		if usersflag and mediaflag and not postsflag:
			if not '/users' in route and not '/media' in route:
				continue 
		for endpoint in routes[route]['endpoints']:
			for method in endpoint['methods']:
				if '?P' in route:
					if '/media' in route and mediaID:
						route = re.sub("\(\?P.+\)",str(mediaID),route)
					elif '/posts' in route and postID:
						route = re.sub("\(\?P.+\)",str(postID),route)
					elif '/users' in route and userID:
						route = re.sub("\(\?P.+\)",str(userID),route)
					else:
						route = re.sub("\(\?P.+\)","1",route)
				finalurl = url + route + '?'
				postdata = {}
				try:
					if method == 'GET' or method == 'DELETE':
						for arg in endpoint['args']:
							if str(endpoint['args'][arg]["required"]) == "True":
								if endpoint['args'][arg]['type'] == 'string':
									if str(arg) == 'url':
										finalurl = finalurl + '&' + arg + '=' + oob
									else:
										finalurl = finalurl + '&' + arg + '=view'
								else:
							 		finalurl = finalurl + '&' + arg + '=1'
						response = requests.get(finalurl,headers=headers)
					if method == 'PATCH' or method == 'POST' or method == 'PUT':
						for arg in endpoint['args']:
							if str(endpoint['args'][arg]["required"]) == "True":
								if endpoint['args'][arg]['type'] == 'integer':
									y = {arg:1}
								elif str(arg) == 'url':
									y = {arg:oob}
								else:
							 		y = {arg:"view"}
								postdata.update(y)
					if method == 'GET':
						response = requests.get(finalurl,headers=headers)
					if method == 'DELETE':
						response = requests.delete(finalurl,headers=headers)
					if method == 'POST':
						response = requests.post(finalurl,headers=headers,json=postdata)
					if method == 'PATCH':
						response = requests.patch(finalurl,headers=headers,json=postdata)	
					if method == 'PUT':
						response = requests.put(finalurl,headers=headers,json=postdata)
						
					output(method,finalurl,response.status_code)
				except KeyboardInterrupt:
					sys.exit()
				except Exception:
					#print(traceback.format_exc())
					pass
	



if __name__ == "__main__":
	banner()
	parser = argparse.ArgumentParser(description="WP-REST-SCAN",usage="\nFull Scan\npython3 wp-rest-scan.py -u https://wordpress.blog\n\nAdd OOB Url\npython3 wp-rest-scan.py -u https://wordpress.blog -oob https://webhook.server\n\nMedia/Image Endpoints Only\npython3 wp-rest-scan.py -u https://wordpress.blog --media\n\nUser Endpoints Only\npython3 wp-rest-scan.py -u https://wordpress.blog --users\n\nPosts Endpoints Only\npython3 wp-rest-scan.py -u https://wordpress.blog --posts")
	parser.add_argument("-u", "--url", help="Wordpress URL", required=True)
	parser.add_argument("-oob","--oob", nargs="?", const="default-oob-url",default="default-oob-url")
	parser.add_argument("-m","--media",default=False, required=False, const=True, nargs='?')
	parser.add_argument("-us","--users",default=False, required=False, const=True, nargs='?')
	parser.add_argument("-p","--posts",default=False, required=False, const=True, nargs='?')
	args = parser.parse_args()
	global url,oob,media,posts,users,postsflag,mediaflag,usersflag
	url=vars(args)['url']+'/wp-json'
	oob=str(vars(args)['oob'])
	postsflag=int(vars(args)['posts'])
	usersflag=int(vars(args)['users'])
	mediaflag=int(vars(args)['media'])
	media=1
	posts=1
	users=1
	main()
