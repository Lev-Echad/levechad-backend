#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

cd $GITHUB_WORKSPACE

pycode_output="$(python -m pycodestyle ${LINTER_ARGS} . | sed 's#^#*#g')"

# If output is empty then there are no linting errors
if [ -z ${pycode_output} ]; then
	exit 0
fi

comment="{\"body\": \"${COMMENT_MESSAGE}\r\n\n${pycode_output}\"}"
echo -En ${comment} > payload.json
cat payload.json

# Escape backslashes if any
sed -i 's#\\#\\\\#g' payload.json

# Endpoint for posting comments
comments_endpoint=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)

curl -sS \
	-H "Authorization: token ${GITHUB_TOKEN}" \
	-H "Content-Type: Application/json" \
	--data-binary @payload.json \
	${comments_endpoint}

# Always fail, if we reach here there are linting errors
exit 1
