sap.ui.define([
	"./BaseController", "sap/m/MessageBox", "sap/ui/model/Filter", "sap/ui/model/json/JSONModel"
], function (BaseController, MessageBox, Filter, JSONModel) {
	"use strict";

	return BaseController.extend("dcu.ca2.controller.Main", {
		onInit: async function () {
			// read the dataset

			const dataset = await fetch("/dataset");
			if (!dataset.ok) {
				MessageBox.error("Error: " + dataset.statusText);
				return;
			}
			const data = await dataset.json();

			this.getModel().setProperty("/dataset", data);
		},

		sayHello: function () {
			MessageBox.show("Hello World!");
		},

		onSearchPress: async function (oEvent) {
			const query = this.byId("search_text").getValue();

			if (!query) {
				MessageBox.error("Please enter a search term");
				return;
			}
			oEvent.getSource().setEnabled(false);
			this.getView().byId("countdownText").setVisible(true);
			const start = Date.now();
			const algo = this.byId("search_algorithm").getSelectedKey();

			const url = `/search/${algo}/${query}`;

			const intervalFn = () => {
			};
			let initialStart = 0;
			this.getModel().setProperty("/realtimeCountdown", 0.000);
			const intervalExec = setInterval(() => {
				initialStart = initialStart + 10;
				this.getModel().setProperty("/realtimeCountdown", initialStart/1000);
			}, 1 );
			const response = await fetch(url);
			clearInterval(intervalExec);
			oEvent.getSource().setEnabled(true);
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

			const dataset = this.getModel().getProperty("/dataset");
			const filters = {};
			for (const i in relevant_docs) {
				const key = Object.keys(relevant_docs[i])[0];
				const value = relevant_docs[i][key]
				filters[parseInt(key)] = value;
			}
			const query_results = dataset.filter((images) => {
				if (filters[images.page_id]) {
					images.rankingPos = filters[images.page_id]
					return true;
				}
				return false;
			});

			this.getModel().setProperty("/total", relevant_docs.length);
			this.getModel().setProperty("/ranking", relevant_docs);
			this.getModel().setProperty("/results", query_results);
			this.getModel().setProperty("/timeSpent", (end - start)/1000 + " seconds");
			this.getModel().setProperty("/realtimeCountdown", (end - start)/1000);

		},

		onImagePress: function (oEvent) {
			const url = this.getModel().getProperty(`${oEvent.getSource().getBindingContext().getPath()}/wikipedia_source_url`);
			window.open(url, "_blank");
		}
	});
});
