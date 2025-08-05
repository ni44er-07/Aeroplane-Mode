# shop_lead.py
import frappe

def get_context(context):
    # Get the query param from the request
    shop_name = frappe.form_dict.get("shop_name")

    # Pass it to the context so Jinja can use it
    if shop_name:
        context.shop_name = shop_name
