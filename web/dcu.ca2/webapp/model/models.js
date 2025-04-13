sap.ui.define(["sap/ui/model/json/JSONModel", "sap/ui/model/BindingMode", "sap/ui/Device"], function (JSONModel, BindingMode, Device) {
	"use strict";

	return {
		createDeviceModel: function () {
			const oModel = new JSONModel(Device);
			oModel.setDefaultBindingMode(BindingMode.OneWay);
			return oModel;
		},

		createLocalModel: function () {
			const oModel = new JSONModel({
				total: 0,
				timeSpent: 0,
				busy: false,
				results: []
			});
			return oModel;
		}
	};
});
