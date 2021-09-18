#!/usr/bin/python3

if __name__=="__main__":

	# executable in ubuntu: https://stackoverflow.com/a/64641595/2351696

	from forms import home 
	root=home.Tk()
	root['bg']='black'
	root.resizable(0,0)
	frmmenu=home.FormMenu(root)
	root.mainloop()
