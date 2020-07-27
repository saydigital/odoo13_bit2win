odoo.define('ifs_dental_product.subscription', function (require) {
	'use strict';
	var core = require('web.core');
	var ajax = require('web.ajax');
	var qweb = core.qweb;
	ajax.loadXML('/anonymous_ticket_comment/static/src/xml/portal_chatter.xml', qweb);
});