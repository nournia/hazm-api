
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from hazm import sent_tokenize, word_tokenize, Normalizer, Lemmatizer, POSTagger, DependencyParser

resources = os.environ['OPENSHIFT_DATA_DIR']

app = Flask(__name__)
parser = DependencyParser(tagger=POSTagger(path_to_model=os.path.join(resources, 'persian.tagger'), path_to_jar=os.path.join(resources, 'stanford-postagger.jar')), working_dir=resources)


@app.route('/api/parse', methods = ['POST'])
def parse():
	if not 'sentence' in request.form:
		abort(400)

	return parser.parse(word_tokenize(request.form['sentence'])).to_conll(10)


@app.route('/')
def main():
	return 'Hazm API Server!'


if __name__ == '__main__':
	app.run(debug=True)
