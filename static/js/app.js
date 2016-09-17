Vue.config.debug = true
Vue.config.delimiters = ['[[', ']]']
var vm = new Vue({
	el: '#app',
	data: {
		// tags checkbox
		tags: [],
		activeTags: storage.fetch("activeTags") || [],

		// channels checkbox
		channels: [],
		activeChannels: storage.fetch("activeChannels") || [],		

		// messages
		messages: [],
		maxMessages: 50
	},

	ready: function () {
		this.updateChannels();
		this.updateTags();
		this.updateFilteredMessages(this.activeChannels, this.activeTags);
	},

	watch: {
		activeTags: {
			handler: function (tags) {
				storage.save("activeTags", tags)
				this.updateFilteredMessages(this.activeChannels, this.activeTags);
			},
			deep: true
		},
		activeChannels: {
			handler: function (channels) {
				storage.save("activeChannels", channels)
				this.updateFilteredMessages(this.activeChannels, this.activeTags);
			},
			deep: true
		}
	},

	methods: {
		updateChannels: function () {
	    	console.log("get channels...")
			this.$http.get('/api/v1/get_channels').then((response) => {
				var channels = response.body.channels;
				this.$set('channels',channels);
			}, (response) => {
				console.log("Failed to get channels")
			});
	    },
		updateTags: function () {
	    	console.log("get tags...")
			this.$http.get('/api/v1/get_tags').then((response) => {
				var tags = response.body.tags;
				this.$set('tags',tags);
			}, (response) => {
				console.log("Failed to get tags")
			});
	    },
	    updateFilteredMessages: function (channels, tags) {
	    	console.log("get getFilteredMessages...")
	    	if(channels && tags){
				this.$http.get('/api/v1/get_filtered_messages?channels='+channels.join("+")+"&tags="+tags.join("+")).then((response) => {
					console.log("Got messages")
					var messages = response.body.messages;
					console.log(response.body)
					this.$set('messages',messages);
				}, (response) => {
					console.log("Failed to get messages")
				});
	    	} else {
	    		console.log("Please select one or more channel and tag")
	    	}
	  		//{
			// 	xhr: {
			// 		onprogress: function(event) {
			// 			console.log("progress")
			// 		}
			//	}
			//}
	    }
	}
});
