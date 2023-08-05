#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, pathlib
def __get_file_path_base__(path, back=1):
	path = path.replace('//','/')
	if path[len(path)-1] == "/": path = path[:-1]
	string, items, c = "", path.split("/"), 0
	for item in items:
		if c == len(items)-(1+back):
			string += "/"+item
			break
		else:
			string += "/"+item
		c += 1
	return string+"/"

# source.
ALIAS = "nas-client"
SOURCE_NAME = "nas-client"
VERSION = "v1"
SOURCE_PATH = __get_file_path_base__(__file__, back=2)
sys.path.insert(1, f"{SOURCE_PATH}/{VERSION}")

# imports.
from classes.config import *
from classes import utils
from classes.manager import manager
from classes.automount import automount
VERSION = "v1"

	def start(self):

		# clear logs option.
		if not self.argument_present('-c'): 
			os.system("clear")

		# help.
		if self.argument_present('-h') or self.argument_present('--help'):
			print(self.documentation)

		# start.
		elif self.argument_present('--start'):

			# start the web server.
			if not os.path.exists(f"{SOURCE_PATH}/{VERSION}/db.sqlite3"):
				os.system(f"cd {SOURCE_PATH}/{VERSION}/ && ./manage.py migrate")
			os.system(f"cd {SOURCE_PATH}/{VERSION}/ && ./manage.py runserver")

		# automount.
		elif self.argument_present('--agent'):

			# start the ssh agent.
			if self.argument_present('--start'):

				# activate encryption.
				self.__activate_encryption__()

				# activate clients.
				response = manager.activate_clients()
				if response["error"] != None: print(response["error"])
				else: print(response["message"])

				# activate smart cards.
				response = ssht00ls.smart_cards.__single_key_plugged_in__()
				if response["success"]:
					smart_card = response["smart_card"]
					try:
						attempts = int(smart_cards.info()["pin_attempts"])
						if attempts == 1:
							print("Warning your card will be blocked upon an incorrect pin!\nPin attempts left:",attempts)
						elif attempts == 2:
							print("Warning! Pin attempts left:",attempts)
						else: print("Pin attempts left:",attempts)
					except: a=1
					serial_number = smart_card.serial_number
					response = ssht00ls.agent(
						path=ssht00ls.smart_cards.path,
						smart_card=True,
						pin=utils.__prompt_password__(f"Enter the pin of smart card [{serial_number}]:",))
					if response["error"] != None: print(response["error"])
					else: print(response["message"])

			# start the ssh agent.
			elif self.argument_present('--stop'):
				os.system("ssh-add -D")

			# invalid.
			else: 
				print(self.documentation)
				print("Selected an invalid mode.")

		# automount.
		elif self.argument_present('--automount'):

			# mount targets.
			if self.argument_present('--mount'):
			
				# activate clients.
				response = automount.mount()
				if response["error"] != None: print(response["error"])
				else: print(response["message"])

			# mount targets.
			elif self.argument_present('--unmount'):
			
				# activate clients.
				response = automount.unmount()
				if response["error"] != None: print(response["error"])
				else: print(response["message"])

			# mount targets.
			elif self.argument_present('--remount'):
			
				# activate clients.
				response = automount.remount()
				if response["error"] != None: print(response["error"])
				else: print(response["message"])

			# invalid.
			else: 
				print(self.documentation)
				print("Selected an invalid mode.")

		# install a new key.
		elif self.argument_present('--install'):

			# smart card.
			if self.argument_present('--smart-cards'):

				# install client.
				serial_numbers = []
				for i in self.get_argument("--serial-numbers").split(','):
					for x in range(101):
						if len(i) > 0 and i[0] == " ": i = i[1:]
						elif len(i) > 0 and i[len(i)-1] == " ": i = i[:-1]
						else: break
					serial_numbers.append(i)
				response = manager.install_client(
					# the username.
					username=self.get_argument("--username"), 
					# the servers alias. (example:vandenberghinc.com)
					server=self.get_argument("--server"), 
					# the lan ip address of the server.
					lan_ip=self.get_argument("--lan-ip"), 
					# the wan ip address of the server.
					wan_ip=self.get_argument("--wan-ip"),
					# the lan ssh port of the server.
					lan_ssh_port=self.get_argument("--lan-ssh-port"),
					# the wan ssh port of the server.
					wan_ssh_port=self.get_argument("--wan-ssh-port"),
					# option 1:
					# the new passphrase for the private key.
					new_passphrase=None, 
					# the old passphrase for the private key.
					old_passphrase="''",  # (no passphrase)
					# the path to the private key.
					private_key=None, 
					# the path to the private key.
					public_key=None, 
					# option 2:
					# enable for smart cards.
					smart_cards=True,
					# serial numbers of the smart cards.
					serial_numbers=serial_numbers,)
				# response is already printed inside for this function only.

			# non smart card.
			else:

				# check encryption.
				if not os.path.exists(ENCRYPTION.key):

					# create pass & install & activate encryption.
					print(f"{utils.color.red}WARNING:{utils.color.yellow} the passphrase of the master encryption key can not be recovered. If you lose this passphrase you will have to reinstall all installed clients.{utils.color.end}")
					passphrase = utils.__prompt_password__("Enter a passphrase for the master encryption key:")
					verify_passphrase = utils.__prompt_password__("Enter the same passphrase:")
					response = manager.install_encryption(
						passphrase=passphrase,
						verify_passphrase=verify_passphrase,)
					if response["error"] != None:
						print(response['error'])
						sys.exit(1)

				else:

					# activate encryption.
					self.__activate_encryption__()

				# install client.
				old_passphrase = self.get_argument("--old-passphrase")
				if old_passphrase in ["none", ""]: old_passphrase = '""'
				response = manager.install_client(
					# the username.
					username=self.get_argument("--username"), 
					# the servers alias. (example:vandenberghinc.com)
					server=self.get_argument("--server"), 
					# the lan ip address of the server.
					lan_ip=self.get_argument("--lan-ip"), 
					# the wan ip address of the server.
					wan_ip=self.get_argument("--wan-ip"),
					# the lan ssh port of the server.
					lan_ssh_port=self.get_argument("--lan-ssh-port"),
					# the wan ssh port of the server.
					wan_ssh_port=self.get_argument("--wan-ssh-port"),
					# option 1:
					# the new passphrase for the private key.
					new_passphrase=Formats.String("").generate(length=48, digits=True, capitalize=True, special=True), 
					# the old passphrase for the private key.
					old_passphrase=old_passphrase,  # (no passphrase)
					# the path to the private key.
					private_key=self.get_argument("--private-key"), 
					# the path to the private key.
					public_key=self.get_argument("--public-key"), 
					# option 2:
					# enable for smart cards.
					smart_cards=False,
					# serial numbers of the smart cards.
					serial_numbers=None,)
				# response is already printed inside for this function only.

		# create an alias.
		elif self.argument_present('--create-alias'):
			file = f"""package={SOURCE_PATH}/{VERSION}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
			os.system(f"sudo touch /usr/local/bin/{self.alias}")
			os.system(f"sudo chmod 755 /usr/local/bin/{self.alias}")
			if OS in ["osx"]:
				os.system(f"sudo chown {os.environ.get('USER')}:wheel /usr/local/bin/{self.alias}")
			elif OS in ["linux"]:
				os.system(f"sudo chown {os.environ.get('USER')}:root /usr/local/bin/{self.alias}")
			utils.__save_file__(f"/usr/local/bin/{self.alias}", file)
			os.system(f"sudo chmod 755 /usr/local/bin/{self.alias}")
			print(f'Successfully created alias: {self.alias}.')
			print(f"Check out the docs for more info $: {self.alias} -h")

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	# system functions.
	def __activate_encryption__(self):
		# activate encryption.
		passphrase = utils.__prompt_password__("Enter the passphrase of the master encryption key:")
		response = manager.activate_encryption(
			passphrase=passphrase,)
		if response["error"] != None:
			print(response['error'])
			sys.exit(1)
	





#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from h3roku.v1.classes.config import *


# the cli object class.
class Heroku(cl1.CLI):
	def __init__(self, package=Formats.FilePath(__file__).base()):
		
		# variables.
		cl1.CLI.__init__(self, 
			modes={
				"--push":"Push to heroku.",
				"--tail":"Tail the heroku website logs.",
				"--add-env-variable MY_VARIABLE='helloworld' / --file /path/to/dict.json":"Add env variables to heroku.",
				"--remove-env-variable MY_VARIABLE":"Remove env variables from heroku.",
				"-h / --help":"Show the documentation.",
			},
			options={},
			alias="heroku",
			executable=__file__,)

		#
	def start(self):
		if "-h" in sys.argv or "--help" in sys.argv:
			print(self.documentation)
		elif '--push' in sys.argv:
			self.push()
		elif '--tail' in sys.argv:
			self.tail()
		elif '--add-env-variable' in sys.argv:
			key = self.get_argument("--add-env-variable")
			if key == "--file":
				path, dict = self.get_argument("--file"), None
				with open(path, "r") as json_file: dict = json.load(json_file)
				self.add_environment_variables(dict)
			else:
				key, value = key.split("=")
				self.add_environment_variables({
					key: value
				})
		elif '--remove-env-variable' in sys.argv:
			key = self.get_argument("--remove-env-variable")
			if key == "--file":
				path, dict = self.get_argument("--file"), None
				with open(path, "r") as json_file: dict = json.load(json_file)
				self.remove_environment_variables(dict)
			else:
				self.remove_environment_variables({
					key: ""
				})
		else:
			print(self.documentation)
			print("Selected an invalid mode.", mode="warning")
	def check(self):
		os.system("cd "+self.package.file_path.path)
		os.system("heroku ps:scale web=1")
		os.system("./manage.py makemigrations")
		os.system("./manage.py migrate")
	def tail(self):
		os.system("cd "+self.package.file_path.path)
		os.system("heroku logs --tail")
	def push(self):
		print("Pushing to heroku.")
		commands = [
			"cd "+self.package.file_path.path,
			"git add .",
			"git commit -am 'automatic updates'",
			"git push heroku master",
		]
		for command in commands: 
			os.system(command)
	def add_environment_variables(self, variables={}):
		c = "cd "+self.package.file_path.path
		c += " && heroku config:set"
		for key, value in variables.items():
			c += " {}='{}'".format(key, value)
		os.system(c)
	def remove_environment_variables(self, variables={}):
		os.system("cd "+self.package.file_path.path)
		for key, value in variables.items():
			os.system("heroku config:unset {}".format(key, value))
	def get_environment_variables(self, variables={}):
		os.system("cd "+self.package.file_path.path)
		for key, value in variables.items():
			os.system("heroku config:get {}".format(key))

"""
Create a file named: heroku.py in the root package directory.
#!/usr/bin/env python3
if __name__ == "__main__":
	heroku = Heroku(package=Formats.FilePath(__file__).base())
	heroku.start()


"""
