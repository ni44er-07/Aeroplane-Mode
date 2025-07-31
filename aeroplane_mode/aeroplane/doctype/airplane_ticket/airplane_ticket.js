frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        // Add a custom button to assign Gate Number
      frappe.call({
    method: 'aeroplane_mode.aeroplane.doctype.airplane_ticket.airplane_ticket.assign_gate',
    args: {
        doc: frm.doc
    },
    callback: function (r) {
        if (!r.exc) {
            frm.reload_doc();
            frappe.show_alert({
                message: __('Gate {0} has been assigned', [r.message.gate_number]),
                indicator: 'green'
            }, 3);
        }
    }
});

        // Add a custom button to assign Seat Number
        frm.add_custom_button(__('Assign Seat'), function () {
            let dialog = new frappe.ui.Dialog({
                title: __('Assign Seat Number'),
                fields: [
                    {
                        label: __('Seat Number'),
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1,
                        description: __('Please enter the seat number'),
                        default: frm.doc.seat || '' // Pre-fill with existing seat if available
                    }
                ],
                primary_action_label: __('Assign'),
                primary_action(values) {
                    // Set the seat number in the form
                    frm.set_value('seat', values.seat_number);
                    frappe.show_alert({
                        message: __('Seat {0} has been assigned', [values.seat_number]),
                        indicator: 'green'
                    }, 3);
                    dialog.hide();
                }
            });

            dialog.show();
        });
    }
});
