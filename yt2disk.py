import sys
import os
import requests
from requests_html import HTML
import re
import json
from pprint import pprint
import win32api


if __name__ == "__main__":
	print(
		"""
		 __  ___________  ___  _     __  
		 \\ \\/ /_  __/_  |/ _ \\(_)__ / /__
		  \\  / / / / __// // / (_-</  '_/
		  /_/ /_/ /____/____/_/___/_/\\_\\ 
		"""
			)

	# obtain video-url
	try:
		link = sys.argv[1]
	except IndexError:
		link = input("Video-URL: ")

	# request html, determine title, locate js
	while True:
		try:
			html = HTML(html=requests.get(link).text)
			script = html.find("body div#player div script")[-1].text
			print("-"*50)
			break
		except IndexError:
			print("something happened, trying again...")

	# extact info from js
	config_from_re = re.search(r'ytplayer\.config = \{(.+?)\};', script).group(1)
	config_json = f"{{{config_from_re}}}"
	config_dict = json.loads(config_json)
	pr_json = config_dict["args"]["player_response"]
	pr_dict = json.loads(pr_json)
	sd_dict = pr_dict["streamingData"]

	title = pr_dict['videoDetails']['title']
	fmts_list = sd_dict["formats"] + sd_dict["adaptiveFormats"]

	# display potential formats
	for fmt_opt, fmt in enumerate(fmts_list):
		if 'audioQuality' in fmt.keys() and 'video' in fmt['mimeType']:
			print(f"Format Option [{fmt_opt}]:  (Video & Audio)\n")
		else:
			print(f"Format Option [{fmt_opt}]:\n")
		pprint(fmt)
		print("-"*50)

	# choose format
	while True:
		try:
			fmt_choice = fmts_list[int(input("\nSelect a Format Option from above: "))]
			break
		except Exception as e:
			print(e)
			print("Invalid selection; please try again...")

	# write file to disk
	file_ext = fmt_choice['mimeType'].split(";")[0].split("/")[1]
	dir_loc = f"C:\\Users\\{win32api.GetUserName()}\\Desktop"
	file_path = f"{dir_loc}\\{title}.{file_ext}"
	if os.path.exists(file_path):
		os.remove(file_path)
	with open(file_path, "wb") as f:
		print("writing file...")
		f.write(requests.get(fmt_choice['url']).content)
	print("done")
