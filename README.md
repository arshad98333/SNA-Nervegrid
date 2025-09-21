# AI Compliance Co-Pilot for HealthTech

![alt text](https://img.shields.io/badge/Google_Cloud-GenAI_Hackathon-4285F4)

![alt text](https://img.shields.io/badge/AI_Core-Gemini_&_Vertex_AI-blueviolet)

![alt text](https://img.shields.io/badge/Framework-Streamlit-red)

![alt text](https://img.shields.io/badge/Status-Functional_Prototype-brightgreen)

---

An **enterprise-grade generative AI platform** built to resolve compliance and quality assurance bottlenecks in the HealthTech industry. By integrating **Google Vertex AI (Gemini)** and **Document AI services**, this solution automates the end-to-end QA lifecycle — from analyzing regulatory requirements to generating traceable test cases and creating privacy-safe synthetic data for development and testing.

**Repository:** [SNA-Nervegrid](https://github.com/arshad98333/SNA-Nervegrid.git)
**Live Demo:** [Demo Link](%22%22)

---

## 1. The Problem: The High Cost of Manual Compliance

The healthcare industry is one of the most regulated industries worldwide. Developers, testers, and compliance officers face significant challenges in building software that complies with **HIPAA, GDPR, FDA CFR Title 21, IEC 62304, and MDR**.

### Key Pain Points

1. **High Manual Effort**

   * Compliance officers spend weeks reading, analyzing, and mapping regulatory texts into actionable requirements.
   * Each update to a standard (for example, GDPR amendments) requires revisiting documentation and test plans.

2. **Specialized Knowledge Required**

   * Standards like FDA Part 11 or HIPAA security rules demand niche expertise.
   * Experts are costly and rare, creating bottlenecks.

3. **Broken Traceability**

   * For audits, teams must prove traceability between **requirements → test cases → execution results**.
   * Manual methods (Excel sheets, Word documents) are error-prone and difficult to scale.

4. **Privacy and Security Risks**

   * Using real patient health information (PHI) in tests violates compliance.
   * Mock data is often incomplete and unrealistic, leading to inadequate QA coverage.

### Impact

* **Slower release cycles**
* **Higher costs due to manual work**
* **Increased compliance risk** (fines, failed audits)
* **Reduced innovation** as resources are diverted to repetitive compliance checks

---

## 2. The Solution: AI-Powered Compliance Automation

The **AI Compliance Co-Pilot** automates the most labor-intensive parts of compliance and QA. It is designed as a **collaborative hub** for compliance teams, developers, and QA engineers.

### Core Features

#### 2.1 Compliance Scanner

* Upload regulatory documents (PDF, DOCX, TXT).
* The system analyzes text against international standards (**HIPAA, GDPR, FDA CFR Title 21, MDR, DPDPA**).
* Outputs structured compliance checks:

  * `[Risk - High]`: Major compliance violation detected.
  * `[Warning - Medium]`: Possible gap, requires review.
  * `[Pass]`: Meets compliance expectations.

#### 2.2 Automated Test Case Generator

* Accepts requirement documents or specifications.
* Generates structured test cases:

  * Positive tests
  * Negative tests
  * Edge cases
  * Compliance-specific validations
* Each test includes ID, description, steps, expected results, and traceability back to requirements.

#### 2.3 Synthetic Data Hub

* Generates privacy-safe datasets using natural language prompts.
* Templates: patient profiles, lab test results, appointment records.
* Fully compliant with GDPR and HIPAA — no real PHI exposure.

#### 2.4 AI Co-Pilot Assistant

* Chat interface powered by **Vertex AI Gemini**.
* Teams can ask: *“Does this requirement comply with HIPAA section 164.312?”* and receive context-aware answers.
* Functions as a regulatory knowledge base on demand.

---

## 3. Technical Architecture

The platform leverages a modular, service-oriented architecture using **Google Cloud AI services**.

```
+--------------------------------+       +------------------------------------+
|       Streamlit Frontend       | --(1)-|         Python Backend             |
|  - dashboard_ui.py             | User |  - src/modules/ (Business Logic)    |
|  - scanner_ui.py               | Input|  - src/services/ (Service Wrappers) |
|  - generator_ui.py             +------>|  - src/utils/ (Helpers)             |
+--------------------------------+       +-----------------|------------------+
                                                          | (2) Orchestrated API Calls
         +------------------------------------------------v-------------------------------------------+
         |                                Google Cloud AI & Data Services                             |
         |--------------------------------------------------------------------------------------------|
         |  [Vertex AI - Gemini Model]  |  [Document AI Processor]  | [Cloud DLP]      | [Firestore]  |
         |  - Generative AI Core        |  - Intelligent Text       | - PII Scanning   | - Audit Trail |
         |  - Analysis & Synthesis      |    Extraction             |   (Future)       |   (Future)    |
         +--------------------------------------------------------------------------------------------+
```

### Example Workflow: Test Case Generation

1. User uploads `requirements.docx` in the Streamlit interface.
2. Backend invokes `generate_test_cases_from_doc` in the test generator module.
3. Document AI extracts structured text.
4. Extracted text is embedded into a Gemini prompt.
5. Vertex AI Gemini generates JSON-formatted test cases.
6. Backend parses results into a Pandas DataFrame.
7. Streamlit UI presents test cases with export options (CSV, Excel, JSON).

---

## 4. Hackathon Alignment with Google Cloud Goals

| **Objective**                    | **Implementation in Solution**                            |
| -------------------------------- | --------------------------------------------------------- |
| Automate Test Case Generation    | Transforms unstructured docs into structured test suites. |
| Understand Complex Requirements  | Gemini interprets FDA/GDPR-heavy specifications.          |
| Integrate with Toolchains        | Jira and GitHub integration planned for future updates.   |
| Ensure Compliance & Traceability | Scanner + test case traceability ensures audit readiness. |
| GDPR-Compliant Testing           | Synthetic Data Hub ensures realistic but safe test data.  |
| Google AI Technology             | Powered by Vertex AI Gemini and Document AI.              |

---

## 5. Setup and Installation Guide

This section provides a **step-by-step beginner-friendly guide** to setting up the project, including Google Cloud configuration.

### 5.1 Prerequisites

* Python **3.11.8 or later**
* Google Cloud project with billing enabled
* APIs required:

  * Vertex AI API
  * Document AI API
  * Cloud DLP API (optional)

### 5.2 Clone Repository and Install Dependencies

```bash
git clone https://github.com/arshad98333/SNA-Nervegrid.git
cd SNA-Nervegrid
pip install -r requirements.txt
```

### 5.3 Configure Environment Variables

Create a `.env` file in the root of the project:

```env
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1
DOCAI_PROCESSOR_ID=your-document-ai-processor-id
```

**Where to find values:**

* `GCP_PROJECT_ID`: Google Cloud Console > Dashboard > Project ID
* `GCP_REGION`: Typically `us-central1`, but select the region where your services are deployed
* `DOCAI_PROCESSOR_ID`: Found in Google Cloud Console > Document AI > Processors > Copy Processor ID

### 5.4 Enable Required APIs in Google Cloud Console

1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project.
3. Navigate to **APIs & Services > Library**.
4. Enable the following:

   * **Vertex AI API**
   * **Document AI API**
   * **Cloud DLP API** (optional for PII scanning)

Command-line alternative:

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable documentai.googleapis.com
gcloud services enable dlp.googleapis.com
```

### 5.5 Authentication Setup

#### Option A: Local Development with gcloud CLI

```bash
gcloud auth application-default login
```

* Opens a browser window.
* Sign in with your Google Cloud account.
* Credentials are stored locally for API calls.

#### Option B: Service Account for Production

1. In Google Cloud Console:

   * Go to **IAM & Admin > Service Accounts**
   * Click **Create Service Account**
   * Assign roles:

     * `Document AI Editor`
     * `Vertex AI User`
   * Download the JSON key file.

2. Save it securely (do not commit to GitHub).

3. Export key path in terminal:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/service_account.json"
```

Windows (PowerShell):

```powershell
setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\service_account.json"
```

### 5.6 Run the Application

```bash
streamlit run app.py
```

Open browser: [http://localhost:8501](http://localhost:8501)

---

## 6. Testing and Quality Assurance

The project includes **pytest**-based automated tests.

### Run All Tests

```bash
python run_tests.py --all
```

### Test Categories

* **Unit Tests**: Validate core functions.
* **Integration Tests**: Verify Document AI and Vertex AI integrations.
* **Edge Case Tests**: Handle empty documents, invalid formats.
* **Linting and Type Checks**: Ensure code quality and maintainability.

### Sample Test Output

```
================= Test Session Starts =================
collected 42 items

src/tests/test_docai.py ........
src/tests/test_vertex.py .......
src/tests/test_utils.py .......

================= 42 Passed in 12.45s =================
```

---

## 7. Best Practices and Security Notes

* Do not commit `.env` or service account keys to GitHub.
* Use **Google Secret Manager** for production credentials.
* Enable **Cloud Logging** and **Monitoring** for observability.
* Regularly rotate service account keys.

---

## 8. Future Roadmap

* **Jira Integration**: One-click export of test cases.
* **Audit Trail in Firestore**: Store compliance decisions for future audits.
* **Enhanced Data Privacy**: Use Cloud DLP to auto-redact sensitive data.
* **Role-Based Access Control**: Limit access to compliance reports.
* **Multilingual Support**: Scan regulations in non-English languages.

---

## 9. Team — SNA Nervegrid

* **Sowmya A M** — HR Strategist: Aligns compliance workflows with organizational structures.
* **Naila Khan** — UI/UX Designer: Crafts intuitive, professional user interfaces.
* **Arshad Ahamed** — AI Engineer: Builds and deploys AI pipelines using Vertex AI and Document AI.

---

Developed by **SNA Nervegrid** for the **Google Cloud Generative AI Hackathon**.
