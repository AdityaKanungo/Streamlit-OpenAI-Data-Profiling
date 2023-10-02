from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import base64

import warnings
warnings.filterwarnings('ignore')

# Initialization
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']
llm = OpenAI(api_token=API_KEY)
pandas_ai = PandasAI(llm)

st.title("Prompt-driven analysis with PandasAI")
uploaded_file = st.file_uploader("Upload a CSV file for analysis", type=['csv'])

if uploaded_file is not None:
    # Reading file and basic setup
    df = pd.read_csv(uploaded_file)
    st.write(df.head(3))
    filename = "data_profile_" + uploaded_file.name.split('.')[0] + ".xlsx"

    # Categorize columns
    num_columns = df.select_dtypes(['float64', 'int64']).columns.tolist()
    cat_columns = df.select_dtypes(['object']).columns.tolist()
    date_columns = df.select_dtypes(['datetime']).columns.tolist()

    # Exclude columns that are likely unique identifiers
    likely_id_cols = [col for col in df.columns if df[col].nunique() == df.shape[0]]
    for col in likely_id_cols:
        if col in num_columns:
            num_columns.remove(col)

    # Generating the Excel file for download
    with pd.ExcelWriter(filename) as writer:
        df.describe().to_excel(writer, sheet_name="Stats")
        summary_df = pd.DataFrame({
            'Feature': df.columns,
            'Data Type': [df[col].dtype for col in df.columns],
            'Number of Unique Values': [df[col].nunique() for col in df.columns],
            'Sample Value': [df[col].iloc[0] for col in df.columns],
            'Missing Values': [df[col].isnull().sum() for col in df.columns]
        })
        summary_df.to_excel(writer, sheet_name="Summary")
        
        missing_counts = df.isnull().sum()
        not_missing_counts = df.shape[0] - missing_counts
        missing_percentage = (missing_counts / df.shape[0]) * 100
        missing_df = pd.DataFrame({
            'Column': missing_counts.index,
            'Missing Values': missing_counts.values,
            'Not Missing Values': not_missing_counts.values,
            'Percentage Missing': missing_percentage.values
        })
        missing_df.to_excel(writer, sheet_name="Null Values")

    with open(filename, "rb") as f:
        bytes_data = f.read()
        st.download_button(label="Download Data Profile as Excel", data=bytes_data, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Tabs using new structure
    tab_prompt, tab_stats, tab_summary, tab_null, tab_eda = st.tabs(["Prompt Analysis", "Stats", "Summary", "Null Values", "EDA"])

    with tab_prompt:
        prompt = st.text_area("Enter your prompt:")
        if st.button("Generate"):
            if prompt:
                with st.spinner("Generating response..."):
                    st.write(pandas_ai.run(df, prompt))
            else:
                st.warning("Please enter a prompt.")

    with tab_stats:
        st.write(df.describe())

    with tab_summary:
        st.table(summary_df)

    with tab_null:
        st.write(missing_df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(missing_df['Column'], missing_df['Not Missing Values'], label='Not Missing', color='blue')
        ax.bar(missing_df['Column'], missing_df['Missing Values'], bottom=missing_df['Not Missing Values'], label='Missing', color='red')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Count")
        plt.title("Proportion of Missing Values in Each Column")
        ax.legend()
        st.pyplot(fig)

    with tab_eda:
        # Histograms for numerical columns
        for col in num_columns:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

        # Bar charts for categorical columns with limited unique values
        for col in cat_columns:
            if df[col].nunique() <= 20:  # Display top 20 categories
                fig, ax = plt.subplots()
                sns.countplot(y=df[col], ax=ax)
                st.pyplot(fig)

        # Grouped scatter plots if two numerical columns and one categorical column exist
        if len(num_columns) == 2 and len(cat_columns) == 1:
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[num_columns[0]], y=df[num_columns[1]], hue=df[cat_columns[0]], ax=ax)
            st.pyplot(fig)

        # Time series plots for numerical columns with date columns
        for date_col in date_columns:
            for num_col in num_columns:
                fig, ax = plt.subplots()
                sns.lineplot(x=df[date_col], y=df[num_col], ax=ax)
                st.pyplot(fig)

        # Correlation heatmap for numerical columns
        if len(num_columns) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
