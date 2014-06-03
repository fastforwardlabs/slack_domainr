import os
import json
import urllib

from flask import *

app = Flask(__name__)

def domainr_query(query):
    print "Running query: %s" % query
    BASE_URL = "https://domai.nr/api/json/search?q="
    h = urllib.urlopen(BASE_URL + query)
    results = json.loads(h.read())
    #print results
    return results


@app.route('/', methods=['GET','POST'])
def hello():
    query = request.args.get('text', None)
    results = domainr_query(query)
    available_domains = []
    for result in results['results']:
        if result['availability'] != 'taken':
            if result['path']:
                available_domains.append(result['domain'] + result['path'])
            else:
                available_domains.append(result['domain'])
    return render_template('plain.html', query=query, available_domains=available_domains)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True # DEBUG
    app.run(host='0.0.0.0', port=port)
