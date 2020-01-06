# -*- coding: utf-8 -*-
# Copyright (c) 2020, itsdave GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import file_manager
import csv
import re
from frappe.model.document import Document

class SomeFunctions(Document):

	def create_customer_accounts(self):
		log =[]
		with open(frappe.utils.file_manager.get_file_path(self.customer_accounts_csv)) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')
			cff = 0
			cfe = 0
			for row in csv_reader:
				cff = cff + 1
				log.append(str(row) + "<br>")

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
	pass

