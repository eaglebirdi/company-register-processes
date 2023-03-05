#!/bin/bash

sudo echo ""

wget https://github.com/leoprover/Leo-III/releases/download/v1.6/leo3-v1.6.jar

echo "#!/bin/bash" > ./leo3
echo "" >> ./leo3
echo "java -jar /usr/local/bin/leo3_data/leo3-v1.6.jar \"\$@\"" >> ./leo3

sudo cp ./leo3 /usr/local/bin/leo3
sudo chmod +x /usr/local/bin/leo3

sudo mkdir /usr/local/bin/leo3_data
sudo cp ./leo3-v1.6.jar /usr/local/bin/leo3_data/leo3-v1.6.jar

rm ./leo3-v1.6.jar
rm ./leo3

