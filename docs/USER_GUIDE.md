# End-User Installation & Operation Guide - Customer Segmentation System

This document provides step-by-step instructions to install, run, and use the Customer Segmentation System from an end-user and administrator perspective.

---

## 1. Introduction

### Purpose of the Project
The Customer Segmentation System is an analytical software suite designed to group a retail customer base into discrete business segments based on purchasing behaviors. It uses a K-Means clustering algorithm trained on Recency, Frequency, and Monetary (RFM) metrics.

### Intended Users
*   **Marketing Managers**: Target campaigns to specific customer groups (e.g. VIP rewards or reactivation discount offers).
*   **Business Analysts**: Analyze segment distributions and transaction trends.
*   **System Administrators**: Monitor system operations, manage database assets, and maintain analytical models.

### Problems It Solves
*   **High Churn Rates**: Identifies "At Risk" customers so marketing teams can deploy retention campaigns.
*   **Low Conversion Rates**: Replaces generic marketing with targeted campaigns designed for specific segments.
*   **Customer Relationship Management (CRM) Gaps**: Translates transactional datasets into actionable buyer classifications.

---

## 2. System Requirements

| Parameter | Minimum Requirement | Recommended Specification |
| :--- | :--- | :--- |
| **Operating System** | Windows 10 / macOS 11 / Ubuntu 20.04 | Windows 11 / macOS 13+ |
| **Python Version** | Python 3.9 | Python 3.10+ |
| **Node.js** | Node.js 18.0 | Node.js 20.0+ |
| **npm** | npm 9.0 | npm 10.0+ |
| **Git** | Git 2.30+ | Git 2.40+ |
| **RAM** | 8 GB | 16 GB |
| **Disk Space** | 2 GB free space | 5 GB free space (SSD preferred) |
| **Supported Browsers** | Google Chrome / Mozilla Firefox / Safari | Google Chrome / Microsoft Edge (Chromium) |

---

## 3. Project Structure

```
customer-segmentation/
├── backend/                # Python backend API application files
│   ├── app/                # Main FastAPI execution scripts and controllers
│   └── requirements.txt    # Python package dependencies manifest
├── frontend/               # React + Vite frontend source code
│   └── package.json        # Frontend Node dependencies manifest
├── datasets/               # CSV database files
├── models/                 # Serialized K-Means clustering models
├── notebooks/              # Data science exploration files
├── screenshots/            # Visual image references
├── tests/                  # Backend pytest script directories
└── docs/                   # System architectural and markdown documentation files
```

---

## 4. Installation Guide

Follow these steps to clone the repository and install all dependencies:

### Step 1: Clone the Repository
Open a terminal and execute:
```bash
git clone https://github.com/ML-Projects/customer-segmentation.git
cd customer-segmentation
```

### Step 2: Create a Python Virtual Environment
Navigate to the root project directory and create a virtual environment to isolate the Python dependencies:
*   **Windows (PowerShell)**:
    ```powershell
    python -m venv .venv
    ```
*   **macOS / Linux**:
    ```bash
    python3 -m venv .venv
    ```

### Step 3: Activate the Virtual Environment
Activate the environment to execute packages within the container boundaries:
*   **Windows (PowerShell)**:
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
*   **macOS / Linux**:
    ```bash
    source .venv/bin/activate
    ```

### Step 4: Install Backend Dependencies
With the virtual environment active, navigate to the `backend` folder and run the installation script:
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### Step 5: Install Frontend Dependencies
Navigate to the `frontend` folder and install the Node modules:
```bash
cd frontend
npm install
cd ..
```

---

## 5. Running the Backend

Follow these steps to run the FastAPI backend server:

### Step 1: Navigate to Backend
Navigate to the backend directory and activate the virtual environment if it is not already active:
```bash
cd backend
```

### Step 2: Start the FastAPI Server
Run the application using Uvicorn:
```bash
uvicorn app.main:app --reload --port 8000
```

### Expected Console Output
```
INFO:     Will watch for changes in these directories: ['d:\\ML-Projects\\customer-segmentation\\backend']
INFO:     Uvicorn server running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
Customer Segmentation Model Loaded Successfully
Feature StandardScaler initialized successfully
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### How to Verify the Backend is Online
*   **Health Check**: Open `http://127.0.0.1:8000/health` in your browser. You should receive:
    ```json
    { "backend": "running", "model": "loaded", "version": "1.0.0" }
    ```
