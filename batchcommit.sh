#!/bin/bash

BATCH=20
COUNT=0

# Get all files (untracked + modified) after reset
mapfile -t FILES < <(git status --porcelain | awk '{print $2}')

if [ ${#FILES[@]} -eq 0 ]; then
    echo "No files to commit. Make sure you have unstaged changes."
    exit 1
fi

for f in "${FILES[@]}"; do
    git add "$f"
    COUNT=$((COUNT+1))
    echo "Staged: $f ($COUNT/$BATCH)"

    if [ $COUNT -ge $BATCH ]; then
        git commit -m "Batch commit"
        echo "Pushing batch..."
        git push --force origin main

        COUNT=0
    fi
done

if [ $COUNT -gt 0 ]; then
    git commit -m "Final batch"
    echo "Pushing final batch..."
    git push --force origin main

fi

echo "All files committed and pushed in batches."
