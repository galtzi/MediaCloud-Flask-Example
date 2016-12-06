import ConfigParser, logging, datetime, os

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    fmonth = int(request.form['fmonth'])
    fday = int(request.form['fday'])
    fyear = int(request.form['fyear'])
    tmonth = int(request.form['fmonth'])
    tday = int(request.form['tday'])
    tyear = int(request.form['tyear'])
    fromdate = datetime.date(fyear, fmonth, fday)
    todate = datetime.date(tyear, tmonth, tday)

    results = mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query(fromdate,
                                            todate),
                     'media_sets_id:1'])

    splitanalysis = mc.sentenceCount(keywords,
                                    solr_filter=[mc.publish_date_query(fromdate,
                                                                       todate),
                                                 'media_sets_id:1'], split=1)


    return render_template("search-results.html",
        keywords=keywords, sentenceCount=results['count'], splitanalysis=splitanalysis) # splitanalysis['split']



if __name__ == "__main__":
    app.debug = True
    app.run()

#
# datetime.date( 2015, 1, 1),
# datetime.date( now.year, now.month, now.day) ),