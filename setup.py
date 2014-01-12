from setuptools import setup

setup(name='hazm-api',
	version='0.2',
	description='OpenShift App',
	author='Alireza Nourian',
	author_email='example@example.com',
	url='http://www.python.org/sigs/distutils-sig/',
	install_requires=[
		'Flask==0.10.1',
		'Jinja2==2.7.1',
		'Werkzeug==0.9.4',
		'gunicorn==18.0',
	],
	dependency_links=[
		'https://github.com/sobhe/hazm/archive/master.zip'
	]
)
