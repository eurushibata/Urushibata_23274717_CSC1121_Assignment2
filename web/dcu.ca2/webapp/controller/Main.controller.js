sap.ui.define(["./BaseController", "sap/m/MessageBox"], function (BaseController, MessageBox) {
	"use strict";

	return BaseController.extend("dcu.ca2.controller.Main", {
		sayHello: function () {
			MessageBox.show("Hello World!");
		}
	});
});
