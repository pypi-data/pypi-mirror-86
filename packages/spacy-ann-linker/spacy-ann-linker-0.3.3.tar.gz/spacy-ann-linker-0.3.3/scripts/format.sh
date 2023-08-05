#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place docs/src/ spacy_ann tests --exclude=__init__.py
black spacy_ann tests docs/src
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --thirdparty spacy_ann --apply spacy_ann tests docs/src
