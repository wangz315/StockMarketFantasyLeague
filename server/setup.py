from distutils.core import Command
from setuptools import setup, find_packages
import sys


class RunServerCommand(Command):
    description = 'Runs an instance of the StockFantasyLeague Server'
    user_options = []
    
    def initialize_options(self):
        pass
        
    def finalize_options(self):
        pass
        
    def run(self):
        import flask_server

        flask_server.run()
        
class RunAcceptanceTests(Command):
    description = 'Runs acceptance tests. Make sure a local instance of the server is active.'
    user_options = []
    
    def initialize_options(self):
        pass
        
    def finalize_options(self):
        pass
        
    def run(self):
        try:
            import requests
            
            response = requests.get('http://localhost:5000')
            
            if response.headers['Server'] != 'Werkzeug/0.11.15 Python/2.7.12':
                print 'Please ensure that a local instance of the server is running.'
                sys.exit(1)
            else:
                import pytest
                
                pytest.main(['tests_acceptance'])
        except requests.exceptions.ConnectionError:
            print 'Please ensure that a local instance of the server is running.'
            sys.exit(1)
            
class RunAllTests(Command):
    description = 'Runs acceptance tests. Make sure a local instance of the server is active.'
    user_options = []
    
    def initialize_options(self):
        pass
        
    def finalize_options(self):
        pass
        
    def run(self):
        import subprocess
        
        if subprocess.call(['python', 'setup.py', 'test']) == 0 and subprocess.call(['python', 'setup.py', 'test_accept']) == 0:
            sys.exit(0)
        else:
            sys.exit(1)
        
class RunCodeCoverage(Command):
    description = 'Runs tests and generates a coverage report'
    user_options = []
    
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import subprocess
        import webbrowser
        
        if subprocess.call(['coverage', 'run', '--source', 'api,business', 'setup.py', 'test']) == 0:
            subprocess.call(['coverage', 'html'])
            
            if sys.platform == 'win32':
                webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open('htmlcov/index.html')
            else:
                webbrowser.open('htmlcov/index.html')

setup(
    name='StockFantasyLeague',
    version='1.0',
    description='StockFantasyLeague Server',
    author='COMP 4350 Group B',
    
    packages=find_packages(exclude=('tests', 'tests_acceptance')),
    
    install_requires=[
        'boto3==1.4.4',
        'Flask==0.12',
        'simplejson==3.10.0',
        'pytest==3.0.7',
        'yahoo-finance==1.4.0'
    ],
    
    test_suite='tests',
    tests_require=[
        'mock==2.0.0',
        'moto==0.4.31',
        'nose==1.3.7',
        'requests==2.13.0'
    ],
    
    cmdclass={
        'coverage': RunCodeCoverage,
        'run': RunServerCommand,
        'test_accept': RunAcceptanceTests,
        'test_all': RunAllTests
    }
)