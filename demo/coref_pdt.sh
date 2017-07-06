#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

# adding coreference information from pdt files to conllu files
udapy read.Conllu files='!pdt_train/*.in.conll' demo.Coreference.PDT.Pdt_main write.Conllu > train/all.out.conllu # training files with coreference
cat pdt_test/*.in.conll > test/all.in.conllu # testing files without coreference
udapy read.Conllu files='!pdt_test/*.in.conll' demo.Coreference.PDT.Pdt_main write.Conllu > test/all.out.conllu # testing files with coreference (for evaluation)
