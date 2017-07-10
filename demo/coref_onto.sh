#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

list="list"

ls onto_train/*.in.conllu | sed 's:.*/\(.*\).in.conllu:\1:' > $list
while read name
do
    input="onto_train/$name.in.conllu"
    output="train/$name.out.conllu"
    udapy read.Conllu files=$input demo.Coreference.OntoNotes.Onto_main write.Conllu > $output
done < $list
rm $list



ls onto_test/*.in.conllu | sed 's:.*/\(.*\).in.conllu:\1:' > $list
while read name
do
    input="onto_test/$name.in.conllu"
    plain_output="test/$name.in.conllu"
    coref_output="test/$name.out.conllu"
    cp $input $plain_output
    udapy read.Conllu files=$input demo.Coreference.OntoNotes.Onto_main write.Conllu > $coref_output
done < $list
rm $list

# adding coreference information from onf files to conllu files
#udapy read.Conllu files='!onto_train/*.in.conllu' demo.Coreference.OntoNotes.Onto_main write.Conllu > train/all.out.conllu # training files with coreference
#cat onto_test/*.in.conllu > test/all.in.conllu # testing files without coreference
#udapy read.Conllu files='!onto_test/*.in.conllu' demo.Coreference.OntoNotes.Onto_main write.Conllu > test/all.out.conllu # testing files with coreference (for evaluation)
