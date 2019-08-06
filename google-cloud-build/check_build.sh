if [[ $(< /workspace/build-status.txt) == "fail" ]]; then
	exit 1
fi
