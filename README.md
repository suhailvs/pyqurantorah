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

	$ sudo apt install python3-tk vlc
	$ pip install arabic-reshaper
	$ pip install AwesomeTkinter
	$ pip install python-vlc


Run the app:

	$ cd pyqurantorah
    $ python3 main.py

only audio files of 113(falaq), 114(an naas) exists, you can copy files to `static/audio` folder

Make Ubuntu Executable file
---------------------------

	pip install pyinstaller
	pyinstaller main.py --onefile
	cp -r static dist/
	./dist/main