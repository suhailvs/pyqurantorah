Quran Torah
===========

if you’d like to help out, hop on over to GitHub and send us a pull request!

Windows installation
--------------------

pyqurantorah is a quran and torah learning software developed using python3.2 tkinter and sqlite3. You need only python3x software installed on windows to run this. tkinter and sqlite3 modules are built in python3.x so no need to install these packages


Linux Installation
------------------

For linux os:

Install Python3 Tkinter Package:

	$ sudo apt-get install python3-tk

Run the app:

	$ cd pyqurantorah
    $ python3 main.py



Make Ubuntu Executable file
---------------------------

	pip install pyinstaller
	pyinstaller main.py --onefile
	cp -r static dist/
	./dist/main