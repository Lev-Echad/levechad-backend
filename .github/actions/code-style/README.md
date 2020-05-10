# Pycodestlye Action

This action executes pycodestyle on the entire project, on each Pull Request. It will comment in the PR with pycodestyle's output.

## Inputs

### `linter-args`

**Optional** Arguments to pass to the linter.

### `comment-message`

**Optional** A message to prepend to pycodeestyle output in the comment.

## Example usage

```yaml
uses: ./.github/actions/code-style/
with:
  linter-args: '--first'
  comment-message: 'Nice code! But please fix the followings:'
```
