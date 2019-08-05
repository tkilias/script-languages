export LC_ALL=C.UTF-8
export LANG=C.UTF-8
apt-get update
apt-get install -y python3-pip git
pip3 install pipenv
./exaslct export --flavor-path  --workers 7
