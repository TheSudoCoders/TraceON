#!/bin/bash
# If lambda name exists, updates existing code. Otherwise, upload new.

FUNCTION_NAME="sudotrace-iot"
IAM_ROLE_NAME="sudotrace-iot-server-role"
S3_BUCKET="sudotrace-images"
USERSTORE_TABLENAME="sudotrace-user-db"
TRACESTORE_TABLENAME="sudotrace-trace-db"
DELIVERABLES="entry.py common/dao/image_store.py common/dao/trace_store.py common/dao/user_store.py common/utils.py"

zip_deliverables() {
    echo "[Script] Zipping deliverables"
    zip /tmp/deliverables.zip $DELIVERABLES
}

echo "[Script] Checking if function exists..."
aws lambda get-function --function-name ${FUNCTION_NAME} --output json

if [[ "$?" -ne 0 ]]; then
    echo "[Script] No function created. We'll check if the role exists..."
    IAM_ROLE="$(aws iam get-role --role-name ${IAM_ROLE_NAME} --output json | grep -oE "arn:.+role" --color=none)"

    if [[ "$?" -ne 0 ]]; then
	# NOTE: it is recommended that we don't create the IAM role automatically.
	echo "[Script] Please create an appropriate IAM role, called $IAM_ROLE_NAME"
	exit 1
    fi

    echo "[Script] IAM Role: $IAM_ROLE"
    echo "[Script] Role exists. Creating function."

    zip_deliverables
    aws lambda create-function --function-name ${FUNCTION_NAME} --role ${IAM_ROLE} --handler entry.handler --runtime python3.6 --zip-file fileb:///tmp/deliverables.zip
    rm /tmp/deliverables.zip
else
    echo "[Script] Found function. Updating."
    zip_deliverables
    aws lambda update-function-code --function-name ${FUNCTION_NAME} --zip-file fileb:///tmp/deliverables.zip
    rm /tmp/deliverables.zip
fi

aws lambda update-function-configuration --function-name ${FUNCTION_NAME} --environment "{\"Variables\":{\"S3_BUCKET\":\"$S3_BUCKET\", \"USERSTORE_TABLENAME\":\"$USERSTORE_TABLENAME\", \"TRACESTORE_TABLENAME\":\"$TRACESTORE_TABLENAME\"}}"
