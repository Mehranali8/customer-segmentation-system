# Frontend Application - Customer Segmentation System

This directory houses the frontend React source code and static web assets for the Customer Segmentation System dashboard interface.

---

## 1. Frontend Overview

The frontend layer is a responsive Single Page Application (SPA) designed to convert customer data into visual business analytics. 

By integrating with the FastAPI backend through a customized Axios client wrapper, the application dynamically displays ML-derived customer segments, handles database queries, and executes classification predictions.

---

## 2. Technology Stack

| Technology | Role / Purpose | Selection Rationale |
| :--- | :--- | :--- |
| **React** | Component Model | Core UI rendering library. Renders views based on declarative state properties. |
| **Vite** | Bundling Engine | Development compiler and bundler. Provides sub-second compile and HMR speeds. |
| **React Router** | Page Router | Client-side routing library. Manages page navigations on the client side. |
| **Axios** | Networking | Promise-based HTTP client for calling backend FastAPI REST endpoints. |
| **CSS3** | Styling | Styled layouts using custom CSS variables (no runtime css compiling overhead). |
| **JavaScript (ES6+)** | Logic Layer | Implements page state, data mapping, and validations. |
| **HTML5** | Layout Semantics | Web layout structure. |
| **Context API** | State Management | Shares theme configuration data across layout containers. |

---

## 3. Project Structure

```
frontend/
├── public/                 # Static asset folders directly served by the browser
└── src/                    # Primary React application source
    ├── assets/             # Vector images and brand resource icons
    ├── components/         # Reusable presentation widgets
    │   ├── charts/         # Pure React + CSS bar and distribution charts
    │   ├── customer/       # Customer profiles data grids and lists
    │   └── layout/         # Layout components (Sidebar, Header)
    ├── context/            # React Context Provider containers
    │   └── ThemeContext.jsx# Dark and Light mode theme context provider
    ├── pages/              # Primary route views (Dashboard, Search, Prediction, Details)
    │   ├── CustomerDetails.jsx
    │   ├── CustomerSearch.jsx
    │   ├── Dashboard.jsx
    │   └── Prediction.jsx
    ├── services/           # Backend API integration wrappers
    │   └── api.js          # Shared Axios configuration and interceptors
    ├── App.jsx             # Entrypoint page layouts wrapper and routing config
    ├── index.css           # Global typography definitions, layouts, and variables
    └── main.jsx            # DOM mounting script
```

### Folder Responsibilities
*   **public**: Houses resources served directly without Vite transformation.
*   **src/assets**: Stores graphics used across layouts.
*   **src/components**: Contains isolated widgets (tables, headers, custom charts).
*   **src/context**: Stores context providers (such as the dark/light mode context).
*   **src/pages**: Contains primary page views mounted via React Router.
*   **src/services**: Configures the Axios client wrapper.

---

## 4. Installation

### Prerequisites
*   **Node.js**: Version 18.0 or higher is required.
*   **npm**: Version 9.0 or higher is required.

To install dependencies, navigate to the `frontend/` directory and execute:
```bash
npm install
```

---

## 5. Running the Frontend

Start the local development server:
```bash
npm run dev
```

