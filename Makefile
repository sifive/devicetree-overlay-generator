# Copyright (c) 2019 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

all: virtualenv

venv/bin/activate:
	python3 -m venv venv
	. $@ && pip install --upgrade pip
	. $@ && pip install -r requirements.txt

.PHONY: virtualenv
virtualenv: venv/bin/activate

.PHONY: clean
clean:
	-rm -rf venv .mypy_cache __pycache__
