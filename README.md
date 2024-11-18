# Iterative AI Web Scraping Tool

This project is an **Iterative AI Web Scraping Tool** that allows you to upload CSV files, select a column, and analyze data using iterative AI scraping with error handling and refined queries. The tool leverages the SERP API to scrape search results and processes them using AI for further analysis. It retries failed queries with refined versions and continues to gather data until it succeeds or reaches the maximum retry attempts.

## Features

- Upload a CSV file with data. 
- Select a column and dynamically create queries based on it.
- Perform web searches using the **SERP API**.
- Process and refine failed queries automatically.
- Analyze search results using AI-powered prompts.
- View and download the results in CSV format.

## Requirements

- Python 3.x
- Streamlit
- pandas
- Groq ai api
- `serpapi` for Google search scraping
- `.env` file for API key management

## Create a Virtual Environment
Navigate to the project directory where you want to create the virtual environment.
Run the following command to create a virtual environment:
```bash
python -m venv env
```
This will create a new directory named env inside your project folder, which will contain the isolated environment for your project.

## Activate the Virtual Environment
To activate the virtual environment, follow the instructions below based on your operating system:

On Windows:
```bash
.\env\Scripts\activate
```
On macOS/Linux:
```bash
source env/bin/activate
```

### Python Packages

You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Create a .env File

Create a .env file in the root directory of the project and add your API keys.

- `SERPAPI_KEY=your_serpapi_key_here`
- `GROQAI_KEY=your_groqapi_key_here`

## Running the Application

Once the dependencies are installed and the .env file is configured, you can run the application.

Open a terminal or command prompt.
Navigate to your project directory where the main.py file is located.
Run the Streamlit application with the following command:
```bash
streamlit run main.py
```

## Interact with the App
Upload a CSV file containing the data you want to analyze.
Select a column of interest that will be used to generate search queries.
Provide an AI prompt for analysis.
The app will automatically perform web searches, process the results, and retry failed queries with refined versions if needed.
You can view the results directly in the app and download them in CSV format once the process is complete.

## Error Handling and Retry Logic
If a search query fails or returns no results, the system will automatically refine the query and retry it up to 3 times (default behavior).
If no results are found after retries, the query is skipped and a warning message is displayed.




