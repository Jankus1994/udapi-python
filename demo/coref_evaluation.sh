#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

python ../udapi/block/demo/Coreference/CoNLL/conll_evaluator.py test/all.out.conllu test/auto_result.conllu # gold vs auto data
