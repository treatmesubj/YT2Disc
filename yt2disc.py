import sys
import requests
from requests_html import HTML
import re
import json
from pprint import pprint


if __name__ == "__main__":
	print(
		"""
		 __  ___________  ___  _        
		 \\ \\/ /_  __/_  |/ _ \\(_)__ ____
		  \\  / / / / __// // / (_-</ __/
		  /_/ /_/ /____/____/_/___/\\__/ 

		"""
			)

	# obtain video-url
	try:
		link = sys.argv[1]
	except IndexError:
		link = input("Video-URL: ")

	# request html, locate js
	while True:
		try:
			html = HTML(html=requests.get(link).text)
			script = html.find("body div#player div script")[-1].text
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
	fmts_list = sd_dict["adaptiveFormats"]  # list of fmt_dicts

	# display potential formats
	for fmt_opt, fmt in enumerate(fmts_list):
		print(f"Format Option {fmt_opt}:")
		pprint(fmt)
		print("-"*50)

	# choose format
	while True:
		try:
			fmt_choice = int(input("\nSelect a Format Option from above: "))
			break
		except Exception:
			print("Invalid selection; please try again...")
