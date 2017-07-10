#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

cat test/*.out.conllu > test/gold.conllu
cat test/*.auto.conllu > test/auto.conllu
udapy read.Conllu files='test/gold.conllu test/auto.conllu' demo.Coreference.CoNLL.Conll_pokus