*   **Swagger API Playground**: Navigate to `http://127.0.0.1:8000/docs` to access the interactive API playground.

---

## 6. Running the Frontend

Follow these steps to run the React dev server:

### Step 1: Navigate to Frontend
Open a new terminal window, navigate to the frontend directory, and start the development server:
```bash
cd frontend
npm run dev
```

### Expected Console Output
```
  VITE v8.1.4  ready in 184 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Step 2: Open the Web UI
Open your browser and navigate to the local address output by Vite:
```
http://localhost:5173/
```

---

## 7. Using the Dashboard

The dashboard is the landing page of the application, displaying key metrics of the customer base:

*   **Welcome Banner**: Confirms the operational state of the machine learning pipeline.
*   **Summary Cards**:
    *   **Total Customers**: Displays the total unique customer records parsed.
    *   **Total Segments**: The number of clusters defined by the model ($k=4$).
    *   **Average Recency**: Average days elapsed since the customer's last purchase.
    *   **Average Monetary Value**: Average lifetime customer spend in GBP (£).
*   **Model Insights & Distributions**: Renders percentage bar allocations representing customer segments across clusters.
*   **Recent Customer Profiles**: A responsive data table showing customer IDs, segments, transaction values, and relationship statuses.
*   **Model Status Widget**: Displays backend metadata, including algorithm configurations and dataset scales.

---

## 8. Using Customer Search

Access the lookup tool by clicking **Customer Search** in the sidebar:

*   **Searching**: Input a target Customer ID (e.g. `17850`) into the lookup field and click **Search**.
*   **Input Validation**: The lookup engine enforces formatting rules. If you submit alphabetic characters, decimals, or negative numbers, it displays a validation warning without sending the request.
*   **Success Results**: Displays the customer's segment category, transaction metrics, and cluster ID.
*   **Error Handling**: If a Customer ID is not present in the database, the page displays a clean `"No customer found matching the specified ID."` warning card.

---

## 9. Using Customer Details

Access details by clicking **Customer Details** in the sidebar:

*   **Automatic Load**: On mount, the page automatically retrieves the detailed profile for VIP customer `#14911`.
*   **Profile Lookup**: Input a Customer ID into the selector panel and click **Load Profile** to update the details.
*   **Demographic Metrics Card**: Displays K-Means cluster numbers, segment categories, recency scores, frequency records, monetary values, and calculated customer statuses.
*   **Customer Status Badge**: Displays dynamic, color-coded tags based on recency:
    *   `Active` (Recency $\le$ 30 days) - Green badge
    *   `Recent` (31 - 90 days) - Soft green badge
    *   `Inactive` (91 - 180 days) - Amber badge
    *   `Dormant` (181+ days) - Red badge
*   **Behavior Summary**: Lists customer purchasing behavior descriptors based on their segment.
*   **Recommended Actions**: Suggests marketing strategies matching the customer's segment classification (e.g. VIP loyalty rewards or reactivation discount offers).

---

## 10. Using Prediction

Access the prediction page by clicking **Prediction** in the sidebar to classify new customer inputs:

*   **Form Parameters**:
    *   **Recency**: Input the days elapsed since the customer's last transaction (e.g. `15`).
    *   **Frequency**: Input the customer's unique invoice count (e.g. `25`).
    *   **Monetary Value**: Input the customer's total spend in GBP (£) (e.g. `8500`).
*   **Execution**: Click **Predict Segment**. The button disables, the input metrics are sent to the backend, and the segment classification is displayed.
*   **Outputs**:
    *   **Predicted Segment**: Displays the calculated business segment name.
    *   **Model Centroid Cluster**: Displays the assigned K-Means cluster ID.
    *   **Strategic Recommendation**: Suggests target marketing campaigns matching the predicted segment.

---

## 11. Error Messages

Common error messages and their meanings:

*   **"Could not connect to the analytical engine API..."**
    *   *Meaning*: The React client cannot reach the FastAPI backend server.
    *   *Remedy*: Ensure that the backend server is running on `http://127.0.0.1:8000`.
