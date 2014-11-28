from flask import Flask
import pyble


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# Requests (discover nodes and list enabled nodes)
#

# The gateway will perform passive scan for nodes. 
# Used scan parameters are decided by the gateway  
@app.route("/gap/<nodes>")
def discover():
	return "discover"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
