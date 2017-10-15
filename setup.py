
from setuptools import setup

setup(name='hazm-api',
	version='0.5',
	description='Hazm API App',
	author='Alireza Nourian',
	author_email='az.nourian@gmail.com',
	url='http://www.sobhe.ir/hazm/',
	install_requires=[
		'Flask==0.12.2',
		'hazm==0.5.2',
	]
)
