# Onio
KIP KOE GEIT KOE KIP GEIT KOE en je bakkes is *dicht*.

# Git recommendations

## Committing changes

1. Verify changes: `git diff`
2. Add the file: `git add <filename>`, or, if it is the only updated file: `git add -u`
3. Commit the file using a *descriptive* message: `git commit -m "Put your descriptive message here"`
4. Try to keep commits short and clean

### Adding new files
To add a new file, `git add -u` won't work because there is no copy of the file yet in the tree.
Therefore, you need to add the file: `git add <filename>`
This also works for entire directories.
