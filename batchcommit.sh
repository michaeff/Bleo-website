#!/bin/bash

# ---------------- CONFIG ----------------
BATCH=50                                 # Number of files per commit
LFS_THRESHOLD=$((100*1024*1024))         # 100 MB
MAX_RETRIES=5                            # Push retry count
BRANCH="main"                            # Change if needed

# ---------------- PREP ----------------
git lfs install --local

# Track images by default (recommended)
if ! grep -q "\*.png" .gitattributes 2>/dev/null; then
    echo "*.png filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
    git add .gitattributes
    echo "Enabled Git LFS for PNG files."
fi

mapfile -t FILES < <(git ls-files -o --exclude-standard; git ls-files -m)

if [ ${#FILES[@]} -eq 0 ]; then
    echo "No files to commit."
    exit 0
fi

COUNT=0

# ---------------- FUNCTIONS ----------------

push_with_retry() {
    local attempt=1

    while [ $attempt -le $MAX_RETRIES ]; do
        echo "Push attempt $attempt/$MAX_RETRIES..."

        # Timeout after 120 seconds so push cannot hang forever
        if timeout 120 git push --force origin main; then
            echo "Push succeeded."
            return 0
        else
            echo "Push failed (exit $?). Retrying in 5 seconds..."
            sleep 5
        fi

        attempt=$((attempt+1))
    done

    echo "ERROR: Push failed after $MAX_RETRIES attempts."
    exit 1
}

# ---------------- LOOP ----------------

for f in "${FILES[@]}"; do
    [ -f "$f" ] || continue

    FILESIZE=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f")

    if [ "$FILESIZE" -gt "$LFS_THRESHOLD" ]; then
        echo "Tracking large file: $f ($((FILESIZE/1024/1024)) MB)"
        git lfs track "$f"
        git add .gitattributes
    fi

    git add "$f"
    COUNT=$((COUNT+1))
    echo "Staged: $f ($COUNT/$BATCH)"

    if [ $COUNT -ge $BATCH ]; then
        git commit -m "Batch commit"
        push_with_retry
        COUNT=0
    fi
done

# ---------------- FINAL COMMIT ----------------

if [ $COUNT -gt 0 ]; then
    git commit -m "Final batch"
    push_with_retry
fi

echo "All files committed and pushed successfully."
