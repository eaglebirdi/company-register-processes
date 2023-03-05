#!/bin/bash

sudo echo ""

wget https://github.com/uuverifiers/princess/releases/download/snapshot-2022-11-03/princess-bin-2022-11-03.zip
unzip princess-bin-2022-11-03.zip

echo "#!/bin/bash" > ./princess
echo "" >> ./princess
echo "/usr/local/bin/princess_data/princess \"\$@\"" >> ./princess

sudo cp ./princess /usr/local/bin/princess
sudo chmod +x /usr/local/bin/princess

sudo mkdir /usr/local/bin/princess_data
sudo cp ./princess-bin-2022-11-03/princess /usr/local/bin/princess_data/princess
sudo cp -r ./princess-bin-2022-11-03/dist /usr/local/bin/princess_data/dist

rm ./princess
rm ./princess-bin-2022-11-03.zip
rm -rf ./princess-bin-2022-11-03

