$LOG_BUCKET=$1
$FLAVOR=$2
$BUILD_ID=$3
gsutil rsync -x exports -r .build_output "$LOG_BUCKET/build_output/$FLAVOR/$BUILD_ID/"
if [[ $(< /workspace/build-status.txt) == "fail" ]]; then
	exit 1
fi
