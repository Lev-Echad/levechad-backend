#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

readonly MARKDOWN_CODE_WRAPPER='```'

cd $GITHUB_WORKSPACE

pycode_output=$(python -m pycodestyle ${LINTER_ARGS} .)

comment="{\"body\": \"${COMMENT_MESSAGE}\n${MARKDOWN_CODE_WRAPPER}${pycode_output}${MARKDOWN_CODE_WRAPPER}\"}"
echo -En ${comment} > payload.json
cat payload.json

# Escape backspaces
sed -i 's#\\#\\\\#g' payload.json

comments_url=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)
echo ${comments_url}
cat ${GITHUB_EVENT_PATH}

curl -sS -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: Application/json" --data-binary @comment.json ${comments_url}

exit 0

