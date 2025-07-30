import frappe
import random

def execute():
    ats = frappe.get_all("Airplane Ticket", pluck="name")

    for at in ats:
        doc = frappe.get_doc("Airplane Ticket", at)

        if not doc.seat:
            seat_number= str(random.randint(1,99))
            seat_letter = random.choice(['A','B','C','D'])
            doc.seat = seat_number + seat_letter

        if doc.docstatus == 1:
            doc.status = "Completed"	