*   **"No customer found matching the specified ID."**
    *   *Meaning*: The requested Customer ID does not exist in the database datasets.
    *   *Remedy*: Verify that you entered the ID correctly.
*   **"Please enter a valid positive integer..."**
    *   *Meaning*: The entered Customer ID does not match the integer requirements.
    *   *Remedy*: Input a positive integer (no text, decimals, or negative values).
*   **"API Error: ensure this value is greater than or equal to 0"**
    *   *Meaning*: Pydantic validation caught negative values in form input.
    *   *Remedy*: Ensure all form parameters are positive.

---

## 12. Troubleshooting

| Symptom | Probable Cause | Action |
| :--- | :--- | :--- |
| **Backend fails to start** | Port 8000 is occupied by another process. | Run the server on a different port: `uvicorn app.main:app --port 8001`. Update the frontend API configuration if you change the port. |
| **"ModuleNotFoundError: No module named 'fastapi'"** | Python virtual environment is not active. | Activate the virtual environment: `.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (macOS/Linux). |
| **Model Loader throws ModelNotFound exceptions** | Trained model joblib binary is missing. | Navigate to `backend/` and run `python app/save_model.py` to serialize the reference model object to disk. |
| **Vite fails to run npm command** | Node modules are not installed in the frontend directory. | Navigate to `frontend/` and run `npm install` to download dependencies. |
| **Console log CORS errors** | FastAPI origin policies block client requests. | Ensure the frontend port matches allowed origins in `backend/app/main.py`. |
| **Prediction button is disabled** | Input fields are empty, invalid, or query is active. | Complete the Recency, Frequency, and Monetary fields using positive values. |

---

## 13. Frequently Asked Questions

#### Q1: Why is the Prediction option in the sidebar disabled or failing?
Verify that the machine learning model binary `customer_segmentation_model.joblib` exists inside the `models/` directory. If it is missing, run `python app/save_model.py` to create the serialization file on disk.

#### Q2: Can I run this system without Node.js installed?
No. The frontend requires Node.js to run the Vite compilation and development environment.

#### Q3: Can I run this system without Python?
No. The backend API is written in Python using the FastAPI framework.

#### Q4: Why is the dashboard showing a connection error card?
The FastAPI backend server is offline or running on a port other than `8000`. Ensure that Uvicorn is active in your terminal.

#### Q5: Can I upload another dataset to update customer records?
The current version reads data from local files (`customer_rfm.csv` and `customer_segments_labeled.csv`). Future updates will include a dataset upload feature.

#### Q6: How does the system determine the customer status (Active, Recent, etc.)?
The status is calculated dynamically based on unscaled Recency: $\le$ 30 days is Active, 31 - 90 days is Recent, 91 - 180 days is Inactive, and 181+ days is Dormant.

#### Q7: Can I retrain the clustering model with new data?
Yes. You can retrain the model by running the model training script `python app/model_training.py` with updated datasets.

#### Q8: Does the system store user login sessions?
No. The current development build is a public administration console and does not require authentication.

#### Q9: What browser is recommended?
Google Chrome, Mozilla Firefox, or Safari are recommended.

#### Q10: How can I change the currency symbol?
The system references GBP (£). To update this, modify the currency formatting in the React component files.

---

## 14. Best Practices

*   **Input Validations**: Ensure form values are positive floats or integers to prevent validation errors.
*   **Run Server Decoupled**: Run the backend FastAPI and frontend Vite services in separate terminal windows.
*   **Environment Variables**: Use `.env` files to configure backend URLs and port mappings.

---

## 15. Future Enhancements

*   **Secure Authentication**: User sign-in flows using JWT.
*   **Database Integration**: Connect relational databases (such as PostgreSQL) in place of local CSV files.
*   **CSV Upload Interface**: Drag-and-drop CSV uploads to update customer datasets.
*   **Dynamic Visualizations**: Interactive graphs using charting libraries.
*   **Automatic Retraining Pipelines**: Automate model retraining as new customer transactions are recorded.

---

## 16. User Guide Summary

The Customer Segmentation System consists of a FastAPI backend and a React frontend. To run the application, launch the FastAPI server using Uvicorn and run the React frontend using Vite. Once running, you can explore customer details, search for specific profiles, and classify new inputs using real-time predictions.
