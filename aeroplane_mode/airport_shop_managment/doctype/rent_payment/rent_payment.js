frappe.ui.form.on('Rent Payment', {
    validate: function(frm) {
        if (!frm.doc.contract) {
            frappe.throw(__('Contract is required.'));
        }
        if (frm.doc.amount_paid <= 0) {
            frappe.throw(__('Amount Paid must be greater than zero.'));
        }
        if (frm.doc.date_paid > frappe.datetime.get_today()) {
            frappe.throw(__('Date Paid cannot be in the future.'));
        }
    }
});
// Copyright (c) 2025, Rafay and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Rent Payment", {
// 	refresh(frm) {

// 	},
// });
