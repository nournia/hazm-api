
from setuptools import setup

setup(name='hazm-api',
	version='0.4',
	description='Hazm API App',
	author='Alireza Nourian',
	author_email='az.nourian@gmail.com',
	url='http://www.sobhe.ir/hazm/',
	install_requires=[
		'Flask==0.10.1',
		'hazm==0.4',
	]
)
