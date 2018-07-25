# -*- coding: utf-8 -*-
import re
import os
import math
import tkinter.scrolledtext as tkst
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import matplotlib.pyplot as plt

class Calc:
	version = '2.3.1'
	pattern_start = r'^([a-z0-9\+\*/\^(\sroot\s)\(\)\.,-]+)$'
	pattern_result = r'^[-]?[0-9]+(\.[0-9]+)?$'
	pattern1 = r'([-]?[0-9]+(\.[0-9]+)?)([+-])([-]?[0-9]+(\.[0-9]+)?)'
	pattern2 = r'([-]?[0-9]+(\.[0-9]+)?)([\*/])([-]?[0-9]+(\.[0-9]+)?)'
	pattern3 = r'([-]?[0-9]+(\.[0-9]+)?)(root|\^)([-]?[0-9]+(\.[0-9]+)?)'
	pattern4 = r'\(((?![\(\)]).)+\)'
	pattern5 = r'^(f\(x\)|y)=([-]?[0-9]+)x([+-][0-9]+)$'
	accuracy = 6 # Set default accuracy
	autocalc = False
	constants = {'pi':math.pi, 'fi':(1.5**0.5)/2, 'e':math.e}
	history = []
	history_pos = 0
	
	def __init__(self):
		self.set_win = False
		self.read_settings()
		self.start_gui()
		
	def btnClick(self, e=None):
		self.warning['text'] = ""
		command = self.textbox.get().replace(",", ".")
		if len(command) > 1:
			if re.search(self.pattern_start, command):
				self.textarea.delete(1.0, END)
				self.textarea.insert(END, command)
				if len(self.history) >= 10:
					del self.history[0]
				self.history.append(command)
				self.analysis(command)
			else:
				self.warning['text'] = "Użyto niedozwolonych znaków"
		else:
			self.warning['text'] = "Wpisz działanie!"

	def clearText(self):
		self.textbox.delete(0, END)
		self.textarea.delete(1.0, END)		
	
	def clearTextbox(self, e=None):
		self.textbox.delete(0, END)
	
	def showInfo(self):
		messagebox.showinfo("Kalkulator - informacje", "Kalkulator v."+self.version+"\nGrzegorz Babiarz 2017-2018\nGNU General Public License v3.0\nhttps://github.com/Programista3/Algorytmy/tree/master/Python/kalkulator")

	def quit(self):
		self.root.destroy()

	def historyKey(self, e):
		if e.keysym == "Up":
			if self.history_pos < 9:
				self.history_pos += 1
			self.textbox.delete(0, END)
			self.textbox.insert(0, self.history[len(self.history)-self.history_pos-1])
		elif e.keysym == "Down":
			if self.history_pos > 0:
				self.history_pos -= 1
			self.textbox.delete(0, END)
			self.textbox.insert(0, self.history[len(self.history)-self.history_pos-1])

	def autocalculation(self, e):
		if self.autocalc:
			search = re.search(self.pattern5, self.textbox.get())
			if search:
				self.chart.pack(in_=self.bottom, pady=4)
			else:
				self.chart.pack_forget()
				self.btnClick()

	def drawChart(self):
		search = re.search(self.pattern5, self.textbox.get())
		x = [-2, 2]
		y = [int(search.group(2))*i+int(search.group(3)) for i in x]
		plt.gca().set_prop_cycle('color', ['black', 'black', 'red'])
		plt.plot([0, 0], [max(y), min(y)])
		plt.plot(x, [0, 0])
		plt.plot(x, y)
		plt.title(search.group())
		plt.grid(True)
		plt.show()

	def start_gui(self):
		self.root = Tk()
		self.root.geometry('{}x{}'.format(550, 250))
		self.root.title("Kalkulator")
		menu = Menu(self.root)
		options = Menu(menu)
		options.add_command(label="Ustawienia", command=self.settings)
		options.add_command(label="Informacje", command=self.showInfo)
		options.add_command(label="Wyjście", command=self.quit)
		menu.add_cascade(label="Opcje", menu=options)
		self.textbox = ttk.Entry(self.root, width=85)
		self.textbox.bind("<Return>", self.btnClick)
		self.textbox.bind("<Delete>", self.clearTextbox)
		self.textbox.bind("<Up>", self.historyKey)
		self.textbox.bind("<Down>", self.historyKey)
		self.textbox.bind("<KeyRelease>", self.autocalculation)
		self.textbox.pack(pady=10)
		self.textarea = tkst.ScrolledText(self.root, width=62, height=9)
		self.textarea.pack()
		self.warning = ttk.Label(self.root, text="")
		self.warning.pack()
		self.bottom = Frame(self.root)
		self.bottom.pack()
		clear = ttk.Button(self.root, command=self.clearText, text="Wyczyść")
		clear.pack(in_=self.bottom, side=LEFT)
		button = ttk.Button(self.root, command=self.btnClick, text='Oblicz')
		button.pack(in_=self.bottom, side=LEFT, padx=4, pady=4)
		self.chart = ttk.Button(self.root, command=self.drawChart, text='Wykres')
		self.root.config(menu=menu)
		self.root.resizable(0,0)
		self.root.mainloop()

	def calculate(self, command):
		calculation1 = re.search(self.pattern1, command)
		calculation2 = re.search(self.pattern2, command)
		calculation3 = re.search(self.pattern3, command)
		if calculation3:
			if calculation3.group(3) == '^':
				return calculation3.group(), float(calculation3.group(1))**float((calculation3.group(4)))
			elif calculation3.group(3) == 'root':
				if float(calculation3.group(4)) < 0 and float(calculation3.group(1))%2 == 0:
					self.warning['text'] = "Nie można obliczyć pierwiastka stopnia parzystego z liczby ujemnej!"
					return False, False
				else:
					return calculation3.group(), float(calculation3.group(4))**(1/float(calculation3.group(1)))
			else:
				self.warning['text'] = "Błąd: niezindentyfikowane działanie"
				return False, False
		elif calculation2:
			if calculation2.group(3) == '*':
    				return calculation2.group(), float(calculation2.group(1))*float(calculation2.group(4))
			elif calculation2.group(3) == '/':
				if float(calculation2.group(4)) != 0:
					return calculation2.group(), float(calculation2.group(1))/float(calculation2.group(4))
				else:
					self.warning['text'] = "Nie można dzielić przez 0"
					return False, False
			else:
				self.warning['text'] = "Błąd: niezindentyfikowane działanie"
				return False, False
		elif calculation1:
			if calculation1.group(3) == '+':
				return calculation1.group(), float(calculation1.group(1))+float(calculation1.group(4))
			elif calculation1.group(3) == '-':
				return calculation1.group(), float(calculation1.group(1))-float(calculation1.group(4))
			else:
				self.warning['text'] = "Błąd: niezindentyfikowane działanie"
				return False, False
		else:
			if not self.autocalculation:
				self.warning['text'] = "Niepoprawne działanie"
			return False, False	
		
	def analysis(self, command):
		command = command.replace(" ", "")
		for key, val in self.constants.items():
			command = command.replace(key, str(round(val, self.accuracy)))
		calculation = re.search(self.pattern4, command)
		if calculation:
			calculation = calculation.group()
			calculation.replace('(', '').replace(')', '')
			calculation2, result = self.calculate(calculation)
			if calculation2 != False:
				command = command.replace(calculation, str(self.format_result(result)))
				if re.search(self.pattern_result, command) == None:
					self.textarea.insert(END, "="+command)
					self.analysis(command)
				else:
					if not self.autocalc:
						self.textbox.delete()
						self.textbox.insert(0, command)
					self.textarea.insert(END, "="+command)
			else:
				self.textarea.delete(1.0, END)
		else:
			calculation2, result = self.calculate(command)
			if calculation2 != False:
				command = command.replace(calculation2, str(self.format_result(result)))
				if re.search(self.pattern_result, command) == None:
					self.textarea.insert(END, "="+command)
					self.analysis(command)
				else:
					if not self.autocalc:
						self.textbox.delete(0, END)
						self.textbox.insert(0, command)
					self.textarea.insert(END, "="+command)
			else:
				self.textarea.delete(1.0, END)
			
	def read_settings(self):
		if os.path.isfile('config.dat'):
			config = open("config.dat", "r").read()
			ac_pattern = r'accuracy: ([0-9]+)'
			atc_pattern = r'autocalc: ([10]|True|False|true|false)'
			search = re.search(ac_pattern, config)
			if search:
				accuracy = int(search.group(1))
				if accuracy >= 0 and accuracy <= 10:
					self.accuracy = accuracy
			search2 = re.search(atc_pattern, config)
			if search2:
				if search2.group(1) == '1' or search2.group(1) == 'True' or search2.group(1) == 'true':
					self.autocalc = True
			
	def format_result(self, number):
		number = float(number)
		if number.is_integer():
			return int(number)
		else:
			return round(number, self.accuracy)
	
	def close(self):
		self.window.destroy()
		self.set_win = False

	def save_settings(self):
		ac_pattern = r'accuracy: ([0-9]+)'
		atc_pattern = r'autocalc: ([10]|True|False|true|false)'
		config_text = self.configText.get(1.0, END).strip()
		err = None
		search = re.search(ac_pattern, config_text)
		search2 = re.search(atc_pattern, config_text)
		if search:
			accuracy = float(search.group(1))
			if accuracy >= 0 and accuracy <= 10:
				self.accuracy = accuracy
			else:
				err = "Dokładność nie może być większa niż 10"
		if search2:
			if search2.group(1) == '1' or search2.group(1) == 'true' or search2.group(1) == 'True':
				self.autocalc = True
			else:
				self.autocalc = False
		if not err:
				config = open("config.dat", "w")
				config.write(config_text)
				messagebox.showinfo("Zapisywanie ustawień", "Zmiany zostały zapisane")
				config.close()
		else:
			messagebox.showinfo("Błąd", err)

	def settings(self):
		if not self.set_win:
			self.set_win = True
			self.window = Toplevel()
			self.window.geometry("400x300")
			self.window.wm_title("Zmień ustawienia")
			self.configText = tkst.ScrolledText(self.window, width=50, height=16)
			self.configText.pack()
			if os.path.isfile("config.dat"):
				config = open("config.dat", "r")
				self.configText.insert(END, config.read())
			else:
				config = open("config.dat", "w+")
				text = "accuracy: "+str(self.accuracy)
				config.write(text)
				self.configText.insert(END, text)
			config.close()
			frame = ttk.Frame(self.window)
			frame.pack(pady=6)
			btn = ttk.Button(self.window, text="Zapisz", command=self.save_settings)
			btn.pack(in_=frame, side=LEFT)
			exit = ttk.Button(self.window, text="Zamknij", command=self.close)
			exit.pack(in_=frame)
			self.window.resizable(0,0)
			self.window.protocol("WM_DELETE_WINDOW", self.close)
			
kalkulator = Calc()