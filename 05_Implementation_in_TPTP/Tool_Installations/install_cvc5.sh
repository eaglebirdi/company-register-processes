#!/bin/bash

sudo echo ""

wget https://github.com/cvc5/cvc5/releases/download/cvc5-1.0.4/cvc5-Linux
sudo cp ./cvc5-Linux /usr/local/bin/cvc5
sudo chmod +x /usr/local/bin/cvc5
rm ./cvc5-Linux

