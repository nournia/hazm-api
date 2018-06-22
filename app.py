
from __future__ import unicode_literals
import os, json
from flask import Flask, request, abort
from hazm import *
from azbar import AzBarChars, TextCleaner


application = Flask(__name__)
application.config['PROPAGATE_EXCEPTIONS'] = True

resources = os.environ.get('OPENSHIFT_DATA_DIR', 'resources')

normalizer, cleaner, lemmatizer, tagger, chunker, parser = None, None, None, None, None, None


def get_normalizer():
	global normalizer
	if not normalizer:
		normalizer = Normalizer()
	return normalizer


def get_cleaner():
	global cleaner
	if not cleaner:
		cleaner = TextCleaner(language_model=AzBarChars(os.path.join(resources, 'chars.klm')))
	return cleaner


def get_lemmatizer():
	global lemmatizer
	if not lemmatizer:
		lemmatizer = Lemmatizer()
	return lemmatizer


def get_tagger():
	global tagger
	if not tagger:
		tagger = POSTagger(model=os.path.join(resources, 'postagger.model'))
	return tagger


def get_chunker():
	global chunker
	if not chunker:
		chunker = Chunker(model=os.path.join(resources, 'chunker.model'))
	return chunker


def get_parser():
	global parser
	if not parser:
		parser = DependencyParser(lemmatizer=get_lemmatizer(), tagger=get_tagger(), working_dir=resources)
	return parser


@application.route('/api/normalize', methods=['POST'])
def normalize():
	if 'text' not in request.form:
		abort(400)

	return get_normalizer().normalize(request.form['text'])


@application.route('/api/correct', methods=['POST'])
def correct():
	if 'text' not in request.form:
		abort(400)

	mode = request.form.get('mode', '')

	if mode == 'normalizer':
		return get_normalizer().normalize(request.form['text'])

	if mode == 'cleaner':
		return get_cleaner().clean_text(request.form['text'])

	if mode == 'spellchecker':
		# todo: spellcheck
		return request.form['text']

	return request.form['text']


@application.route('/api/tokenize', methods=['POST'])
def tokenize():
	if 'normalized_text' not in request.form:
		abort(400)

	return json.dumps(map(word_tokenize, sent_tokenize(request.form['normalized_text'])), ensure_ascii=False)


@application.route('/api/lemmatize', methods=['POST'])
def lemmatize():
	if 'tagged_text' in request.form:
		tagged_text = json.loads(request.form['tagged_text'])
		return json.dumps([[get_lemmatizer().lemmatize(word, tag) for word, tag in sentence] for sentence in tagged_text], ensure_ascii=False)

	elif 'tokenized_text' in request.form:
		tokenized_text = json.loads(request.form['tokenized_text'])
		return json.dumps([[get_lemmatizer().lemmatize(word) for word in sentence] for sentence in tokenized_text], ensure_ascii=False)

	else:
		abort(400)


@application.route('/api/tag', methods=['POST'])
def tag():
	if 'tokenized_text' not in request.form:
		abort(400)
	tokenized_text = json.loads(request.form['tokenized_text'])

	return json.dumps(get_tagger().tag_sents(tokenized_text), ensure_ascii=False)


@application.route('/api/chunk', methods=['POST'])
def chunk():
	if 'tagged_text' not in request.form:
		abort(400)
	tagged_text = json.loads(request.form['tagged_text'])
	tagged_text = [map(tuple, sent) for sent in tagged_text]

	return json.dumps(list(map(tree2brackets, get_chunker().parse_sents(tagged_text))), ensure_ascii=False)


@application.route('/api/parse', methods=['POST'])
def parse():
	if 'tagged_text' not in request.form:
		abort(400)
	tagged_text = json.loads(request.form['tagged_text'])

	return json.dumps([dependency_graph.to_conll(10) for dependency_graph in get_parser().parse_tagged_sents(tagged_text)], ensure_ascii=False)


@application.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'origin, x-requested-with, content-type')
	response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
	return response


@application.route('/')
def main():
	return 'Hazm API Server!'


if __name__ == '__main__':
	application.run(debug=True)
