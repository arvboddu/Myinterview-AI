# MyInterview AI

MyInterview AI is a local mock interview app for PM-delivery style practice. It includes a FastAPI backend, a Streamlit frontend, local retrieval support, resume analysis, JD intelligence, feature-planning workflows, resume-based question generation, and placeholder voice integrations.

## Current behavior

### Frontend

The Streamlit app includes six main tabs:

- `Interview`: sends one message at a time to the backend interview engine and displays the rolling interviewer response
- `Job Description Intelligence`: supports Option A and Option C by analyzing pasted JD text or uploaded JD files and generating JD-based interview packages
- `Feature Lab`: supports Option B by turning a plain-language feature request into an implementation plan
- `Resume Review`: analyzes pasted resume text, can analyze an uploaded resume file, and can generate tailored interview questions from that file
- `RAG Search`: lets you directly inspect the context returned by the retrieval layer
- `Voice Tools`: exercises the backend placeholder speech-to-text and text-to-speech routes

The sidebar includes an interview reset control that clears the backend conversation history.

### Backend

The backend exposes:

- conversational interview generation through `/api/interview`
- interview history reset through `/api/reset`
- JD analysis through `/api/jd/analyze`
- JD-based interview package generation through `/api/jd/generate-interview`
- uploaded JD analysis through `/api/jd/analyze-upload`
- uploaded JD interview package generation through `/api/jd/generate-interview-upload`
- feature planning through `/api/features/plan`
- resume text analysis through `/api/resume/analyze`
- resume upload plus question generation through `/api/resume/questions`
- retrieval search through `/api/rag/search`
- voice placeholders through `/api/voice/stt` and `/api/voice/tts`

The backend uses Ollama when available and falls back gracefully in a few service paths if local model or service dependencies are unavailable.

## Project structure

```text
backend/
  Dockerfile
  config.py
  main.py
  models/
  routers/
  services/
frontend/
  app.py
  Dockerfile
rag/
  ingest.py
  splitter.py
  embeddings.py
  vectorstore.py
nginx/
  nginx.conf
  Dockerfile
docker-compose.yml
```

## Local run

### Backend

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8001
```

### Frontend

```bash
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

The frontend expects the backend at `http://localhost:8001/api` by default.

## PowerShell helper

For Windows-friendly shortcuts, use [`scripts/dev.ps1`](/c:/Users/aravind.boddu/Desktop/Myinterview/fullcodebase/scripts/dev.ps1).

Examples:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 start-all
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 status
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 restart-all
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 stop-all
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 backend
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 frontend
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 compose-up
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 health
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 interview
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 reset
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 resume
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 questions
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 rag
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 voice-tts
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 voice-stt
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 jd-analyze
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 jd-generate
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 jd-upload-analyze
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 jd-upload-generate
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 feature-plan
```

Supported commands:

- `start-all`: start backend and frontend in the background and wait for both ports to come up
- `status`: show whether backend and frontend are running, plus the tracked PID files and URLs
- `restart-all`: stop and relaunch both services in the background
- `stop-all`: stop both background services
- `backend`: run the FastAPI app on port `8001`
- `frontend`: run the Streamlit app
- `compose-up`: start the Docker stack
- `health`: call `GET /health`
- `interview`: send a sample interview request
- `reset`: reset backend interview history
- `resume`: send a sample resume analysis request
- `questions`: upload a sample resume file for question generation
- `rag`: run a sample retrieval query
- `voice-tts`: send a sample text-to-speech request
- `voice-stt`: upload a sample `.wav` file to the speech-to-text route
- `jd-analyze`: analyze a sample job description
- `jd-generate`: generate a JD-based interview package and activate JD-aware mode
- `jd-upload-analyze`: upload a sample JD file for analysis
- `jd-upload-generate`: upload a sample JD file and activate JD-aware interview mode
- `feature-plan`: create a sample implementation plan from a natural-language feature request

## Docker run

```bash
docker compose up --build
```

Then open:

- `http://localhost` through Nginx
- `http://localhost:8501` for Streamlit directly

The Compose setup now persists Ollama model data in a named Docker volume and points backend vector storage to `/app/vectorstore` inside the mounted project directory.
Backend and frontend now also have dedicated Dockerfiles, so the production bundle more closely matches a conventional deployable layout.

## Recommended local startup

For the most reliable Windows workflow, start the local app stack with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 start-all
```

Then confirm the process manager sees both services:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 status
```

Expected URLs:

- Frontend: `http://127.0.0.1:8501`
- Backend health: `http://127.0.0.1:8001/health`

If you need to relaunch everything:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 restart-all
```

If you want to stop the background services:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 stop-all
```

## Smoke tests

After starting the backend and frontend, use these quick checks.

