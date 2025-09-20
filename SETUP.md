# AI Compliance Co-Pilot Setup Guide

This guide is designed for beginners and provides step-by-step instructions to help you set up, configure, and run the **AI Compliance Co-Pilot** application. Even if you are new to Google Cloud, Python, or Streamlit, you should be able to follow along.

---

## Quick Start

### Step 1: Install Dependencies

First, ensure you have **Python 3.11.8** installed on your machine. You can check your version by running:

```bash
python --version
```

If you do not have Python installed, download it from [python.org](https://www.python.org/downloads/).

Now, install the project dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all the required Python packages including **Streamlit**, **Google Cloud libraries**, and **testing tools**.

---

### Step 2: Configure Environment Variables

The application requires some configuration values stored in a file called `.env`. This file must be created in the **root folder of the project**.

Create a file named `.env` and paste the following configuration:

```env
# Required: Google Cloud Platform Configuration
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1
DOCAI_PROCESSOR_ID=your-document-ai-processor-id
```

#### What each variable means:

* **GCP\_PROJECT\_ID**: The unique ID of your Google Cloud project.
* **GCP\_REGION**: The region where your Document AI processor is deployed (e.g., `us-central1`).
* **DOCAI\_PROCESSOR\_ID**: The processor ID created in the Document AI Console.

> Note: **Jira integration is not included in this release.** In future versions, we plan to support one-click export of test cases to Jira for seamless tracking.

---

### Step 3: Run the Application

Once your `.env` file is configured, you can start the application with:

```bash
streamlit run app.py
```

After running this command, a local development server will start, and Streamlit will open a browser window (usually at [http://localhost:8501](http://localhost:8501)). This will display the AI Compliance Co-Pilot dashboard.

---

### Step 4: Run Tests (Optional)

To ensure everything is working correctly, you can run the automated test suite:

```bash
python run_tests.py --all
```

This will execute all unit, integration, and edge-case tests.

---

## Google Cloud Platform Setup

### Prerequisites

Before using the application, ensure that:

* You have a **Google Cloud Project** with billing enabled.
* The following APIs are enabled in your project:

  * **Document AI API**
  * **Vertex AI API**
  * **Cloud DLP API** (optional, for advanced privacy checks)

---

### Document AI Setup

1. Go to the [Document AI Console](https://console.cloud.google.com/ai/document-ai).
2. Create a new **processor**.
3. Choose the type of processor you need:

   * **Form Parser** (for structured forms)
   * **Document OCR** (for general text extraction)
4. Copy the processor ID and add it to your `.env` file under `DOCAI_PROCESSOR_ID`.

---

### Authentication

Google Cloud requires authentication for API access. Choose one of the following methods:

**Option 1: Service Account (Recommended for production)**

1. Go to the [Google Cloud Console IAM & Admin](https://console.cloud.google.com/iam-admin/serviceaccounts).
2. Create a **new service account**.
3. Assign it the required roles (e.g., `Document AI Editor`, `Vertex AI User`).
4. Download the JSON key file.
5. Set the environment variable:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

**Option 2: gcloud CLI (For development)**

1. Install the Google Cloud CLI: [gcloud CLI installation](https://cloud.google.com/sdk/docs/install).
2. Authenticate using:

   ```bash
   gcloud auth application-default login
   ```

---

## Features

### Fixed Issues

* Upload functionality fully operational with detailed error handling.
* Enterprise-grade UI/UX redesign with responsive layouts.
* Fixed alignment and spacing issues across devices.
* Proper formatting for LLM-generated text with consistent spacing.
* All emojis removed for a professional look.
* Improved error handling for missing configs and failed API calls.
* Edge cases addressed for workflows and input handling.
* Comprehensive test suite ensures reliability.

### Core Capabilities

1. **Compliance Scanner**: Analyze documents against global standards such as DPDPA, HIPAA, and GDPR.
2. **Test Case Generator**: Automatically generate structured test suites and export them to multiple formats (CSV, JSON, PDF).
3. **Synthetic Data Hub**: Create privacy-compliant, realistic test data using templates and prompts.
4. **AI Co-Pilot**: Get professional, AI-powered guidance on regulatory and compliance topics.

### Testing & Quality

* More than 50 automated tests covering key features.
* Strong edge-case handling.
* Linting, type checking, and code formatting applied.
* Graceful recovery from errors with user-friendly messages.

---

## Troubleshooting

### Common Issues and Fixes

**Error: "GCP\_PROJECT\_ID not found"**

* Check that your `.env` file exists and is in the root folder.
* Verify that `GCP_PROJECT_ID` is correctly set.

**Error: "Document AI processing failed"**

* Confirm your `DOCAI_PROCESSOR_ID` is correct.
* Ensure the **Document AI API** is enabled in Google Cloud.
* Check your authentication credentials.

**Error: "Vertex AI client not initialized"**

* Confirm your project ID and region match your setup.
* Verify that the **Vertex AI API** is enabled.
* Check authentication setup.

---

### Getting Help

* Review the terminal logs for detailed error messages.
* Ensure all required environment variables are present.
* Double-check that your Google Cloud project has all required APIs enabled.
* Refer to Google Cloud documentation for further guidance.

---

## Additional Resources

* [Google Cloud Documentation](https://cloud.google.com/docs)
* [Streamlit Documentation](https://docs.streamlit.io/)
* [Python Official Documentation](https://docs.python.org/3/)

---

This guide should provide everything a beginner needs to install, configure, and run the **AI Compliance Co-Pilot** with confidence.
