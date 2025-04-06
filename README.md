## BW Exercises

## Ubuntu 24.04.2 LTS

this project runs with python3.9

in order to setup the env, run following lines

```shell
#update software packages
sudo apt update
sudo apt upgrade
#install compilers and dev tools
sudo apt install build-essential
#include newer versions of python
sudo add-apt-repository ppa:deadsnakes/ppa
#install 
sudo apt install python3.9
sudo apt install python3.9-venv
#create venv
python3.9 -m venv venv
#activate venv
source venv/bin/activate
#install requirements
pip install -r prod-requirements.txt
#upgrade cython, some libs need to compile code
pip install --upgrade cython
#handle binaries/libs
pip install wheel
#update again packages
sudo apt update
sudo apt 
```


## Exercise 1

use transactions1.csv and transactions2.csv for testing

## Exercise 2

use my_file.txt, invalid_utf8.txt and binary_file.txt for testing

my_file.txt should be the normal case

invalid_utf8.txt should ignore characters that are not recognizable by utf8

binary_file.txt should break, given that is not a normal file

## Exercise 3

just run debug on exercise 3 and test variables and states on debug terminal