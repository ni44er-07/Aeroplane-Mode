frappe.ready(function() {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const shopName = urlParams.get('shop_name');

    // If shop_name exists in URL, set it in the form
    if (shopName) {
        const shopField = $('[data-fieldname="shop_name"] input');

        if (shopField.length) {
            shopField.val(shopName);
            shopField.prop('readonly', true); // Make read-only
        }
    }
});
