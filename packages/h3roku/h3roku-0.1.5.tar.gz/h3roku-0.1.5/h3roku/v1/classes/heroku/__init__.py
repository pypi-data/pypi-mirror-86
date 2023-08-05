#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from h3roku.v1.classes.config import *

# the heroku cli object class.
class Heroku(cl1.CLI):
	def __init__(self, package=Formats.FilePath(__file__).base()):
		
		# variables.
		self.package = Formats.FilePath(package)
		cl1.CLI.__init__(self, 
			modes={
				"--push":"Push to heroku.",
				"--tail":"Tail the heroku website logs.",
				"--add-env-variable MY_VARIABLE='helloworld' / --file /path/to/dict.json":"Add env variables to heroku.",
				"--remove-env-variable MY_VARIABLE":"Remove env variables from heroku.",
				"-h / --help":"Show the documentation.",
			},
			options={},
			alias="./heroku.py",
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
from h3roku import Heroku
from fil3s import Files, Formats
if __name__ == "__main__":
	heroku = Heroku(package=Formats.FilePath(__file__).base())
	heroku.start()


"""
