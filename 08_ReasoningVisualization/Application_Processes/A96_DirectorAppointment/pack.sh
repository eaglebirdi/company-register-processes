#!/bin/bash

mkdir ./axioms
cp ./types.ax ./axioms/types.ax
cp ./staticdata.ax ./axioms/staticdata.ax
cp ./rules.ax ./axioms/rules.ax
cp ./rules.arithmetic.ax ./axioms/rules.arithmetic.ax

echo "" > ./metadata
echo "types.ax" >> ./metadata
echo "staticdata.ax" >> ./metadata
echo "rules.ax" >> ./metadata
echo "rules.arithmetic.ax" >> ./metadata

zip -r A96_DirectorAppointment.zip ./metadata ./axioms 

rm -r ./axioms
rm -r ./metadata

