#!/bin/bash

sudo echo ""

wget https://github.com/vprover/vampire/releases/download/v4.7/vampire4.7.zip
unzip ./vampire4.7.zip
sudo cp ./vampire_z3_rel_static_HEAD_6295 /usr/local/bin/vampire
rm ./vampire_z3_rel_static_HEAD_6295
rm ./vampire4.7.zip
rm -rf ./bin

