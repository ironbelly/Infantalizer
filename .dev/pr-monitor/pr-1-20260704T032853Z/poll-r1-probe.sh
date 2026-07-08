#!/usr/bin/env bash
set -uo pipefail
REPO="ironbelly/Infantalizer"; PR=1; OUTDIR="$1"
for i in $(seq 1 30); do
  reviews_json=$(gh api "repos/$REPO/pulls/$PR/reviews" 2>/dev/null)
  comments_json=$(gh api "repos/$REPO/issues/$PR/comments" 2>/dev/null)
  bot_review=$(echo "$reviews_json" | jq -r '[.[] | select(.user.type=="Bot")] | length' 2>/dev/null)
  bot_comment=$(echo "$comments_json" | jq -r '[.[] | select(.user.type=="Bot")] | length' 2>/dev/null)
  if [ "${bot_review:-0}" -gt 0 ] || [ "${bot_comment:-0}" -gt 0 ]; then
    echo "$reviews_json" > "$OUTDIR/pr1-reviews.json"
    echo "$comments_json" > "$OUTDIR/pr1-comments.json"
    login=$(echo "$reviews_json$comments_json" | jq -r '.[] | select(.user.type=="Bot") | .user.login' 2>/dev/null | sort -u | tr '\n' ',')
    echo "AUGMENT-REVIEW-DETECTED on PR#1: bot=${login} reviews=${bot_review} comments=${bot_comment} (evidence captured to $OUTDIR)"
    exit 0
  fi
  sleep 30
done
echo "R1-PROBE-TIMEOUT: no Bot-type review/comment on PR#1 after 15 min — the Augment App may not be installed on $REPO"
exit 3
