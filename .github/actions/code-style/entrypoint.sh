#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

cd $GITHUB_WORKSPACE

# Replace newlines with line break
# sed 1 explained:
#    'a:' label named "a"
#    'N' Append the next line to the pattern (<br />)
#    '$!' if not the last line 'ba' branch (goto) label a
#    's' substitue
# sed 2 explained:
#    Adds tab before each line (tab == code line in markdown)
pycode_output=$(python -m pycodestyle ${LINTER_ARGS} . | sed ':a;N;$!ba;s#\n#<br />#g' | sed 's#^#\t##g')

comment="{\"body\": \"${COMMENT_MESSAGE}<br />${pycode_output}\"}"
echo -En ${comment} > payload.json
cat payload.json

# Escape backslashes if any
sed -i 's#\\#\\\\#g' payload.json

# Endpoint for posting comments
comments_endpoint=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)

curl -sS -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: Application/json" --data-binary @payload.json ${comments_endpoint}

exit 0

