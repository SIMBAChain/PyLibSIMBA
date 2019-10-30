# PyLibSIMBA

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/SIMBAChain/PyLibSIMBA/master?filepath=notebooks%2FSIMBAChain_test_comments.ipynb)


pylibsimba is a library simplifying the use of SIMBAChain APIs. We aim to abstract away the various blockchain 
concepts, reducing the necessary time needed to get to working code.

### [🏠 Homepage](https://github.com/simbachain/PyLibSIMBA#readme)
### [📝 Documentation](https://simbachain.github.io/PyLibSIMBA/)

## Install

Just needs python >=3.7, and python3.7-dev (or -devel) installed.<br>
The rest can be installed into a virtualenv with :

### Install - from PyPI

	pip install pylibsimba

## Usage

The main imports required are:

```python
from pylibsimba import get_simba_instance
from pylibsimba.wallet import Wallet
```

## Examples

See [here](https://github.com/SIMBAChain/PyLibSIMBA/blob/master/tests/examples.py)

## Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/SIMBAChain/PyLibSIMBA/issues).

## License

Copyright © 2019 [SIMBAChain Inc](https://simbachain.com/).

This project is [MIT](https://github.com/SIMBAChain/PyLibSIMBA/blob/master/LICENSE) licensed.

## Appendix

### Makefile

Adding these lines to Makefile, so that calling *make github* puts the Sphinx documentation into ./docs so the github
 pages can find it.
 
 Also creates the .nojekyll file so the github templates are ignored and js/css in subfolders is available.

	github:
		@make html
		@cp -a build/html/. ./docs
		@echo "" > ./docs/.nojekyll
		
### Install - from package

	pip install dist/pylibsimba-0.1.tar.gz

### Install - for development

    pip install -r requirements.txt
    pip install -r requirements-full.txt
    
    
## Change log

### v0.1.5
* Changes to the shape server errors are returned in
* Updates so nonce errors are retried with the suggested nonce returned from the server.
* Updates so custom solidity code can be pushed to simbachain.com

### v0.1.0 - v0.1.4
* Initial release and bugfixes
