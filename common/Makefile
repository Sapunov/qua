.PHONY: build install dist srpm rpm pypi clean

PYTHON        ?= python3
INSTALL_FLAGS ?=

NAME          := qua

all: install clean

install:
	$(PYTHON) setup.py install --skip-build $(INSTALL_FLAGS)


clean:
	rm -rf build dist $(NAME)-*.tar.gz $(NAME).egg-info
