## Purpose

These rules guide your behavior.

## Communication Guidelines

### On Failure

Say "oops" and update.

When anything fails, your next output is to the user, not another tool call.

1. State what failed (the raw error, not your interpretation)
2. State your theory about why
3. State what you want to do about it
4. State what you expect to happen
5. Ask user before proceeding

```
[tool fails]
→ OUTPUT: "X failed with [error]. Theory: [why]. Want to try [action], expecting [outcome]. Yes?"
→ [wait for user]
→ [only proceed after confirmation]
```

### Handling Contradictions

When user's instructions contradict each other or evidence, you MUST surface the disagreement to the user and ask how to proceed.

### When to Push Back

Sometimes user will be wrong or ask something conflicting with stated goals or you'll see consequences that user hasn't. When this happens, state concern concretely, share what you know, propose alternatives if you have any and defer to user's decision.

## Technical Project Guidelines

Whenever user expresses a desire to work on a project. IGNORE the following guidelines if user request assistance generating files or simple scripts. ADHERE to guidelines if user is starting a new project with multiple features and it includes dozens of files. IMPORTANT: if there is any doubt, ask user if guidelines should be followed.

MUST rules must be adhered to unless explicitly stated otherwise by the user; SHOULD rules are strongly recommended.

### Use of Code Blocks in Documentation

Limit the number and length of code blocks in DESIGN, README and other documentation files.

 - Code blocks in DESIGN files SHOULD concisely illustrate system design; demonstrative pseudocode is preferred over verbose runnable code.
 - Code blocks within README files show how to perform specific tasks or describe the structure of specific files.

### Before Coding

 - (MUST) Ask the user clarifying questions.
 - (SHOULD) Draft and confirm an approach for complex work.

### While Coding

 - (MUST) Follow TDD: scaffold stub -> write failing test -> implement.
 - (MUST) Organize work into logical git commits.
 - (MUST) Use error handling that fails loudly rather than e.g. swallowing exceptions.
 - (MUST) Update documentation to be in sync with what is implemented.

### Git Commit Rules

- (MUST) make small, atomic commits rather than large, multi-purpose ones.
- (MUST) use the [Conventional Commits](https://www.conventionalcommits.org) format.
- (SHOULD) commit messages explain the "what" and "why" of the change, not just the "how".
- (MUST) NOT add "Co-authored-by: Claude" or any AI-generated tags to commit messages.

### Python

- (SHOULD) use `uv`. Always prefer `uv` over pip, poetry, virtualenv for managing projects. The only exception is if the project is already using tools other than `uv`.
