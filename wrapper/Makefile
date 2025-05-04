# Makefile for c_formatter_42_wrapper

.PHONY: install test clean build

# Default Python interpreter
PYTHON ?= python3

# Installation directories
PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

# Files
WRAPPER_PY = c_formatter_42_wrapper.py
WRAPPER_SH = c_formatter_42_wrapper.sh
SETUP_PY = setup.py
INSTALL_SH = install.sh

# Make all executables executable
all:
	chmod +x $(WRAPPER_PY)
	chmod +x $(WRAPPER_SH)
	chmod +x $(INSTALL_SH)

# Install using pip
install:
	$(PYTHON) -m pip install .

# Install using pipx
install-pipx:
	pipx install .

# Run the install script
install-script:
	./$(INSTALL_SH)

# Manual installation
install-manual: all
	mkdir -p $(BINDIR)
	cp $(WRAPPER_PY) $(BINDIR)/c_formatter_42_wrapper.py
	cp $(WRAPPER_SH) $(BINDIR)/c_formatter_42_wrapper
	chmod +x $(BINDIR)/c_formatter_42_wrapper.py
	chmod +x $(BINDIR)/c_formatter_42_wrapper

# Run tests
test:
	$(PYTHON) -m unittest discover -s ../test

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf dist/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete

# Build distribution packages
build:
	$(PYTHON) $(SETUP_PY) sdist bdist_wheel

# Help
help:
	@echo "Makefile for c_formatter_42_wrapper"
	@echo ""
	@echo "Available targets:"
	@echo "  all            Make all executables executable"
	@echo "  install        Install using pip"
	@echo "  install-pipx   Install using pipx"
	@echo "  install-script Run the install script"
	@echo "  install-manual Install manually to PREFIX/bin"
	@echo "  test           Run tests"
	@echo "  clean          Clean build artifacts"
	@echo "  build          Build distribution packages"
	@echo ""
	@echo "Variables:"
	@echo "  PYTHON         Python interpreter (default: python3)"
	@echo "  PREFIX         Installation prefix (default: /usr/local)"
	@echo "  BINDIR         Binary directory (default: PREFIX/bin)"
