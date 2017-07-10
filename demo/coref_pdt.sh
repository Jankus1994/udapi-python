#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH


list="list"

ls pdt_train/*.in.conll | sed 's:.*/\(.*\).in.conll:\1:' > $list
while read name
do
    input="pdt_train/$name.in.conll"
    output="train/$name.out.conllu"
    udapy read.Conllu files=$input demo.Coreference.PDT.Pdt_main write.Conllu > $output
done < $list
rm $list



ls pdt_test/*.in.conll | sed 's:.*/\(.*\).in.conll:\1:' > $list
while read name
do
    input="pdt_test/$name.in.conll"
    plain_output="test/$name.in.conllu"
    coref_output="test/$name.out.conllu"
    cp $input $plain_output
    udapy read.Conllu files=$input demo.Coreference.PDT.Pdt_main write.Conllu > $coref_output
done < $list
rm $list

# adding coreference information from pdt files to conllu files
 # training files with coreference
#cat pdt_test/*.in.conll > test/all.in.conllu # testing files without coreference
#udapy read.Conllu files='!pdt_test/*.in.conll' demo.Coreference.PDT.Pdt_main write.Conllu > test/all.out.conllu # testing files with coreference (for evaluation)
