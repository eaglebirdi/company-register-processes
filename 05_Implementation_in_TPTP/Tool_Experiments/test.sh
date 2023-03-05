#!/bin/bash

echo "################"
echo "##### CVC5 #####"
echo "################"
cvc5 --tlimit 5000 $1
echo ""

echo "###################"
echo "##### IPROVER #####"
echo "###################"
iProver --time_out_real 5 --stats_out none --out_options none $1
echo ""

echo "###################"
echo "##### LEO-III #####"
echo "###################"
leo3 $1 -t 5 -v 0
echo ""

echo "####################"
echo "##### PRINCESS #####"
echo "####################"
princess -timeout=5000 -inputFormat=tptp +quiet -logo $1
echo ""

echo "####################"
echo "##### VAMPIRE ######"
echo "####################"
vampire -t 5 -p off $1
echo ""

