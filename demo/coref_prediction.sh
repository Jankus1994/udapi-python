#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

udapy read.Conllu files='!test/all.in.conllu' demo.Coreference.CoNLL.Conll_prediction_selector | # selection of feature of the predicted file
python3 ../udapi/block/demo/Coreference/Other/predictor.py model.txt | # prediction using a saved model
udapy read.Conllu files='!test/all.in.conllu' demo.Coreference.CoNLL.Conll_coref_adder write.Conllu > test/auto_result.conllu # adding of coref information to the predicted file
