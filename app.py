from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from SlackConnector import SlackConnector
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s//db' % os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
slack = SlackConnector()

@app.route("/")
def main():
	context = {
		"tags":get_tags(),
		#"messages":slack.get_messages()
	}

	return render_template('main.html', context=context)

"""
Models
"""
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), unique=True)

    @property
    def serialise(self):
		obj = {
			'id': self.id,
			'value': self.value
		}
		return obj 

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<Tag %r>' % self.value

"""
API 
"""

@app.route("/api/v1/get_tags", methods=['GET'])
def get_tags():
	return jsonify(tags=[i.serialise for i in Tag.query.all()])

@app.route("/api/v1/get_channels", methods=['GET'])
def get_channels():
	channels = slack.get_channels()
	print(channels)

	return jsonify(channels=channels.body['channels'])

@app.route("/api/v1/get_filtered_messages", methods=['GET'])
def get_filtered_messages(channels=None, tags=None):
	messages = slack.get_messages()
	return jsonify(messages=messages)

# @app.route("/api/v1/add_tags/<tags>", methods=['POST'])
# def add_tags(tags):
# 	for tag in tags:
# 		tag = Tag(tag)
# 		db.session.add(tag)
# 	db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)