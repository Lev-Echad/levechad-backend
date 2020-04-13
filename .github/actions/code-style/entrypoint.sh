#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

readonly MARKDOWN_CODE_WRAPPER='```'

if [ -z "$GITHUB_TOKEN" ]; then
    echo "The GITHUB_TOKEN is required."
    echo "Submitting a comment will fail!"
fi

cd $GITHUB_WORKSPACE

pycode_output=$(python -m pycodestyle ${LINTER_ARGS} .)
pycode_retval=$?
#pycode_output='asd\n'
#pycode_retval=1
echo $pycode_output

comment=$(echo -E "${COMMENT_MESSAGE}\\n${MARKDOWN_CODE_WRAPPER}${pycode_output}${MARKDOWN_CODE_WRAPPER}" | sed 's/\\n/\\\\n/g')

# If there were errors as part of linting, post a comment. Else, do nothing.
if [ $pycode_retval -ne 0 ]; then
  payload=$(jq -Rn --arg body "$comment" '.body = $body')
  echo $payload
  comments_url=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)
  echo -E "$payload\\n" | curl -s -S -H "Authorization: token $GITHUB_TOKEN" --header "Content-Type: application/json" --data-binary @- "$comments_url"
else
  echo "There were no pycodestyle issues"
fi

exit $pycode_retval

