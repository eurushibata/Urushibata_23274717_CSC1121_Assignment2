sap.ui.define(["./BaseController", "sap/m/MessageBox"], function (BaseController, MessageBox) {
	"use strict";

	return BaseController.extend("dcu.ca2.controller.Main", {
		sayHello: function () {
			MessageBox.show("Hello World!");
		},

		onSearchPress: async function (oEvent) {
			const start = Date.now();
			const query = this.byId("search_text").getValue();
			const algo = this.byId("search_algorithm").getSelectedKey();

			const url = `/search/${algo}/${query}`;
			const response = await fetch(url);
			if (!response.ok) {
				MessageBox.error("Error: " + response.statusText);
				return;
			}
			const results = await response.json();

			// check if any value has score > 0
			const relevant_docs = results.filter((r) => {
				const key = Object.keys(r)[0];
				return r[key] > 0;
			});

			const end = Date.now();
			this.getModel().setProperty("/total", relevant_docs.length);
			this.getModel().setProperty("/timeSpent", (end - start)/1000 + " seconds");
			
		}
	});
});
