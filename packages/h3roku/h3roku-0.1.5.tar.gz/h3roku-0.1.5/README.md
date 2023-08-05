# h3roku
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install h3roku --upgrade

## Usage.
Create a file named: heroku.py in the root website directory.
	
	#!/usr/bin/env python3
	from h3roku import Heroku
	from fil3s import Files, Formats
	if __name__ == "__main__":
		heroku = Heroku(package=Formats.FilePath(__file__).base())
		heroku.start()

## CLI:
	Usage: ./heroku.py <mode> <options> 
	Modes:
	    --push : Push to heroku.
	    --tail : Tail the heroku website logs.
	    --add-env-variable MY_VARIABLE='helloworld' / --file /path/to/dict.json : Add env variables to heroku.
	    --remove-env-variable MY_VARIABLE : Remove env variables from heroku.
	    -h / --help : Show the documentation.
	Author: Daan van den Bergh. 
	Copyright: © Daan van den Bergh 2020. All rights reserved.

## Python Examples.

Controlling a heroku package from python.
```python

# import the package.
from h3roku import Heroku
from fil3s import Files, Formats

# initialize the package.
heroku = Heroku(package=Formats.FilePath(__file__).base())

# check the package.
heroku.check()

# push to heroku.
heroku.push()

# tail the logs.
heroku.tail()

# add environment variables.
heroku.add_environment_variables({
	"Hello":"World!"
})

# remove environment variables.
heroku.remove_environment_variables({
	"Hello":None,
})

# get environment variables (logs to console).
heroku.get_environment_variables({
	"Hello":None,
})

# start the cli.
heroku.start()

```
