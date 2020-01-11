from bs4 import BeautifulSoup  as soup
from urllib.request import urlopen
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv

def searchInfo(*args):
	status.set("Status: Searching for : "+search.get())
	#the url of the website i am going to scrape
	url="https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=Desktop&ignorear=0&N=-1&isNodeId=1"
	url=url.replace("Desktop",search.get())
	uclient=urlopen(url)
	
	#the html to the website
	html=uclient.read()
	mysoup=soup(html,"html.parser")
	uclient.close()
	products=mysoup.findAll("div",{"class":"item-container"})
	file=search.get()+".csv"
	f=open(file,"w")

	x=""
	#loop through all products
	f.write("Brand, Product_name, Price($)\n")#The csv header
	x+="Brand, Product_name, Price($)\n"
	for product in products:
		try:
			make=product.div.div.a.img["title"]
			product_title=product.findAll("a",{"class":"item-title"})
			name=product_title[0].text
			product_price=product.findAll("li",{"class":"price-current"})
			price=product_price[0].text.strip()[0:9]
			price=price[price.index("$")+1:price.index(".")+3]
		except:
			continue
		x+=make+","+name.replace(",", "|")+","+price.replace(",","")+"\n"
		f.write( make+","+name.replace(",", "|")+","+price.replace(",","")+"\n")
	output_Text.insert(END,x)
	status.set("Status: Search complete. Showing the raw "+file)
	sortable.set(False)


def saveFile():
	#This will save a file
	filename = filedialog.asksaveasfilename()
	with open(filename,"w") as f:
		f.write(output_Text.get(1.0,END))
	status.set("Status: The contents of the text area have been written to "+filename)


def copyContent():
	#add the contents of the text field to the clip board
	root = Tk()
	root.withdraw()
	root.clipboard_clear()
	root.clipboard_append(output_Text.get(1.0,END))
	root.update()
	status.set("Status: Contents copied to clipboard")

def helpUser():
	#pop up with information on how to use the application
	messagebox.showinfo("Help", "The search box is for searching different electronics and save the scraped data as a csv file.\n\
\nThe file dropdown menu has an open menu for opening the saved csv files for analysis and a save to save the analysed \
data as a text file.\n\nFinally you have the edit menu with copy contents which copies all the contents in the large text area into \
the clipboard and the clear cmmand that clears everything in the text area.")

def openFile():
	#This will load a new file
	filename = filedialog.askopenfilename()
	if(filename.endswith(".csv")):
		status.set("Status: "+filename+" open")
		with open(filename) as f:
			reader= csv.reader(f)
			next(reader,None)
			x=""

			for row in reader:
				x+="Product Name: "+row[1]+"\n  \t\t Price:"+"$"+row[2]+"*\n\n"
				products.setdefault(row[1],row[2])
			output_Text.delete(1.0,END)
			output_Text.insert(END,x)
			sortable.set(True)


def clearContent():
	#add the contents of the text field to the clip board
	output_Text.delete(1.0,END)
	status.set("Status: Content has been cleared")
	sortable.set(False)

def sortInfo():
	tosort=[]

	if sortable.get():
		for key in products.keys():
			tosort.append(key)
		tosort.sort()
		x=""
		for i in tosort:
			x+="Product Name: "+i+"\n  \t\t Price:"+"$"+products[i]+"*\n\n"
		output_Text.delete(1.0,END)
		output_Text.insert(END,x)
		sortable.set(False)
	else:
		messagebox.showinfo("Ooops!!","Sorry could not sort this data. Open a csv file to enable sorting")






#set up the GUI
#The window
root= Tk()
root.title("Webscraper")



frame=ttk.Frame(root , padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

search= StringVar()
status= StringVar()
status.set("Status:")
products={}
sortable=BooleanVar()


search_entry = ttk.Entry(frame, width=16, textvariable=search)
search_entry.grid(column=1, row=1, sticky=(W, E))


search_button=ttk.Button(frame, text="Search", command=searchInfo).grid(column=2, row=1, sticky=W)

output_Text=Text(frame, width=140, height=40)
output_Text.grid(column=1, row=2, columnspan=3 , sticky=W)
output_Text["wrap"]="none"
scroll = ttk.Scrollbar(frame, orient=HORIZONTAL, command=output_Text.xview)
scroll.grid(column=1, row=3,  columnspan=3, sticky=(W,E))
output_Text['xscrollcommand'] = scroll.set

sort_button=ttk.Button(frame, text="Sort", command=sortInfo).grid(column=2, row=4, sticky=(W,E))




status_label=ttk.Label(root, textvariable=status, relief=SUNKEN, anchor=W)
status_label.grid(column=0, row=1, sticky=(W,E))
root.tk.call('tk', 'windowingsystem')






	
#the menu
root.option_add('*tearOff', FALSE)
menubar=Menu(root)
root["menu"]=menubar
menu_file=Menu(menubar)
menu_edit=Menu(menubar)
menu_help=Menu(menubar)
menubar.add_cascade(menu=menu_file, label="File")
menubar.add_cascade(menu=menu_edit, label="Edit")
menubar.add_cascade(menu=menu_help, label="Help")
menu_file.add_command(label="Open", command=openFile)
menu_file.add_command(label="Save", command=saveFile)
menu_edit.add_command(label="Copy contents", command =copyContent)
menu_edit.add_command(label="Clear", command=clearContent)
menu_help.add_command(label="Help", command=helpUser)	
	
	
	

root.mainloop()