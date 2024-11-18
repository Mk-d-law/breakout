import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from search import serp_search
from analyse import process_scraped_data

def main():
    st.title("Iterative Data Analysis Tool")
    st.write("Upload a CSV file, select a column, and analyze data using iterative AI scraping.")

    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview", df.head())

        column = st.selectbox("Select a column to analyze", df.columns)
        prompt = st.text_area("Enter your AI prompt (e.g., 'Find email ID of {company}')")

        if st.button("Run Analysis"):
            results = []
            search_history = []  # Track all search queries
            previous_info = ""  # Store partial useful information
            total_tokens_used = 0  # Initialize total tokens used

            for index, row in df.iterrows():
                user_input = prompt.replace(f"{{{column}}}", str(row[column]))

                search_query = user_input  # Initial search query

                # Skip if the search query has already been made
                if search_query in search_history:
                    continue

                search_history.append(search_query)
                scraped_results = serp_search(search_query)

                # AI Processing for Results
                ai_prompt = (
                    f"You are an intelligent assistant analyzing web search results. "
                    f"Given the scraped data:\n\n{scraped_results}\n\n"
                    f"The user query is: `{user_input}`. "
                    f"Use the previous info for context: `{previous_info}`. "
                    "If you can find the information, respond in the format: `found: \"result\"`. "
                    "If the data is insufficient, suggest a refined query in the format: "
                    "`notfound: \"refined search query\", info: \"partial useful info\"`. "
                    "If Google Dorking can improve results for this request, provide a dork query in the format: "
                    "`notfound: \"dork: refined search query\", info: \"partial useful info\"`."
                    "Dont conclude a result if you dont satisfy with available result, go to search again by giving a refined search query"
                    "Make the result short and precise to what the user query is and don't give exact words from information. You process information and generate the best result."
                    "Do not include any additional context, explanations, or irrelevant information in your response and strictly follow the formats."
                )

                analysis = process_scraped_data(scraped_results, ai_prompt, previous_info, search_history)

                # Handle AI Response for Refinement or Dorking
                while analysis.startswith("notfound:"):
                    parts = analysis.split("info:")
                    refined_query = parts[0].split("notfound:")[1].strip()
                    partial_info = parts[1].strip() if len(parts) > 1 else ""

                    if refined_query.startswith("dork:"):
                        refined_query = refined_query.replace("dork:", "").strip()

                    search_history.append(refined_query)
                    refined_results = serp_search(refined_query)

                    # Add partial info to the AI prompt
                    previous_info += f"\nFrom search `{refined_query}`: {partial_info}"

                    refined_ai_prompt = (
                        f"You are an intelligent assistant analyzing web search results. "
                        f"Given the refined scraped data:\n\n{refined_results}\n\n"
                        f"The user query is: `{user_input}`. "
                        f"Use the previous info for context: `{previous_info}`. "
                        "If you can find the information, respond in the format: `found: \"result\"`. "
                        "If the data is insufficient, suggest a further refined query in the format: "
                        "`notfound: \"refined search query\", info: \"partial useful info\"`. "
                        "If Google Dorking can improve results for this request, provide a dork query in the format: "
                        "`notfound: \"dork: refined search query\", info: \"partial useful info\"`."
                        "Dont conclude a result if you dont satisfy with available result, go to search again by giving a refined search query"
                        "Make the result short and precise to what the user query is and don't give exact words from information. You process information and generate the best result."
                        "Do not include any additional context, explanations, or irrelevant information in your response and strictly follow the formats."
                    )

                    analysis = process_scraped_data(refined_results, refined_ai_prompt, previous_info, search_history)

                # Update the total tokens used for tracking
                if isinstance(analysis, list):
                    analysis = " ".join(analysis)  # Join list items into a string

                total_tokens_used += len(analysis.split())  # Token count is based on word splitting

                results.append({"Input": row[column], "Output": analysis})

            # Plotly Interactive Line Chart for Search Queries Over Time
            fig_search_queries = go.Figure()
            fig_search_queries.add_trace(go.Scatter(x=list(range(len(search_history))), y=[len(search_history)] * len(search_history), mode='lines+markers', name="Search Queries", line=dict(color='skyblue', width=2), marker=dict(size=6)))
            fig_search_queries.update_layout(title="Search Queries Over Time", xaxis_title="Iterations", yaxis_title="Count")

            st.plotly_chart(fig_search_queries)

            # Plotly Pie Chart for Tokens Used
            fig_tokens_used = go.Figure(go.Pie(labels=["Tokens Used"], values=[total_tokens_used], marker=dict(colors=["orange"])))
            fig_tokens_used.update_layout(title="Total Tokens Used")

            st.plotly_chart(fig_tokens_used)

            # Save Results
            result_df = pd.DataFrame(results)
            st.write("### Final Results", result_df)
            result_df.to_csv("output.csv", index=False)
            st.download_button("Download Results", data=result_df.to_csv(index=False), file_name="output.csv")

if __name__ == "__main__":
    main()
