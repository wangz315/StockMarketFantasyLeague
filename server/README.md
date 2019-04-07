# Stock Fantasy League - Flask Server
## Requirements

- Python 2.7

## Installation

- Uses Python's **[setuptools](https://pypi.python.org/pypi/setuptools)** to install and managed dependencies.
- Make sure **[node.js](https://nodejs.org/en/)** is installed before install npm. 
- Uses npm to mange client side testing, run ```sudo npm install npm -g```  to install npm. 
- From within this directory, run ```python setup.py install``` and ```npm install```

## Running
- ```python setup.py run``` will create a local instance of the server, which can be reached by typing ```localhost:5000``` into your browser address bar.
- The server instance will automatically refresh when file changes are detected. Therefore, there is no need to rerun the command after any changes are made.

## Testing
- ```python setup.py test``` will run all of the unit and integration tests in the tests/ directory using the **[nose](https://pypi.python.org/pypi/nose/)** module.
- ```python setup.py test_accept``` will run acceptance tests on the server's web and API routes.
- ```python setup.py test_all``` will run both commands above in serial order.
- ```npm test``` will run all of the tests in the tests/angular_client directory.
- Please make sure tests are up to date with any changes you commit. In addition, ensure that previous tests are not broken by your changes (unless said tests are no longer needed).
- It is advised that you leverage both automated and manual testing before submitting any pull requests.
- Please document the extent of your manual testing.

## Code Coverage
- ```python setup.py coverage``` will run the ```test``` command and display the unit/integration tests' code coverage percentage.

## End to End Testing
- Uses **[Protractor](http://www.protractortest.org/#/)** to manage end to end testing.
- ```npm install -g protractor``` to install Protractor.
- ```webdriver-manager update```  to get an instance of a Selenium Server running.
- ```webdriver-manager start``` to start up the server.
- To run the test, navigate to tests/end_to_end directory and run ```protractor conf.js```.
