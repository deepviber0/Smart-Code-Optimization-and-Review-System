# Smart Code Optimization and Review System
> An automated, language-aware pedagogical code feedback and optimization platform using AST parsing, heuristics, and ML models.

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![Express](https://img.shields.io/badge/Express.js-404D59?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

---

## Methodology

### Problem Approach
The project solves the problem of providing automated, language-aware pedagogical feedback to developers and students. It analyzes code to find issues, suggests step-by-step improvements, and generates an optimized version of the input code. It focuses on structural quality, readability, and performance rather than just syntax checking.

### System Design
The system uses a hybrid approach combining rule-based heuristics and machine learning:
*   **Rule-based logic:** Employs Tree-sitter for robust Abstract Syntax Tree (AST) parsing, node-type fingerprinting to validate language selection, and regex-based transformation rules for code optimization.
*   **ML-based logic:** Uses `scikit-learn` to extract AST sequence features, process them via `TfidfVectorizer`, and analyze them with an `IsolationForest` (for anomaly detection) and a `RandomForestClassifier` (for AI-generation probability).

### Data Flow
1.  User enters raw code and selects a target language in the React frontend.
2.  The frontend sends a POST request containing the code and language to the Node.js/Express backend gateway (`/api/analyze`).
3.  The backend proxies this payload to the Python Flask AI Engine (`/analyze`).
4.  The AI Engine processes the code through a 6-step pipeline:
    *   **Language Validation:** Checks AST node fingerprints and auto-corrects mismatches.
    *   **AST Parsing:** Extracts the tree structure.
    *   **ML Extraction & Prediction:** Calculates structural score, anomaly status, and AI probability.
    *   **Heuristics:** Runs base and language-specific issue detection rules.
    *   **Scoring:** Computes a final weighted score (70% heuristics, 30% ML structural score).
    *   **Optimization:** Applies fixes (e.g., scoping, loop I/O) and validates syntax.
5.  The AI engine returns the comprehensive JSON result back through the API gateway to the frontend for visualization.

### Architectural Decisions
The project utilizes a distinct Client-Server-AI architecture:
*   **Client (React):** Provides a rich, dynamic code editor interface using CodeMirror and Framer Motion for immediate visual feedback.
*   **API Gateway (Node.js/Express):** Acts as a middle layer to handle CORS and route requests to the microservice.
*   **AI Engine (Python/Flask):** Kept as a separate microservice because Python offers superior libraries for machine learning (`scikit-learn`, `numpy`) and AST manipulation (`tree-sitter`) compared to Node.js.

## Implementation

### Tech Stack
*   **Frontend:** React (Vite), Tailwind CSS, Framer Motion, CodeMirror (with language plugins), jsPDF.
*   **Backend:** Node.js, Express, CORS, Axios, dotenv.
*   **AI/ML Layer:** Python, Flask, Flask-CORS, scikit-learn, numpy (Tree-sitter logic abstracted via `ast_parser`).

### Project Structure
```text
.
├── ai-engine/             # Python Flask ML and code parsing microservice
│   ├── app.py             # Main Flask server and 6-step analysis pipeline
│   ├── ast_parser.py      # Tree-sitter parsing integration
│   ├── heuristics/        # Base and language-specific analysis rules
│   ├── language_detector.py # AST node-type fingerprinting logic
│   ├── ml_pipeline.py     # Scikit-learn anomaly and AI-detection models
│   └── optimizer.py       # Regex-based code transformation logic
├── backend/               # Node.js Express API Gateway
│   ├── package.json       # Backend dependencies
│   └── server.js          # Express server and proxy route definitions
└── frontend/              # React User Interface
    ├── package.json       # Frontend scripts and dependencies
    ├── tailwind.config.js # Tailwind styling configuration
    ├── vite.config.js     # Vite bundler configuration
    └── src/
        ├── components/    # Reusable UI parts (CodeEditor, ScoreCircle, IssueCard)
        ├── pages/         # Application views (Editor, Landing, About)
        └── utils/         # Helper functions like PDF report generation
```

### API Endpoints
*   **`GET /api/health`** (Backend): Health check returning `{ status: 'ok' }`.
*   **`POST /api/analyze`** (Backend): Main proxy endpoint. Expects `{ code, language }`.
*   **`POST /analyze`** (AI Engine): The core processor endpoint in Flask that receives `{ code, language }` and runs the parsing/ML pipeline.

### Key Components
*   **`app.py` (AI Engine):** The orchestrator function. It strings together language validation, AST parsing, ML prediction, heuristic analysis, scoring, and optimization into a single response.
*   **`ml_pipeline.py` (AI Engine):** Defines the `MLAnalyzer` class, which transforms AST node sequences into vectors and applies anomaly and AI-detection models.
*   **`language_detector.py` (AI Engine):** Validates user language selection by cross-referencing parsed node types against unique language "fingerprints" (e.g., C++ `namespace_identifier` vs Java `method_invocation`).
*   **`Editor.jsx` (Frontend):** The primary user workspace combining the CodeMirror editor input and the animated visualization of the analysis results.

### Installation & Setup

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Backend:**
```bash
cd backend
npm install
node server.js
```

**AI Engine:**
*(Note: Setup details for the Python virtual environment are standard; execution is done via Python directly)*
```bash
cd ai-engine
# Ensure dependencies like flask, flask-cors, scikit-learn are installed
python app.py
```

### Environment Variables
Referenced in `backend/server.js`:
*   `PORT`: Port for the Express server (Defaults to `5000`)
*   `AI_ENGINE_URL`: URL to the Python Flask engine (Defaults to `http://127.0.0.1:5001`)

## Dataset Details

### Data Type & Source
The system processes unstructured plain-text code strings provided dynamically by users via the frontend text editor, along with a user-selected language string.

### Data Processing Pipeline
1.  **Parsing:** Raw text is parsed into an Abstract Syntax Tree (AST).
2.  **Extraction:** The AST is traversed to extract a flattened sequence of node types and calculate the maximum tree depth.
3.  **Vectorization:** The sequence of node types is converted into numerical vectors using `TfidfVectorizer`.
4.  **Prediction:** The vectors are fed into an `IsolationForest` (for anomaly scoring) and a `RandomForestClassifier` (for probability scoring).

### Data Format
The system ingests and outputs structured JSON.
*   **Input Data:** JSON object containing `code` (string) and `language` (string).
*   **Internal Representation:** Space-separated strings of AST node types (e.g., `"function_declaration identifier formal_parameters block"`).

### Sample Data
*   **Frontend Mock Code:** `Editor.jsx` contains a hardcoded `sampleCode` string (a flawed JavaScript function with undeclared variables and I/O inside a loop) designed to trigger the system's detection and optimization heuristics.
*   **Dummy ML Training Data:** `ml_pipeline.py` utilizes hardcoded arrays of AST node string sequences (`good_code`, `bad_code`, `ai_code`) to train the `IsolationForest` and `RandomForestClassifier` on instantiation.

### Output Structure
The AI engine generates a comprehensive JSON response resembling the following:
```json
{
  "score": {
    "overall": 85,
    "correctness": 90,
    "performance": 80,
    "readability": 90,
    "bestPractices": 85
  },
  "issues": [
    {
      "severity": "info",
      "title": "Missing documentation",
      "description": "Code lacks comments or docstrings.",
      "line": 1
    }
  ],
  "steps": [
    {
      "number": 1,
      "what": "Add comments",
      "why": "Improves readability and maintainability.",
      "how": "Add comments explaining complex logic or function definitions."
    }
  ],
  "optimizedCode": "// Optimized Version for Javascript\n...",
  "mlStats": {
    "structural_quality_score": 85,
    "ai_generated_probability": 0.1,
    "ast_node_count": 42,
    "ast_max_depth": 5,
    "is_anomalous": false
  },
  "language": "javascript"
}
```

## Features

### Core Features
| Feature | Description | Location |
|---------|-------------|----------|
| **Multi-Language Analysis** | Evaluates JS, Python, Java, C, and C++ for structural and best-practice issues. | `ai-engine/app.py` (`/analyze`) |
| **Language Auto-Correction** | Identifies incorrect language selection via AST fingerprinting and re-analyzes automatically. | `ai-engine/language_detector.py` |
| **Code Optimization** | Applies regex-based fixes (e.g., variable scoping, removing loop I/O) and validates via re-parsing. | `ai-engine/optimizer.py` |
| **PDF Report Generation** | Exports the code, issues, steps, and scores into a downloadable PDF document. | `frontend/src/utils/generateReport.js` |

### UI Features
*   **Syntax-highlighted Editor:** Integrated `CodeMirror` setup for writing code with language-specific styling.
*   **Analysis Mode Toggle:** Allows users to switch between 'Beginner' and 'Advanced' views, hiding or revealing complex ML statistics.
*   **Animated Visualizations:** Uses `framer-motion` to smoothly render score circles, issue cards, and loading states.
*   **Interactive Tabs:** The `OptimizedCode` component features a tabbed diff viewer to compare original and optimized code.

### Backend Features
*   **API Proxying:** The Node.js Express server safely proxies frontend traffic to the Python engine while managing CORS.
*   **Error Handling:** Catches and structures AI Engine timeouts or failures before passing them to the client.

### AI/ML Features
*   **Structural Anomaly Detection:** An `IsolationForest` model evaluates the vectorized AST structure to flag unusual or non-standard coding patterns.
*   **AI-Generation Prediction:** A `RandomForestClassifier` analyzes AST features to predict the percentage probability that the snippet was written by an AI.
*   **AST Depth Penalty:** Penalizes the structural quality score if the AST depth exceeds standard thresholds (indicating overly complex nesting).
