# AI Compliance Co-Pilot for HealthTech

![alt text](https://img.shields.io/badge/Google_Cloud-GenAI_Hackathon-4285F4)

![alt text](https://img.shields.io/badge/AI_Core-Gemini_&_Vertex_AI-blueviolet)

![alt text](https://img.shields.io/badge/Framework-Streamlit-red)

![alt text](https://img.shields.io/badge/Status-Functional_Prototype-brightgreen)

---

An **enterprise-grade generative AI platform** engineered to resolve the most pressing compliance and quality assurance bottlenecks in the HealthTech industry. By integrating **Google Vertex AI (Gemini)** and **Document AI services**, this solution automates the end-to-end QA lifecycle—from analyzing regulatory requirements to generating traceable test cases and creating privacy-safe synthetic data.

**Repository:** [SNA-Nervegrid](https://github.com/arshad98333/SNA-Nervegrid.git)
**Live Demo:** [Demo Link](%22%22)

---

## 1. The Problem: The High Cost of Manual Compliance

The development of healthcare software is constrained by the immense burden of **regulatory compliance** and **manual testing**. QA and compliance teams face several challenges:

* **Intense Manual Labor**: Reading hundreds of pages of regulatory documents to author test cases is slow, repetitive, and error-prone.
* **Deep Domain Expertise Required**: Applying standards like **FDA CFR Title 21, IEC 62304, HIPAA, GDPR** requires years of expertise, making talent scarce and costly.
* **Broken Traceability**: Maintaining a verifiable link between requirements, test cases, and results is critical but extremely difficult manually.
* **Data Privacy & Security Risks**: Using real PHI in testing is a compliance violation. Mock data is often incomplete, leading to inadequate QA.

These bottlenecks cause **slower development cycles, higher costs, increased compliance risk,** and limit innovation in healthcare.

---

## 2. Our Solution: An AI-Powered Automation Engine

The **AI Compliance Co-Pilot** is a unified, intelligent platform that automates the most labor-intensive tasks in HealthTech QA, serving as a **collaborative hub** for compliance, development, and QA teams.

*(A GIF demo would show uploading a document, scanning against HIPAA, and generating a structured test suite.)*

### Core Features & Capabilities

**Real-Time Compliance Scanner**

* Analyzes requirements against global standards (**DPDPA, HIPAA, GDPR, FDA, MDR**).
* Uses AI-powered expert personas to identify risks, ambiguities, and violations.
* Produces actionable reports: **\[Risk - High]**, **\[Warning - Medium]**, **\[Pass]**.

**Automated Test Case Generator**

* Ingests specifications (PDF, DOCX, TXT).
* Autonomously generates comprehensive test suites (positive, negative, edge, compliance).
* Each case includes ID, description, steps, expected results, and traceability.

**On-Demand Synthetic Data Hub**

* Generates **privacy-safe, realistic datasets** via natural language prompts.
* Pre-built templates: patient profiles, lab results, appointments.
* Eliminates PHI risks, enabling **GDPR-compliant testing**.

**AI Co-Pilot Assistant**

* Chat interface powered by **Gemini**.
* Provides instant answers to complex compliance queries.
* Functions as an **on-demand regulatory knowledge base**.

---

## 3. Technical Architecture & Workflow Deep Dive

Built on a **modular, scalable architecture** leveraging Google Cloud’s AI services.

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

### Workflow Example: Test Case Generation

1. **Upload (UI Layer)**: User uploads `requirements.docx` in `generator_ui.py`.
2. **Backend Trigger**: Calls `generate_test_cases_from_doc` in `test_case_generator.py`.
3. **Document Processing (Service Layer)**:

   * Calls `process_document` in `gcp_doc_ai.py`.
   * Document AI extracts structured text.
4. **Generative AI Task**:

   * Embeds text into engineered prompt for Gemini.
   * Calls `generate_text` in `gcp_vertex_ai.py`.
5. **Response Handling**:

   * Gemini returns structured JSON test cases.
   * Backend parses into a Pandas DataFrame.
6. **UI Display & Export**:

   * Interactive table shown in Streamlit.
   * Export options: CSV, Excel, JSON.

---

## 4. Hackathon Challenge Alignment

| **Objective**                    | **How We Deliver**                                          |
| -------------------------------- | ----------------------------------------------------------- |
| Automate Test Case Generation    | Transforms unstructured docs into multi-format test suites. |
| Understand Complex Requirements  | Gemini personas interpret FDA/GDPR-heavy specifications.    |
| Integrate with Toolchains        | Jira integration planned for **future one-click export**.   |
| Ensure Compliance & Traceability | Compliance Scanner + traceable test cases.                  |
| Enable GDPR-Compliant Pilots     | Synthetic Data Hub generates safe, realistic data.          |
| Use Google AI Tech Stack         | Powered by **Vertex AI + Document AI**.                     |

---

## 5. Setup and Installation Guide

### Prerequisites

* **Python 3.11.8+**
* Google Cloud project with billing enabled.
* APIs required: **Vertex AI API, Document AI API**.

### Step 1: Clone Repository & Install Dependencies

```bash
git clone https://github.com/arshad98333/SNA-Nervegrid.git
cd SNA-Nervegrid
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google Cloud Platform Configuration
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1
DOCAI_PROCESSOR_ID=your-document-ai-processor-id
```

**Variable Reference**

* `GCP_PROJECT_ID` → Your Google Cloud project ID (Dashboard).
* `GCP_REGION` → Region where your Document AI processor is deployed.
* `DOCAI_PROCESSOR_ID` → ID of your Document AI processor.

### Step 3: Authenticate with Google Cloud

**Option A: gcloud CLI (local development)**

```bash
gcloud auth application-default login
```

**Option B: Service Account (production)**

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

Access via browser: **[http://localhost:8501](http://localhost:8501)**

---

## 6. Testing & Quality Assurance

The project includes a **pytest suite** covering unit, integration, and edge cases.

Run all tests:

```bash
python run_tests.py --all
```

Quality checks include:

* Linting & type checking
* Error handling validation
* Robust exception coverage

---

## 7. The Team — SNA Nervegrid

**Sowmya A M** — *HR Strategist*
Guides organizational alignment and ensures compliance processes integrate smoothly with team workflows.

**Naila Khan** — *UI-UX Designer*
Designs intuitive, professional interfaces ensuring a user-first, enterprise-grade experience.

**Arshad Ahamed** — *AI Engineer*
Architects AI pipelines, integrates Vertex AI & Document AI, and builds automation logic.

---

> Developed by **SNA Nervegrid** for the **Google Cloud Generative AI Hackathon**.
