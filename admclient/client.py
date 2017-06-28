from tkinter import *
import tkinter.ttk as ttk
import tkinter.simpledialog as simpledialog
import sys
import http.client
import json
from threading import *

bankToPort = {
		'Banco do Brasil' : [8080, 8081],
		'Caixa' : [8082],
		'Bradesco' : [8083],
		'Santander' : [8084]
}

def close():
	top.destroy()

def connection(port, method):
	con = http.client.HTTPConnection(host="localhost", port=port)
	con.request(method, "/total_amount")
	resp = con.getresponse()
	data = resp.read().decode('utf-8')
	con.close()
	return data

def amountFromJson(data):
	r = json.loads(data)
	return float(r["total_amount"])


class AdmClient():

	def __init__(self, top):
		self.top = top
		self.port = 8080 + self.setActualBranch()
		self.branchAmount = StringVar()
		self.branchAmount.set(str(amountFromJson(connection(self.port, "GET"))))
		self.bankAmount = StringVar()
		self.total = 0
		self.initComboBox()
		self.initLabels()
		self.initButtons()
		self.initTextFields()
		self.top.mainloop()
		
	def setActualBranch(self):
		id = simpledialog.askstring("Branch", "Enter the branch you want to visualize")
		return int(id)	

	def initComboBox(self):
		self.box_value = StringVar()
		self.combo = ttk.Combobox(self.top, state="readonly", textvariable=self.box_value)
		self.combo['values'] = ('Banco do Brasil', 'Caixa', 'Bradesco', 'Santander')
		self.combo.current(0)
		self.combo.grid(row=1, column=2)

	def initLabels(self):
		Label(self.top, text="Branch total Amount").grid(row=0,column=0)
		Label(self.top, text="Bank total Amount").grid(row=1, column=0)

	def initButtons(self):
		Button(self.top, text="Refresh", command = self.atualizeTextBranch).grid(row=0,column=2)
		Button(self.top, text="Calculate", command = self.atualizeTextBank).grid(row=1, column=3)
		
	def initTextFields(self):
		self.textBranch = Entry(self.top, textvariable=self.branchAmount)
		self.textBranch.grid(row=0, column=1)
		self.textBranch.config(state="readonly")
		
		self.textBank = Entry(self.top, textvariable=self.bankAmount)
		self.textBank.grid(row=1, column=1)
		self.textBank.config(state="readonly")

	def atualizeTextBranch(self):
		self.branchAmount.set(str(amountFromJson(connection(self.port, "GET"))))
		self.textBranch.config(state="readonly")


	def addBankAmount(self, port, method):
		self.lock = Lock()
		with self.lock:
			self.total += amountFromJson(connection(port,method))	
	
	def atualizeTextBank(self):
		ports = bankToPort[self.combo.get()]
		self.total = 0

		ts = []
		for p in ports:
			ts.append(Thread(target=self.addBankAmount(p, "GET")))

		for t in ts:
			t.start()

		for t in ts:
			t.join()					


		self.bankAmount.set(str(self.total))

top = Tk()
client = AdmClient(top)
