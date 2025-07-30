import frappe
from frappe import _
import random
from frappe.model.document import Document

class AirplaneTicket(Document):
    def before_save(self):
        total_amount = 0
        for i in self.add_ons:
            total_amount += i.amount
        self.total_amount = total_amount + self.flight_price

    def before_validate(self):
        seat_number = str(random.randint(1, 99))
        seat_letter = random.choice(['A', 'B', 'C', 'D'])
        self.seat = seat_number + seat_letter
        
        
        gate_num= str(random.randint(1,10))
        gate_letter = random.choice(('A','B','C'))
        self.gate_number = gate_num + gate_letter
        print(gate_num)
           
    def validate(self):
        # ✅ 1. Enforce unique add-ons
        unique_add_ons = []
        seen_add_ons = set()
        for i in self.add_ons:
            if i.item not in seen_add_ons:
                seen_add_ons.add(i.item)
                unique_add_ons.append(i)
        self.add_ons = unique_add_ons


        # Get airplane linked to this flight
        airplane = frappe.db.get_value("Flights", self.flight, "airplane")

        # Get airplane capacity
        capacity = frappe.db.get_value("Airplane", airplane, "capacity")

        # if not capacity:
        #     frappe.throw("Airplane full")
        #     return

        # Count tickets already created for this flight
        booked_count = frappe.db.count("Airplane Ticket", {
            "flight": self.flight,
            "name": ["!=", self.name]
        })

        # Check if booked count >= capacity
        if booked_count >= capacity:
            frappe.throw(_("Cannot create ticket. Airplane with capacity {0} is fully booked.").format(capacity))

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw(_("You can not submit this Airplane Ticket unless the status is 'Boarded'"))

    def on_submit(self):
        self.status = "Completed"
    def before_insert(self):
            if self.flight:
                flight = frappe.get_doc("Flight", self.flight)
                self.flight_price = flight.price

