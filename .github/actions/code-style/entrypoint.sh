#!/bin/sh -l

# Get args
readonly LINTER_ARGS=$1
readonly COMMENT_MESSAGE=$2

readonly MARKDOWN_CODE_WRAPPER='```'

cd $GITHUB_WORKSPACE

pycode_output=$(python -m pycodestyle ${LINTER_ARGS} .)

comment="${COMMENT_MESSAGE}\\n${MARKDOWN_CODE_WRAPPER}${pycode_output}${MARKDOWN_CODE_WRAPPER}"
echo "This is comment: ${comment}"

#echo "::set-output name=comment::${comment}"
echo ::set-output name=COMMENT::"inline-test"

exit 0

