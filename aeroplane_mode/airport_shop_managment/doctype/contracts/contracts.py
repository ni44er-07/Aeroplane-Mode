import frappe
from frappe.model.document import Document


class Contracts(Document):
    def validate(self):
        self.check_for_conflicting_contracts()
        self.calculate_total_rent()

    def check_for_conflicting_contracts(self):
        overlapping_contracts = frappe.get_all(
            "Contracts",
            filters={
                "shop": self.shop,  
                "name": ["!=", self.name],
                "docstatus": ["!=", 2],
                "contract_start_date": ["<=", self.contract_end_date],
                "contract_end_date": [">=", self.contract_start_date],
            },
            limit=1
        )

        if overlapping_contracts:
            frappe.throw(
                ("This shop already has a conflicting contract during the selected period."),
                title="Overlapping Contract"
            )

    def on_submit(self):
        frappe.db.set_value("Shop", self.shop, "is_occupied", 1)

    def on_cancel(self):
        frappe.db.set_value("Shop", self.shop, "is_occupied", 0)
    def calculate_total_rent(self):
        if not self.rent or not self.payment_frequency:
            self.total_rent = 0
            return

        frequency_map = {
            "Monthly": 1,
            "Quarterly": 3,
            "Semi-Annual": 6,
            "Annual": 12
        }

        multiplier = frequency_map.get(self.payment_frequency, 1)
       

    def send_rent_due_reminders():
        """Send monthly rent due reminders to tenants via email"""
        contracts = frappe.get_all(
            "Contracts",
            filters={"status": "Active"},
            fields=["name", "tenant", "tenant_email", "total_outstanding_rent"]
        )

        for c in contracts:
            if not c.tenant_email:
                continue  # Skip if no email

            subject = f"Rent Payment Reminder - Contract {c.name}"
            message = f"""
    Dear {c.tenant}, 

    This is a friendly reminder that your rent is due for this month.

    **Contract ID:** {c.name}  
    **Outstanding Rent:** {frappe.utils.fmt_money(c.total_outstanding_rent)}

    Please make the payment at your earliest convenience to avoid any late fees.

    Thank you,  
    **Accounts Department**  
    Airport Shops Management
            """

            frappe.sendmail(
                recipients=[c.tenant_email],
                subject=subject,
                message=message
            )

        frappe.logger().info("Monthly rent reminders sent.")
