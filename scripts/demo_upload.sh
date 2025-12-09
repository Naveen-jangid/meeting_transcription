#!/usr/bin/env bash
set -euo pipefail

FILE_NAME=${1:-demo.mp3}
ORG_ID=${2:-01}
API=${API:-http://localhost:8080}

CREATE=$(curl -s -X POST "$API/meetings/create?file_name=$FILE_NAME&org_id=$ORG_ID")
MID=$(echo "$CREATE" | python -c "import json,sys;print(json.load(sys.stdin)['meeting_id'])")
URL=$(echo "$CREATE" | python -c "import json,sys;print(json.load(sys.stdin)['upload_url'])")

echo "Meeting ID: $MID"
echo "Upload URL: $URL"
