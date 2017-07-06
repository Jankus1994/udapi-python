#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

udapy read.Conllu files='!train/all.out.conllu' demo.Coreference.CoNLL.Conll_training_selector | python ../udapi/block/demo/Coreference/Other/trainer.py model.txt
