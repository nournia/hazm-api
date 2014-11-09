from setuptools import setup

setup(name='hazm-api',
	version='0.3',
	description='Hazm API App',
	author='Alireza Nourian',
	author_email='az.nourian@gmail.com',
	url='http://www.sobhe.ir/hazm/',
	install_requires=[
		'Flask==0.10.1',
		'Jinja2==2.7.1',
		'Werkzeug==0.9.4',
		'gunicorn==18.0',
		'hazm==0.3',
	]
)
