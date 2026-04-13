# Developer Quick Start

Step-by-step commands to get the Sales Intelligence Pipeline running locally.

## 1. Backend Setup (FastAPI)

Ensure you are in the root directory (`d:\project\sales_helper`).

**Step 1: Activate Virtual Environment**
```bash
# Windows
venv\Scripts\activate

# Unix/macOS
source venv/bin/activate
```

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Environment Configuration**
Ensure your `.env` file is present in the root directory with the appropriate API keys. (e.g., `OPENAI_API_KEY`).

**Step 4: Run the Backend Server**
```bash
uvicorn backend.main:app --reload
```
*API docs available at: http://localhost:8000/docs*

---

## 2. Frontend Setup (React/Vite)

Open a new terminal window.

**Step 1: Navigate to Frontend Directory**
```bash
# From the root directory:
cd frontend
```

**Step 2: Install Dependencies**
```bash
npm install
```

**Step 3: Run the Frontend Dev Server**
```bash
npm run dev
```
*Frontend available at: http://localhost:5173*
