(function (exports) {

	'use strict';

	var STORAGE_KEY = 'slack-aggregator';

	exports.tagsStorage = {
		fetch: function () {
			return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
		},
		save: function (tags) {
			localStorage.setItem(STORAGE_KEY, JSON.stringify(tags));
		}
	};

})(window);