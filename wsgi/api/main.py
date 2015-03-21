
from __future__ import unicode_literals
import os, json
from flask import Flask, request, abort
from hazm import *

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

resources = os.environ['OPENSHIFT_DATA_DIR']

normalizer = Normalizer()
lemmatizer = Lemmatizer()
tagger = StanfordPOSTagger(path_to_model=os.path.join(resources, 'persian.tagger'), path_to_jar=os.path.join(resources, 'stanford-postagger.jar'))
chunker = Chunker(model=os.path.join(resources, 'chunker.model'))
parser = DependencyParser(lemmatizer=lemmatizer, tagger=tagger, working_dir=resources)


@app.route('/api/normalize', methods=['POST'])
def normalize():
	if 'text' not in request.form:
		abort(400)

	return normalizer.normalize(request.form['text'])


@app.route('/api/tokenize', methods=['POST'])
def tokenize():
	if 'normalized_text' not in request.form:
		abort(400)

	return json.dumps(map(word_tokenize, sent_tokenize(request.form['normalized_text'])), ensure_ascii=False)


@app.route('/api/tag', methods=['POST'])
def tag():
	if 'tokenized_text' not in request.form:
		abort(400)
	tokenized_text = json.loads(request.form['tokenized_text'])

	return json.dumps(tagger.tag_sents(tokenized_text), ensure_ascii=False)


@app.route('/api/lemmatize', methods=['POST'])
def lemmatize():
	if 'tagged_text' in request.form:
		tagged_text = json.loads(request.form['tagged_text'])
		return json.dumps([[lemmatizer.lemmatize(word, tag) for word, tag in sentence] for sentence in tagged_text], ensure_ascii=False)

	if 'tokenized_text' in request.form:
		tokenized_text = json.loads(request.form['tokenized_text'])
		return json.dumps([[lemmatizer.lemmatize(word) for word in sentence] for sentence in tokenized_text], ensure_ascii=False)

	abort(400)


@app.route('/api/chunk', methods=['POST'])
def chunk():
	if 'tagged_text' not in request.form:
		abort(400)
	tagged_text = json.loads(request.form['tagged_text'])

	return json.dumps(list(map(tree2brackets, chunker.parse_sents(tagged_text))), ensure_ascii=False)


@app.route('/api/parse', methods=['POST'])
def parse():
	if 'tagged_text' not in request.form:
		abort(400)
	tagged_text = json.loads(request.form['tagged_text'])

	return json.dumps([dependency_graph.to_conll(10) for dependency_graph in parser.tagged_parse_sents(tagged_text)], ensure_ascii=False)


@app.route('/')
def main():
	return 'Hazm API Server!'


if __name__ == '__main__':
	app.run(debug=True)
