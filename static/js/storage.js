(function (exports) {

	'use strict';

	var STORAGE_KEY = 'slack-aggregator-';

	exports.storage = {
		fetch: function (storeName) {
			return JSON.parse(localStorage.getItem(STORAGE_KEY+storeName) || '[]');
		},
		save: function (storeName, tags) {
			localStorage.setItem(STORAGE_KEY+storeName, JSON.stringify(tags));
		}
	};

})(window);