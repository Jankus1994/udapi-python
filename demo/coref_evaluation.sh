#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

udapy read.Conllu files='!test/*.out.conllu' demo.Coreference.CoNLL.Conll_merger write.Conllu > test/gold.conllu
udapy read.Conllu files='!test/*.auto.conllu' demo.Coreference.CoNLL.Conll_merger write.Conllu > test/auto.conllu
udapy read.Conllu files='test/gold.conllu test/auto.conllu' demo.Coreference.CoNLL.Conll_evaluator
#rm test/gold.conllu
#rm test/auto.conllu
