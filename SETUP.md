# AI Compliance Co-Pilot — Setup Guide

This guide explains step-by-step how to install, configure, and run the **AI Compliance Co-Pilot** application. It is written for beginners, so even if you are new to Google Cloud, Python, or Streamlit, you should be able to follow along.

---

## Quick Start

### Step 1: Install Python and Dependencies

1. Make sure you have **Python 3.11.8** installed. To check your version, open your terminal or command prompt and type:

   ```bash
   python --version
   ```

   If the version is not **3.11.8**, download and install the correct version from [python.org](https://www.python.org/downloads/).

2. Navigate to your project folder using your terminal. For example:

   ```bash
   cd path/to/your/project
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   This command installs all the necessary dependencies, including **Streamlit**, **Google Cloud client libraries**, and the testing tools used in the project.

---

### Step 2: Configure Environment Variables

The application needs a configuration file to know how to connect to Google Cloud. This is done using a `.env` file.

1. In the **root folder** of your project, create a new file named `.env`.

2. Copy and paste the following lines into the `.env` file:

   ```env
   GCP_PROJECT_ID=your-gcp-project-id
   GCP_REGION=us-central1
   DOCAI_PROCESSOR_ID=your-document-ai-processor-id
   ```

3. Replace the placeholders with your actual Google Cloud details:

   * **GCP\_PROJECT\_ID**: The unique ID of your Google Cloud project.
   * **GCP\_REGION**: The region where your Document AI processor is deployed (for example, `us-central1`).
   * **DOCAI\_PROCESSOR\_ID**: The ID of your Document AI processor, which you will get from the Google Cloud console.

*Note: Jira integration is planned for future versions, but it is not included in this release.*

---

### Step 3: Run the Application

Once the `.env` file is ready:

1. Start the application with:

   ```bash
   streamlit run app.py
   ```

2. A local server will start, and your web browser will open at [http://localhost:8501](http://localhost:8501).

3. You should now see the **AI Compliance Co-Pilot dashboard** running on your machine.

---

### Step 4: Run Tests (Optional)

If you want to confirm that everything is working correctly:

```bash
python run_tests.py --all
```

This will run all available tests, including unit tests, integration tests, and edge-case checks.

---

## Setting Up Google Cloud Platform

### Prerequisites

Before using the application, you must have:

* A Google Cloud project with **billing enabled**.
* The following APIs enabled in your project:

  * **Document AI API**
  * **Vertex AI API**
  * **Cloud DLP API** (optional, only needed for advanced privacy checks)

---

### Setting Up Document AI

1. Go to the [Document AI Console](https://console.cloud.google.com/ai/document-ai).
2. Create a new **processor**.
3. Choose the type of processor you need:

   * **Form Parser** for structured forms.
   * **Document OCR** for general text extraction.
4. Copy the processor ID from the console and paste it into your `.env` file as the value for `DOCAI_PROCESSOR_ID`.

---

### Authentication with Google Cloud

You must authenticate with Google Cloud so the app can access the APIs.

**Option 1: Service Account (Recommended for production use)**

1. Go to [IAM & Admin → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts).
2. Create a new service account.
3. Assign the following roles:

   * `Document AI Editor`
   * `Vertex AI User`
4. Download the service account key as a JSON file.
5. Set an environment variable in your terminal:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

   Replace `path/to/your/service-account-key.json` with the actual file path.

**Option 2: gcloud CLI (Easier for development)**

1. Install the Google Cloud CLI by following the instructions at [gcloud CLI installation](https://cloud.google.com/sdk/docs/install).
2. Authenticate by running:

   ```bash
   gcloud auth application-default login
   ```

---

## Features

### Improvements and Fixes

* File upload works smoothly with detailed error messages if something goes wrong.
* The user interface is redesigned to be professional and responsive.
* Proper formatting of AI-generated text for easier reading.
* Better handling of configuration errors and failed API calls.
* Support for edge cases in workflows and inputs.
* Automated testing for reliability.

### Core Capabilities

1. **Compliance Scanner**: Checks documents against standards like DPDPA, HIPAA, and GDPR.
2. **Test Case Generator**: Creates structured test cases and exports them as CSV, JSON, or PDF.
3. **Synthetic Data Hub**: Generates realistic, privacy-compliant test data.
4. **AI Co-Pilot**: Provides guidance on compliance and regulatory topics.

### Testing and Quality

* More than 50 automated tests are included.
* Code formatting, linting, and type checking applied.
* Errors are handled gracefully with helpful messages for users.

---

## Troubleshooting

**Problem: `GCP_PROJECT_ID not found`**

* Check that `.env` exists in your project root.
* Confirm that the `GCP_PROJECT_ID` value is correct.

**Problem: `Document AI processing failed`**

* Make sure the `DOCAI_PROCESSOR_ID` in `.env` is correct.
* Verify that the Document AI API is enabled in your Google Cloud project.
* Confirm that your authentication setup is valid.

**Problem: `Vertex AI client not initialized`**

* Check that the project ID and region are correct.
* Make sure the Vertex AI API is enabled.
* Reconfirm your authentication method.

---

## Additional Resources

* [Google Cloud Documentation](https://cloud.google.com/docs)
* [Streamlit Documentation](https://docs.streamlit.io/)
* [Python Documentation](https://docs.python.org/3/)

---

With this guide, even beginners should be able to set up and run the **AI Compliance Co-Pilot** successfully.
