FLAVOR=$1
./exaslct run-db-test --flavor-path "flavors/$FLAVOR"  --workers 7 || echo "fail" > /workspace/build-status.txt
