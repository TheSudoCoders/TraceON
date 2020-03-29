#!/bin/bash
# Tests lambda

exit_with_message() {
    echo $1
    exit
}

FUNCTION_NAME="sudotrace-portal"
aws lambda invoke --function-name ${FUNCTION_NAME} --cli-binary-format raw-in-base64-out --payload '{}' output.test
