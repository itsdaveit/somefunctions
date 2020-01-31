# -*- coding: utf-8 -*-
# Copyright (c) 2020, itsdave GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import file_manager
import csv
import re
from frappe.model.document import Document
from pprint import pprint

class SomeFunctions(Document):

	def create_customer_accounts(self):
		log =[]
		with open(frappe.utils.file_manager.get_file_path(self.customer_accounts_csv)) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')
			cff = 0
			cfe = 0
			for row in csv_reader:
				cff = cff + 1

				regex = re.compile('^\d{5}$')
				if None not in (regex.match(row[0]), regex.match(row[2])):
					#log.append(row[2] + " matcht")
					#log.append(re.match(r'^\d*$', row[0]))
					#log.append(re.match(r'^\d*$', row[2]))
					#log.append(re.match(r'\d*', row[0]))
					#log.append(re.match(r'\d*', row[2]))
					try:
						customer = frappe.get_doc("Customer", "Cust-"+ row[0])
						cfe = cfe + 1
						if not customer.accounts:
						
							acc = frappe.get_doc({
													"doctype": "Account",
													"company": self.company,
													"parent_account": self.account,
													"account_type": self.account_type,
													"account_name": customer.customer_name,
													"account_number": row[2]
													}).insert()
							customer.append("accounts", {
														"company": acc.company,
														"account": acc.name
														})
							customer.save()



					except Exception as e:
						print(e.args[0])
						log.append(e.args)
			logtext = ""
			for line in log:
				logtext = logtext + str(line) + "<br>"
			self.log = logtext
						
					
		print("stats: cff: " + str(cff) + " cfe:  " + str(cfe))

	
	
	def dryrun(self):
		log =[]
		with open(frappe.utils.file_manager.get_file_path(self.suppliers_csv)) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')
			cff = 0 #lines processed
			cfe = 0 #existing suppliers
			list_cfe = []
			cfn = 0 #new suppliers
			list_cfn = []
			list_all = []
			accounts = []
			for row in csv_reader:
				list_all.append({"name": row[0], "account": row[1]})
				cff += 1
				accounts.append(int(row[1]))
				try:
					supplier_list = frappe.get_list("Supplier", filters={"supplier_name": row[0]} )
					if supplier_list:
						if len(supplier_list) == 1:
							cfe += 1
							print("found " + row[0])
							log.append("found " + row[0])
							list_cfe.append({"name": row[0], "account": row[1]})
						else:
							print("error, supplier not unique " + row[0])
							log.append("error, found <> 1 suppliers " + row[0])
					else:
						cfn += 1
						print("new supplier " + row[0])
						log.append("new supplier " + row[0])
						list_cfn.append({"name": row[0], "account": row[1]})
				except Exception as e:
					print(e.args[0])
					log.append(e.args)

			for supplier in list_cfn:
				supplier_doc = frappe.get_doc({
						"doctype": "Supplier",
						"supplier_name": supplier["name"],
						"supplier_group": self.supplier_group,
						"supplier_type": "Company"
				})
				supplier_doc.insert()
			
			supplier_list_all = frappe.get_list("Supplier", fields=["supplier_name", "name"] )
			print("------")
			pprint(supplier_list_all)
			for s in supplier_list_all:
				for e in list_all:
					if s["supplier_name"] == e["name"]:
						log.append("gefunden: " + e["name"] +" " + s["name"])
						supp_doc = frappe.get_doc("Supplier", s["name"])
						supp_doc.supplier_type = "Company"
						if supp_doc.accounts:
							pass #log.append("has account")
						else:
							log.append("account missing")
							try:
								sac = frappe.get_doc({
														"doctype": "Account",
														"company": self.company,
														"parent_account": self.supplier_account,
														"account_type": self.supplier_account_type,
														"account_name": supp_doc.supplier_name,
														"account_number": e["account"]
														}).insert()
							except Exception as e:
								pass
							supp_doc.append("accounts", {
														"company": sac.company,
														"account": sac.name
														})
							supp_doc.save()
			no_acc = 0
			for s in supplier_list_all:
				supp_doc = frappe.get_doc("Supplier", s["name"])
				if not supp_doc.accounts:
					no_acc += 1
					supp_doc.supplier_type = "Company"
					print(s["name"] + " has still no account")
					next_account = max(accounts) + 1
					try:
						sac = frappe.get_doc({
													"doctype": "Account",
													"company": self.company,
													"parent_account": self.supplier_account,
													"account_type": self.supplier_account_type,
													"account_name": supp_doc.supplier_name,
													"account_number": next_account
													}).insert()
						accounts.append(next_account)
					except Exception as e:
						pass
					supp_doc.append("accounts", {
												"company": sac.company,
												"account": sac.name
												})
					supp_doc.save()






						
						
			

			






			log.append(str(cff) + " Lines Proccesed")
			log.append(str(cfn) + " new suppliers")
			log.append(str(cfe) + " existing suppliers")

			logtext = ""
			for line in log:
				logtext = logtext + str(line) + "<br>"
			self.supplier_log = logtext
						
					
		print("stats: cff: " + str(cff) + " cfe:  " + str(cfe))
		#print(list_cfe)
		#print(list_cfn)
		print("max account: " + str(max(accounts)))
		print("no acc: " + str(no_acc))
	pass

