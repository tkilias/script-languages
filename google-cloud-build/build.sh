FLAVOR=$1
touch /workspace/build-status.txt
./exaslct build --flavor-path "flavors/$FLAVOR"  --workers 7 || echo "fail" > /workspace/build-status.txt
