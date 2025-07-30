# Copyright (c) 2025, Rafay and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def before_save(self):
		full_name = f"{self.first_name} {self.last_name or ""}"
		self.full_name = full_name.strip()
		
