#!/bin/bash

mkdir ./axioms
cp ./types.ax ./axioms/types.ax
cp ./staticdata.ax ./axioms/staticdata.ax
cp ./rules.ax ./axioms/rules.ax

echo "" > ./metadata
echo "types.ax" >> ./metadata
echo "staticdata.ax" >> ./metadata
echo "rules.ax" >> ./metadata

zip -r A115_CompanyDissolution_noarith.zip ./metadata ./axioms 

rm -r ./axioms
rm -r ./metadata

