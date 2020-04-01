#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

readonly MARKDOWN_CODE_WRAPPER='```'

if [[ -z "$GITHUB_TOKEN" ]]; then
	echo "The GITHUB_TOKEN is required."
	echo "Submitting a comment will fail!"
fi

cd $GITHUB_WORKSPACE

pycode_output=$(pycodestyle ${LINTER_ARGS} .)
pycode_retval=$?
echo $pycode_output

comment="${COMMENT_MESSAGE}\n${MARKDOWN_CODE_WRAPPER}\n${pycode_output}\n${MARKDOWN_CODE_WRAPPER}"

# If there were errors as part of linting, post a comment. Else, do nothing.
if [ $pycode_retval -ne 0 ]; then
  payload=$(echo '{}' | jq --arg body "$comment" '.body = $body')
  comments_url=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)
  curl -s -S -H "Authorization: token $GITHUB_TOKEN" --header "Content-Type: application/json" --data "$payload" "$comments_url"
else
  echo "There were no pycodestyle issues"
fi

exit $pycode_retval
