#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

readonly MARKDOWN_CODE_WRAPPER='```'

cd $GITHUB_WORKSPACE

pycode_output=$(python -m pycodestyle ${LINTER_ARGS} .)

comment="{\"body\": \"${COMMENT_MESSAGE}\n${MARKDOWN_CODE_WRAPPER}${pycode_output}${MARKDOWN_CODE_WRAPPER}\"}"

# Escape backspaces
escaped_comment=$(echo -nE ${comment} | sed "s#\\#\\\\#g")

#comment='{"body": "test self json"}'
echo -E $comment | tee comment.json 

comments_url=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)

curl -sS -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: Application/json" --data-binary @comment.json $comments_url

exit 0

