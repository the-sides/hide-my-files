
all: 
	echo Building...
	chmod 755 ./lock
	chmod 755 ./unlock
	chmod 755 ./keygen
	pip3 install pycryptodome
