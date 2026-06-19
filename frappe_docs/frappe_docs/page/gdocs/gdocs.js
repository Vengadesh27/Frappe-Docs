frappe.pages['gdocs'].on_page_load = function (wrapper) {
	// Hide Frappe's default page chrome
	$(wrapper).css({ padding: 0, height: '100%', overflow: 'hidden' });

	// Create full-height container for Vue
	const container = document.createElement('div');
	container.id = 'gdocs-app';
	container.style.cssText = 'height:100%;width:100%;overflow:hidden;position:relative;display:flex;flex-direction:column;';
	wrapper.innerHTML = '';
	wrapper.appendChild(container);

	// Load the Vue bundle
	frappe.require('/assets/frappe_docs/js/gdocs.js');
};

frappe.pages['gdocs'].on_page_show = function () {
	// ensure Frappe navbar is visible
	$('.navbar').show();
};
