# Security

Secrets — API tokens, account numbers, keys, credentials — never live in this
repo. Not in working files, not in git history.

## Convention

- Store secrets in Muse's Secure Vault (or your own password manager). Code
  reads them from the environment at runtime; committed code carries only
  placeholder names.
- If a secret ever lands in a commit, say so immediately: cleaning it up means
  rewriting published history, which needs a coordinated force-push plus fresh
  clones on every machine.

## Pre-commit guard

`hooks/pre-commit` blocks commits whose staged changes look like secrets
(tokens, keys, account-number-like digit runs).

Enable it once per clone, from the repo root:

```sh
git config core.hooksPath hooks
```

Verify it's active:

```sh
git config core.hooksPath   # should print: hooks
```

If it blocks a commit you're sure is safe: `git commit --no-verify` — and
consider tightening the patterns in `hooks/pre-commit`.

Note: Working Copy (iPad) does not run git hooks, so iPad commits aren't
covered by the guard — keep secrets out by habit there.