### Backend smoke tests

Health check:

```bash
curl http://localhost:8001/health
```

Interview request:

```bash
curl -X POST http://localhost:8001/api/interview ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Ask me a PM-delivery interview question about execution risk.\"}"
```

Reset interview history:

```bash
curl -X POST http://localhost:8001/api/reset
```

Resume analysis:

```bash
curl -X POST http://localhost:8001/api/resume/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Product manager with delivery ownership across roadmap planning, stakeholder management, and release execution.\"}"
```

RAG search:

```bash
curl "http://localhost:8001/api/rag/search?q=stakeholder%20management"
```

JD analysis:

```bash
curl -X POST http://localhost:8001/api/jd/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"PM-delivery role responsible for cross-functional execution, release planning, stakeholder alignment, KPI tracking, and risk mitigation.\"}"
```

JD upload analysis:

```bash
curl -X POST http://localhost:8001/api/jd/analyze-upload -F "file=@sample_jd.pdf"
```

Feature planning:

```bash
curl -X POST http://localhost:8001/api/features/plan ^
  -H "Content-Type: application/json" ^
  -d "{\"request\":\"Add a delivery-risk simulation mode with competency scoring for every answer.\"}"
```

### Frontend smoke tests

1. Open `http://localhost:8501`.
2. In `Interview`, send a message such as `Ask me a PM-delivery interview question about dependencies`.
3. Click `Reset Interview` in the sidebar and confirm the next backend reply starts a fresh conversation.
4. In `Job Description Intelligence`, paste a JD and confirm analysis plus generated interview categories appear.
5. Upload a `.txt`, `.pdf`, or `.docx` JD file and confirm uploaded analysis and file-based interview generation both work.
6. In `Feature Lab`, describe a feature and confirm the implementation plan is returned.
7. In `Resume Review`, paste sample resume text and confirm an analysis appears.
8. Upload a small `.txt`, `.pdf`, or `.docx` resume file and confirm uploaded analysis plus question generation both work.
9. In `RAG Search`, submit a query and confirm retrieved context is displayed.
10. In `Voice Tools`, enter sample text for TTS and upload a small audio file for STT to confirm both routes respond.

## Environment variables

These backend settings are supported in [`backend/config.py`](/c:/Users/aravind.boddu/Desktop/Myinterview/fullcodebase/backend/config.py):

- `OLLAMA_HOST`: Ollama base URL, default `http://ollama:11434`
- `CHROMA_PATH`: Chroma persistence path, default `vectorstore`
- `EMBED_MODEL`: embedding model name placeholder, default `BAAI/bge-large-en`
- `TTS_HOST`: TTS service base URL, default `http://tts:5002`
- `WHISPER_BIN`: whisper executable name, default `whisper`

## API routes

### Core

- `GET /` returns backend status
- `GET /health` returns a simple health response

### Interview

- `POST /api/interview`
  Request body:

```json
{
  "message": "Ask me a PM-delivery interview question about execution risk."
}
```

- `POST /api/reset`
  Resets the in-memory interview history

### Job Description Intelligence

- `POST /api/jd/analyze`
  Parses responsibilities, requirements, competencies, tools, KPIs, and question categories from pasted JD text

- `POST /api/jd/generate-interview`
  Analyzes the JD, inserts it into the retrieval layer, and activates JD-aware interview behavior

- `POST /api/jd/analyze-upload`
  Accepts a `.txt`, `.pdf`, or `.docx` JD file, extracts text, and returns JD analysis

- `POST /api/jd/generate-interview-upload`
  Accepts a `.txt`, `.pdf`, or `.docx` JD file, extracts text, inserts it into retrieval, and activates JD-aware interview behavior

### Feature Planning

- `POST /api/features/plan`
  Converts a natural-language feature request into a backend/frontend implementation plan

### Resume

- `POST /api/resume/analyze`
  Request body:

```json
{
  "text": "Paste resume text here"
}
```

- `POST /api/resume/upload`
  Uploads a resume file and returns extracted text plus analysis

- `POST /api/resume/questions`
  Uploads a resume file and returns generated PM-delivery questions

### Retrieval

- `GET /api/rag/search?q=stakeholder+management`

### Voice

- `POST /api/voice/stt`
  Uploads an audio file and returns transcribed text when whisper is available

- `POST /api/voice/tts`
  Request body:

```json
{
  "text": "Tell me about a delivery tradeoff you handled."
}
```

## Notes

- Interview history is currently stored in memory and resets when the backend restarts.
- Resume question generation depends on model output shape and may return raw text if parsing fails.
- Chroma retrieval is used when installed and available; otherwise the app falls back to a local text-based retrieval path.
- Voice routes are integration-ready, but they still depend on external whisper and TTS services being available.
