SRC := ecw.py
PREFIX ?= /usr/local/bin

.PHONY:	install format

all:
	$(error Targets must be run directly)

install:
	pip3 install -r requirements.txt
	rm $(PREFIX)/ecw
	ln -s `pwd`/ecw.py $(PREFIX)/ecw

format:
	black $(SRC)
