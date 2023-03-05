#!/bin/bash

sudo echo ""

wget http://www.cs.man.ac.uk/~korovink/iprover/iProver-v3.5-smt.zip
unzip iProver-v3.5-smt.zip

echo "#!/bin/bash" > ./iProver
echo "" >> ./iProver
echo "/usr/local/bin/iProver_data/iProver-v3.5-smt/iproveropt \"\$@\"" >> ./iProver

sudo cp ./iProver /usr/local/bin/iProver
sudo chmod +x /usr/local/bin/iProver

sudo mkdir /usr/local/bin/iProver_data
sudo cp -r ./iProver-v3.5-smt /usr/local/bin/iProver_data/iProver-v3.5-smt

rm ./iProver
rm ./iProver-v3.5-smt.zip
rm -rf ./iProver-v3.5-smt

