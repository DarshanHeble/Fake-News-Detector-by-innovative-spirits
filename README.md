# **Fake-News-Detection-testing**

## **Workflow**

1. **Data transfer from frontend to backend**

   - When sending data to backend for verification of news data, a certain type of data need to be passed.

   ```ts
   type InputNewsType = {
     category: "text" | "url";
     content: string;
   };
   ```

2. **Model Input for prediction**

   - The model takes a news claim inputted by the user(It should be headline) and a body of text(Typically the description of fetched news articles)

   - This can be cannot be changed since the datasets is specifically used for that purpose.

3. **Data transfer from backend to frontend**

   - When sending data to backend for verification of news data, a certain type of data need to be passed.

   ```ts
   type OutputNewsType = {
     label: "real" | "fake";
   };
   ```

## **Requirements**

**To run this project, you'll need the following:**

1. **Node.js and npm (or yarn):**

   - Download and install the latest version from the official Node.js website: [https://nodejs.org/](https://nodejs.org/)
   - **Verification:**
     Open your terminal or command prompt and type the following commands. The output should indicate the installed versions:

     ```powershell
      node -v
      npm -v
     ```

2. **Python and pip:**
   - Download and install Python from [https://www.python.org/](https://www.python.org/)
   - Install `pip`, the Python package installer, which is usually included with Python.

## **Project Setup**

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/DarshanHeble/Fake-News-Detector-by-innovative-spirits.git
   ```

2. **Open the Project in Your IDE:**
   - Open the cloned repository in your preferred IDE (e.g., Visual Studio Code, PyCharm).

## **Running the Backend**

**Navigate to the `backend` directory within your IDE terminal.**

1. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server:**
   ```powershell
   uvicorn app.main:app --reload
   ```
   This will start the server on `http://127.0.0.1:8000` by default.

## **Running the Frontend**

**Navigate to the `frontend` directory within your IDE terminal.**

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```
   This will start the development server and open your default browser.
