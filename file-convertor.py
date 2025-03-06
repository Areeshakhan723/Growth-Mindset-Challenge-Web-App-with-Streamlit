import pandas as pd  # Import pandas for data processing
import streamlit as st  # Import streamlit for creating the web interface
from io import BytesIO  # Import BytesIO to handle file downloads in memory
import os  # Import os module to handle file operations such as extracting file extensions


# Configure Streamlit page settings
st.set_page_config(page_title="Data sweeper", page_icon="💿", layout="wide")

# Display page title and description 
st.title("💿Data sweeper")
st.write("Transform your files between csv or Excel formet, with built-in data cleaning and visuliaztion!")

# File uploader allows users to upload multiple CSV or Excel files
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Process each uploaded file
if uploaded_files :
    for file in uploaded_files :

    # Read the file based on its extension
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")  # Specify the engine
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue
        
        # Display info about the file
        st.write("File name: {file.name}")
        st.write(f"file size: {file.size/10}")

     # Display file name and preview
        st.write("🔎Preview the Head of the Dataframe:")
        st.dataframe(df.head())

        # options for Data cleaning
        st.subheader("🛠Data Cleaning Options:")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Dupilicate from {file.name}"):
                  df = df.drop_duplicates()
                  st.write("Duplicate remove")
            with col2:
                if st.button(f"File Missing Value for {file.name}"):
                    numric_cols = df.select_dtypes(include=["number"]).columns
                    df[numric_cols] = df[numric_cols].fillna(df[numric_cols].mean()) 
                    st.write("Missing value have been filled") 
      
        # Multi-select dropdown to choose specific columns to keep
        st.subheader("Select Columns to Convert")
        selected_colums = st.multiselect(f"Choose coloums - {file.name}", df.columns, default=df.columns)
        df = df[selected_colums]
        
        # Create some Visualizations
        st.subheader("📊 Data Visualizations")

        if not df.select_dtypes(include="number").empty:
            if st.checkbox(f"Show Visualizations for {file.name}"):
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])
        else:
            st.warning(f"No numeric data available for visualization in {file.name}.")

        # Convert the file -> csv or excel
        st.subheader("🔄Convertion Options")
        convertions_types = st.radio(f"Convert {file.name} to:",["CSV", "Excel"], key=file.name)
        if st.button(f"covert {file.name}"):
            output = BytesIO()
            
            if convertions_types == "CSV":
                df.to_csv(output, index=False)
                new_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
                
            elif convertions_types == "Excel":
                df.to_excel(output, index=False)
                new_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd:openxmlformats-officedocument.spreadsheetml.sheet"
    
            output.seek(0)

            st.download_button(
                label=f"⬇️Download {file.name} as {convertions_types}",
                file_name=new_name,
                mime=mime_type,
                data=output,
            )
            # Prepare file for download
            st.success("🎉All File processed!")
    