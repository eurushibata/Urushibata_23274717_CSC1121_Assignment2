sap.ui.define(function () {
	"use strict";

	return {
		name: "QUnit test suite for the UI5 Application: dcu.ca2",
		defaults: {
			page: "ui5://test-resources/dcu/ca2/Test.qunit.html?testsuite={suite}&test={name}",
			qunit: {
				version: 2
			},
			sinon: {
				version: 1
			},
			ui5: {
				language: "EN",
				theme: "sap_horizon"
			},
			coverage: {
				only: "dcu/ca2/",
				never: "test-resources/dcu/ca2/"
			},
			loader: {
				paths: {
					"dcu/ca2": "../"
				}
			}
		},
		tests: {
			"unit/unitTests": {
				title: "Unit tests for dcu.ca2"
			},
			"integration/opaTests": {
				title: "Integration tests for dcu.ca2"
			}
		}
	};
});