### Expected Terminal Output
```
  VITE v8.1.4  ready in 184 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

Open your browser and navigate to the default URL:
```
http://localhost:5173/
```

---

## 6. Routing

The application uses React Router DOM to manage client-side routes:

*   **`/`**: Dashboard Page. Renders statistical summaries and distribution charts.
*   **`/search`**: Customer Search Page. Queries individual customer profiles.
*   **`/prediction`**: Prediction Page. Performs real-time customer segment predictions.
*   **`/customer-details`**: Customer Details Page. Displays detailed profiles and dynamic relationship statuses.

Users navigate between routes using NavLinks in the `Sidebar` component. The `Header` component updates page titles and breadcrumbs dynamically based on the active path.

---

## 7. Component Documentation

*   **Sidebar**: Renders navigation links, applying an `.active` class to highlight the selected page view.
*   **Header**: Placed at the top right of the dashboard layout. Renders breadcrumbs, search placeholders, notifications, and the theme toggle button.
*   **Dashboard**: The primary widgets page, rendering summaries and distribution grids.
*   **Summary Cards**: Renders key metric values inside glassmorphism panels.
*   **Charts**: Horizontal React + CSS percentage bars representing customer segment distributions.
*   **Customer Table**: A responsive data grid showing customer profiles with sticky headers.
*   **Prediction Form**: Forms used to enter RFM values for model inference.
*   **Customer Search Form**: Implements lookup fields, validation checks, and search submit buttons.
*   **Customer Details Card**: Renders customer profile information, behavior analyses, and recommendations.
*   **Theme Toggle**: Switched via click actions in the Header, updating root document elements.
*   **Loading Components**: Renders a spinning loader wheel for active API requests.
*   **Error Components**: Displays connection failure cards and retry buttons.

---

## 8. Theme System

The theme system supports Dark and Light modes:
*   **Theme Provider**: The `ThemeContext` provider initializes and updates the active theme.
*   **HTML Attribute Binding**: Toggling the theme applies the `data-theme="dark"` or `data-theme="light"` attribute to the root document element.
*   **CSS Variables**: All styled layouts reference variables defined in `index.css` (e.g. `--bg`, `--card-bg`, `--text`, `--border`, `--accent`).
*   **Local Storage**: Saves the active theme selection in `localStorage` and restores it on page refresh.

---

## 9. API Integration

API communication is centralized under `src/services/api.js`:
*   **Base URL**: Configured to `http://127.0.0.1:8000` (FastAPI backend).
*   **Request Interceptor**: Inserts authorization tokens (`Authorization: Bearer <token>`) from `localStorage` to support future login security.
*   **Response Interceptor**: Intercepts HTTP errors, formatting error details (`{ message, status, data }`) for clean UI handling.

---

## 10. Responsive Design

*   **Desktop Layout**: Renders sidebars on the left and page views inside container frames on the right.
*   **Tablet Layout**: Grid containers collapse to single columns, and margins adjust.
*   **Mobile Layout**: Form elements stack vertically, tables overflow horizontally with scroll bar access, and navigation buttons expand to full width.

---

## 11. Error Handling

*   **Connection Errors**: Displays a warning card with a Retry button if the backend server is offline.
*   **Validation Errors**: Displays clear validation warnings (e.g. if the user enters negative values in forms).
*   **404 Responses**: Gracefully catches missing resource errors and displays a clean status message instead of throwing console errors.

---

## 12. Development Workflow

Follow this workflow when modifying the frontend application:
1.  **Run Dev Servers**: Ensure the FastAPI server is running on port `8000` and start the Vite dev server (`npm run dev`).
2.  **Add Reusable Styles**: Add styles inside `src/index.css` using custom CSS variables to support Dark/Light modes.
3.  **Compile Bundles**: Run `npm run build` to verify that modifications build successfully without compilation errors.

---

## 13. Future Frontend Improvements

*   **JWT User Authentication**: Implement login views and route guard boundaries.
*   **Interactive Visualizations**: Use visualization libraries (such as Recharts) to render interactive graphs.
*   **WebSocket Integration**: Stream transactional records in real time.
*   **Internationalization**: Add translations for multi-language support.
*   **Progressive Web App (PWA)**: Implement service workers to enable offline caching.

---

## 14. Contributing

Contributions are welcome! Follow these steps to contribute:
1.  Fork the repository.
2.  Create a feature branch: `git checkout -b feature/your-feature`.
3.  Commit your changes: `git commit -m 'Add your feature'`.
4.  Push to the branch: `git push origin feature/your-feature`.
5.  Open a Pull Request.

---

## 15. Frontend Summary

The frontend application provides a responsive dashboard interface to interact with customer database records and predict segments. Built using React 18 and Vite, it uses a custom Axios client layer, client-side routing, and a dynamic theme system to deliver a premium user experience.
