
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="GlobalScale.AI LeadCleaner",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)
st.title("📈 GlobalScale.AI LeadCleaner")
st.markdown("Upload your messy lead file (CSV, XLS, or XLSX). We'll clean it into a unified Contact + Opportunity format — ready to import into GlobalScale.AI CRM.")

uploaded_file = st.file_uploader("Upload your lead file", type=["csv", "xls", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, sheet_name=0)

        st.subheader("Raw Preview")
        st.dataframe(df.head())

        first_name = df.columns[df.columns.str.contains("first", case=False)].tolist()
        last_name = df.columns[df.columns.str.contains("last", case=False)].tolist()
        phone = df.columns[df.columns.str.contains("phone", case=False)].tolist()
        email = df.columns[df.columns.str.contains("email", case=False)].tolist()
        company = df.columns[df.columns.str.contains("company|address", case=False)].tolist()

        clean_df = pd.DataFrame()
        clean_df["First Name"] = df[first_name[0]] if first_name else "John"
        clean_df["Last Name"] = df[last_name[0]] if last_name else "Doe"
        clean_df["Phone"] = df[phone[0]] if phone else ""
        clean_df["Email"] = (
            df[email[0]] if email else
            clean_df["First Name"].str.lower().fillna("user") + "." +
            clean_df["Last Name"].str.lower().fillna("lead") + "@globalscale-import.com"
        )
        clean_df["Role"] = ""
        clean_df["Lifecycle Stage"] = "Lead"
        clean_df["Contact Source"] = "Lead File Upload"
        clean_df["Company Name"] = df[company[0]] if company else "Unknown Company"

        clean_df["Opportunity Name"] = clean_df["First Name"] + " " + clean_df["Last Name"] + " – GlobalScale Deal"
        clean_df["Contact Email"] = clean_df["Email"]
        clean_df["Pipeline Name"] = "Opener → Setter → Closer"
        clean_df["Stage"] = "New Lead (Inbound/Outbound)"
        clean_df["Estimated Value"] = [random.randint(2000, 15000) for _ in range(len(clean_df))]
        clean_df["Product/Service"] = "AI Strategy Call"
        clean_df["Opportunity Source"] = "Lead File Upload"
        clean_df["Opportunity Owner"] = "Setter"
        clean_df["Status"] = "Open"
        clean_df["Lost Reason"] = ""
        clean_df["Next Action Date"] = [
            (datetime.today() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            for _ in range(len(clean_df))
        ]

        st.subheader("✅ Cleaned & Merged Output")
        st.dataframe(clean_df.head())

        csv = clean_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name="GlobalScaleAI_Lead_Cleaned.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"❌ An error occurred while processing your file: {e}")
