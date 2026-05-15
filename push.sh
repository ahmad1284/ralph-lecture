#!/usr/bin/env bash
set -e

# Push local feat/clean-package (has the workflow file) to remote
git push origin feat/clean-package

# Make feat/clean-package the new main
git push origin feat/clean-package:main --force

# Clean up feat/clean-package
git push origin --delete feat/clean-package

echo "Done. Branches: main (clean), ralph (old main)"
