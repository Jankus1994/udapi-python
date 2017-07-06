#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

# adding coreference information from onf files to conllu files
udapy read.Conllu files='!onto_train/*.in.conllu' demo.Coreference.OntoNotes.Onto_main write.Conllu > train/all.out.conllu # training files with coreference
cat onto_test/*.in.conllu > test/all.in.conllu # testing files without coreference
udapy read.Conllu files='!onto_test/*.in.conllu' demo.Coreference.OntoNotes.Onto_main write.Conllu > test/all.out.conllu # testing files with coreference (for evaluation)
