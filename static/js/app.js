Vue.config.debug = true
Vue.config.delimiters = ['[[', ']]']
var vm = new Vue({
	el: '#app',
	data: {
		channels: [],
		tags: [],
		activeTags: [],
		messages: []
	},

	ready: function () {
		this.getChannels();
		this.getTags();
		this.getLastSelected();
		this.getFilteredMessages();
	},

	methods: {
		getChannels: function () {
	    	console.log("get channels...")
			this.$http.get('/api/v1/get_channels').then((response) => {
				var channels = response.body.channels;
				this.$set('channels',channels);
			}, (response) => {
				console.log("Failed to get channels")
			});
	    },
		getTags: function () {
	    	console.log("get tags...")
			this.$http.get('/api/v1/get_tags').then((response) => {
				var tags = response.body.tags;
				this.$set('tags',tags);
			}, (response) => {
				console.log("Failed to get tags")
			});
	    },
	    getLastSelected: function () {

	    },
	    getFilteredMessages: function (channels, tags) {
	    	console.log("get getFilteredMessages...")
	    	if(channels && tags){	
				this.$http.get('/api/v1/get_filtered_messages?'+channels+"&"+tags).then((response) => {
					var messages = response.body.messages;
					this.$set('messages',messages);
				}, (response) => {
					console.log("Failed to get messages")
				});
	    	} else {
	    		console.log("Please select one or more channel and tag")
	    	}
	    }

	}
});
