#Fractalize NLP
A group of Modules encompassing common components that are used in all Fractalize NLP products and deployments

###string_generators####
Module that enables encoding of structured domain knowledge into a conditional processing graph. The conditional
processing graph is used to generate random samples of unstructured strings which represent natural language
invocations of the underlying domain knowledge

### __Building the package__
To build a deployable binary excluding source files, execute:
```console
$ python setup.py bdist_egg --exclude-source-files
```
This will produce fractalize_nlp/dist/fractalize_nlp-<version>-py3.7.egg

Upload the package to PyPi using 
### __Running Test Suite__
To run the test suite, run either:
```console
$ pytest 
```
or
```console
$ coverage run -m pytest
```
To generate the coverage report, the test suite must be invoked via coverage first. Then, run:
```console
$ coverage report -m <module_name>/<relevant_script>.py
```
To generate the full coverage report, run:
```console
$ coverage report -m
```

