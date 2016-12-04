from flask import Flask, jsonify, render_template, request
import pickle
from os.path import expanduser
app = Flask(__name__)

word_frequencies = pickle.load(open('word_frequencies.pkl'))
conditional_word_frequencies = pickle.load(open('conditional_word_frequencies.pkl'))
first_word_frequencies = pickle.load(open('first_word_frequencies.pkl'))
capitalised_words = pickle.load(open('capitalised_words.pkl'))
text_filename = expanduser("~") + '/Documents/roger.txt'

@app.route('/_readfile')
def readfile():
    try:
        with open(text_filename,'r') as text_file:
            text = text_file.read()
    except:
        print 'Exception while reading file.'
    return jsonify(result=text)

@app.route('/_savefile')
def savefile():
    text = request.args.get('text')
    print type(text)
    print text
    res = 'Not saved'
    try:
        with open(text_filename,'w') as text_file:
            text_file.write(text);
            res = 'OK'
    except Exception, e:
        res = 'Exception raised while saving file'
        print e.args
    return jsonify(result=res)

@app.route('/_suggest')
def suggestions():
    prev_word = request.args.get('prev_word', 0, type=str)
    current_letters = request.args.get('current_letters', 0, type=str)
    n_suggestions = request.args.get('n_suggestions', 0, type=int)

    suggestions = []

    if len(prev_word)==0:
        for c in first_word_frequencies.most_common():
            if c[0].startswith(current_letters) and c[0] not in suggestions:
                    suggestions.append(c[0])
            if len(suggestions)==n_suggestions:
                break
    else:
        if prev_word and len(prev_word)>0:
            common = conditional_word_frequencies[prev_word].most_common()
            for c in common:
                if c[0].startswith(current_letters) and c[0] not in suggestions:
                    suggestions.append(c[0])
                if len(suggestions)==n_suggestions:
                    break

    if len(suggestions)<n_suggestions:
        for c in word_frequencies.most_common():
            if c[0].startswith(current_letters) and c[0] not in suggestions:
                    suggestions.append(c[0])
            if len(suggestions)==n_suggestions:
                break

    #if len(prev_word)==0:
    #    suggestions = [s.capitalize() for s in suggestions]

    suggestions = [s.capitalize() if s in capitalised_words else s for s in suggestions]

    if len(suggestions)<n_suggestions:
        suggestions.extend(['']*(n_suggestions-len(suggestions)))



    return jsonify(result=suggestions)

@app.route('/')
def index():
    return render_template('index.html')
