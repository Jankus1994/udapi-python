#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

list="list"
cd pdt_train
ls *.in.conll > ../$list
cd ..

while read p
do
  sh coref_pdt.sh $p
done < $list
rm $list
