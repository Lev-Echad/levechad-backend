#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

if [[ -z "$GITHUB_TOKEN" ]]; then
	echo "The GITHUB_TOKEN is required."
	echo "Submitting a comment will fail!"
fi

cd $GITHUB_WORKSPACE

pycode_output=$(pycodestyle ${LINTER_ARGS} .)
pycode_retval=$?
echo $pycode_output

if [[ -z "$COMMENT_MESSAGE" ]]; then
    echo "No comment message"
else
    echo "There is a comment message"
	commit_message="${COMMENT_MESSAGE}\n${pycode_output}"
fi

# If there were errors as part of linting, post a comment. Else, do nothing.
if [ $pycode_retval -ne 0 ]; then
  payload=$(echo '{}' | jq --arg body "$pycode_output" '.body = $body')
  comments_url=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)
  curl -s -S -H "Authorization: token $GITHUB_TOKEN" --header "Content-Type: application/json" --data "$payload" "$comments_url"
else
  echo "There were no pycodestyle issues"
fi
exit $pycode_retval