# Import statements necessary
from flask import Flask, render_template
from flask_script import Manager
import requests
import json

# Set up application
app = Flask(__name__)

manager = Manager(app)

# Routes

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route('/user/<yourname>')
def hello_name(yourname):
    return '<h1>Hello {}</h1>'.format(yourname)

@app.route('/showvalues/<name>')
def basic_values_list(name):
    lst = ["hello","goodbye","tomorrow","many","words","jabberwocky"]
    if len(name) > 3:
        longname = name
        shortname = None
    else:
        longname = None
        shortname = name
    return render_template('values.html',word_list=lst,long_name=longname,short_name=shortname)

@app.route('/word/<new_word>')
def find_rhyme(new_word):
    baseurl = 'https://api.datamuse.com/words'
    param_dic = {}
    param_dic['rel_rhy'] = new_word
    resp = requests.get(baseurl, params=param_dic)
    python_obj = json.loads(resp.text)
    rhyme = "None"
    if len(python_obj) > 0:
        rhyme = python_obj[0]["word"]
    return '<h1>{}</h1>'.format(rhyme)

## PART 1: Add another route /word/<new_word> as the instructions describe.


## PART 2: Edit the following route so that the photo_tags.html template will render
@app.route('/flickrphotos/<tag>/<num>')
def photo_titles(tag, num):
    # HINT: Trying out the flickr accessing code in another file and seeing what data you get will help debug what you need to add and send to the template!
    # HINT 2: This is almost all the same kind of nested data investigation you've done before!
    FLICKR_KEY = "" # TODO: fill in a flickr key
    baseurl = 'https://api.flickr.com/services/rest/'
    params = {}
    params['api_key'] = 'a28faf5c84205b17cac78e3e4ebe9b4d'
    params['method'] = 'flickr.photos.search'
    params['format'] = 'json'
    params['tag_mode'] = 'all'
    params['per_page'] = num
    params['tags'] = tag
    response_obj = requests.get(baseurl, params=params)
    trimmed_text = response_obj.text[14:-1]
    flickr_data = json.loads(trimmed_text)
    photo_data = flickr_data['photos']['photo']
    titles = []
    for data in photo_data:
        titles.append(data['title'])
        #print(titles)

    # print(flickr_data)
    # TODO: Add some code here that processes flickr_data in some way to get what you nested
    # TODO: Edit the invocation to render_template to send the data you need
    return render_template('photo_info.html', num = num, photo_titles = titles)




if __name__ == '__main__':
    manager.run() # Runs the flask server in a special way that makes it nice to debug
