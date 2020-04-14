#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

cd $GITHUB_WORKSPACE

# Execute pycodestyle, escape the literal '\.' (might occur in W605), prepend each line with '`*', and append '`'
pycode_output="$(python -m pycodestyle ${LINTER_ARGS} . | sed 's#\\.#\\\\.#g' | sed 's#^#* \`#g' | sed 's#$#\`#g')"

# If output is empty then there are no linting errors
if [ -z "${pycode_output}" ]; then
	exit 0
fi

comment="{\"body\": \"${COMMENT_MESSAGE}\r\n\n${pycode_output}\"}"
echo -En "${comment}" > payload.json

# Escape backslashes if any
#sed -i 's#\\#\\\\#g' payload.json

# Endpoint for posting comments
comments_endpoint=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)

set -x
response_code="$(curl -sS \
	-H "Authorization: token ${GITHUB_TOKEN}" \
	-H "Content-Type: Application/json" \
	--data-binary @payload.json \
	-w "%{http_code}\n" \
	${comments_endpoint} | tail -1)"

# If something went wrong, try notfiying with a comment (201 - Created is expected)
if [  ${response_code} -ne 201 ]; then
	echo "Something went wrong, post a warning comment!"
	curl -sS \
		-H "Authorization: token ${GITHUB_TOKEN}" \
		-H "Content-Type: Application/json" \
		--data '{"body": "Something went wrong! Please check code-style workflow!"}' \
		${comments_endpoint}
fi


# Always fail, if we reach here there are linting errors
exit 1
