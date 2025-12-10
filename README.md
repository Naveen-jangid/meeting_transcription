# Fireflies-like Meeting Engine – Dev Blueprint (FastAPI + Celery + Mongo + Whisper + GPT)

A production-oriented reference architecture you can clone and run. Includes service layout, data models, jobs pipeline, prompts, and security patterns.

## Repository layout

```
fire-meeting-engine/
├─ api/
│  ├─ main.py                  # FastAPI app (ingest, status, search, export)
│  ├─ deps.py                  # DI: db, storage, settings
│  ├─ routers/
│  │  ├─ meetings.py           # create/upload/ingest, webhook callbacks
│  │  ├─ transcripts.py        # get captions, timeline, speakers
│  │  ├─ summaries.py          # get/update summaries & action items
│  │  ├─ search.py             # keyword + semantic search endpoints
│  ├─ schemas.py               # Pydantic DTOs for API
│  └─ auth.py                  # JWT auth + RBAC stubs
├─ workers/
│  ├─ celery_app.py            # Celery app, queues, beat schedule
│  ├─ celeryconfig.py          # Broker/result backends, task routes, retries
│  ├─ tasks/
│  │  ├─ ingest.py             # audio normalization, media probe
│  │  ├─ asr.py                # Whisper / Deepgram transcription
│  │  ├─ diarize.py            # Pyannote diarization (optional)
│  │  ├─ align.py              # WhisperX alignment (optional)
│  │  ├─ enrich.py             # NER, sentiment, filter classification
│  │  ├─ summarize.py          # LLM summarization & action items
│  │  ├─ analytics.py          # talk-time, questions, keyword stats
│  │  ├─ persist.py            # write to Mongo/ES, build indices
│  │  ├─ nightly_dedup.py      # batch duplication finder w/ temporary index
│  │  └─ webhooks.py           # send notifications (email/slack/in-app)
├─ nlp/
│  ├─ ner.py                   # spaCy/HF NER wrapper
│  ├─ sentiment.py             # classifier wrapper
│  ├─ filters.py               # task/note/question labels
│  ├─ prompts.py               # LLM prompt templates (meeting types)
│  └─ llm_client.py            # OpenAI/Anthropic/local LLM client
├─ data/
│  └─ stopwords.txt
├─ infra/
│  ├─ docker-compose.yml
│  ├─ Dockerfile.api
│  ├─ Dockerfile.worker
│  ├─ nginx.conf
│  └─ k8s/* (optional manifests)
├─ storage/
│  ├─ s3.py                    # S3/MinIO client & presigned URLs
│  └─ local.py                 # local FS fallback
├─ db/
│  ├─ mongo.py                 # Mongo client + indices
│  ├─ es.py                    # Elasticsearch/OpenSearch client + mappings
│  └─ models.py                # Mongo document shapes
├─ security/
│  ├─ sanitize.py              # PII scrubbing before LLM
│  └─ kms.py                   # KMS envelope encryption helpers
├─ scripts/
│  ├─ bootstrap_indices.py     # create ES indexes and analyzers
│  ├─ create_rbac_roles.py
│  └─ demo_upload.sh
├─ tests/
│  └─ ...
├─ .env.example
├─ requirements.txt
└─ README.md
```

## Environment & Dependencies

See `requirements.txt` and `.env.example` for core dependencies and environment variables. Optional diarization/alignment dependencies are included for parity with the Fireflies-like pipeline.

## Local development

### Run directly with FastAPI (no Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m api.main
```

The app loads environment variables from `.env` on startup and binds to `API_HOST`/`API_PORT` as defined in your environment (defaults to `0.0.0.0:8080`).

#### Quick cURL checks

```bash
BASE_URL="http://localhost:8080"

# 1) Create a meeting record (captures your org + file name)
MEETING_ID=$(curl -s -X POST "${BASE_URL}/meetings/create?file_name=call.mp3&org_id=acme" | jq -r '.meeting_id')
echo "Meeting ID: ${MEETING_ID}"

# 2) Upload audio directly to the API (stored under data/uploads and triggers pipeline)
curl -X POST "${BASE_URL}/meetings/${MEETING_ID}/upload" \
  -F "file=@/absolute/path/to/call.mp3"

# 2b) If a file already exists locally, you can instead mark it uploaded and kick off processing
curl -X POST "${BASE_URL}/meetings/${MEETING_ID}/uploaded" \
  -H "Content-Type: application/json" \
  -d "{\"local_path\":\"data/uploads/${MEETING_ID}_call.mp3\"}"

# 3) Fetch the transcript and summary once processing is complete
curl "${BASE_URL}/transcripts/${MEETING_ID}"
curl "${BASE_URL}/summaries/${MEETING_ID}"

# 4) Search for a phrase across indexed captions
curl "${BASE_URL}/search?q=follow%20up"
```

The upload endpoints persist files locally and fire the Celery pipeline without any S3 or presigned URL requirements. Common audio formats (mp3, wav, m4a, etc.) are accepted; uploads are converted to wav automatically when ffmpeg is available. The transcript/summary/search endpoints expect your backing MongoDB/Elasticsearch instances to be running with data from the processing pipeline.

### Run with Docker Compose

```bash
docker compose -f infra/docker-compose.yml up --build
```

## End-to-end flow

1. `POST /meetings/create` → returns `meeting_id` + suggested local upload path.
2. Client uploads media directly to the API (stored locally under `data/uploads`).
3. `POST /meetings/{id}/uploaded` → triggers Celery pipeline.
4. ASR → optional diarization → enrichment → LLM summarization → analytics → notification.

## Notes

This blueprint mirrors how Fireflies-style systems are built in practice and can be expanded with real integrations, security controls, and frontend contracts.
