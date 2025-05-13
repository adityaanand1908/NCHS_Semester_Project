import streamlit as st
import pandas as pd

# MUST BE FIRST Streamlit COMMAND
st.set_page_config(page_title="NCS Hope Foundation Dashboard", layout="wide")

# Load the Structured DataSet
data_frame = pd.read_csv("datasets/NCSH_Foundation_Dataset_Cleaned.csv", parse_dates=["Grant_Req_Date"])

# Sidebar navigation
page = st.sidebar.selectbox("Dashboard Pages",
                                [
                                    "Ready for Review",
                                    "Support by Demographics",
                                    "Time to Support",
                                    "Grant Usage & Budgeting",
                                    "Annual Impact Summary"
                                ]
                            )

# PAGE NAME = Ready for Review
if page == "Ready for Review":
    st.title("Applications: Ready for Review")
    signed_filter = st.selectbox("STATUS: Application Signed?", ["all", "yes", "no"])

    review_data_frame = data_frame[data_frame["Request_Status"] == "approved"]
    if signed_filter != "all":
        review_data_frame = review_data_frame[review_data_frame["Application_Signed?"] == signed_filter]

    st.dataframe(review_data_frame)

# PAGE NAME = Support by Demographics
elif page == "Support by Demographics":
    st.title("Support Distribution by Demographics")
    demo_option = st.selectbox("Group By", ["Pt_City", "Pt_State", "Gender", "Race", "Total_Household_Gross_Monthly_Income", "Insurance_Type", "App_Year", "Household_Size"])

    if demo_option in data_frame.columns:
        summary = data_frame.groupby(demo_option)["Amount"].sum().reset_index()
        st.bar_chart(summary.set_index(demo_option))


# PAGE NAME = Time to Support
elif page == "Time to Support":
    st.title("Time Between Request and Support Sent")

    if "Days_To_Support" in data_frame.columns:
        st.metric("Average Days to Support", round(data_frame["Days_To_Support"].mean(), 2))
        st.bar_chart(data_frame["Days_To_Support"].value_counts().sort_index())
        st.write(data_frame[["Grant_Req_Date", "Support_Sent_Date", "Days_To_Support"]].head(10))
    else:
        st.warning("Support sent date is not available or needs to be computed.")

# PAGE NAME = Grant Usage & Budgeting
elif page == "Grant Usage & Budgeting":
    st.title("Grant Usage and Budgeting")
    data_frame["Unused_Amount"] = data_frame["Remaining_Balance"]

    unused_by_year = data_frame.groupby("App_Year")["Unused_Amount"].sum().reset_index()
    avg_by_type = data_frame.groupby("Type_of_Assistance_(CLASS)")["Amount"].mean().reset_index()

    st.subheader("Unused Grant Amounts by Application Year")
    st.bar_chart(unused_by_year.set_index("App_Year"))

    st.subheader("Average Support Amount by Assistance Type")
    st.dataframe(avg_by_type)

# PAGE NAME = Annual Impact Summary
elif page == "Annual Impact Summary":
    st.title("Annual Impact Summary")

    yearly_stats = data_frame.groupby("App_Year").agg(
        Total_Applications=("Patient_ID#", "unique"),
        Total_Support_Amount=("Amount", "sum"),
        Avg_Grant_Per_Patient=("Amount", "mean")
    ).reset_index()

    st.write("Impact Summary by Year")
    st.dataframe(yearly_stats)
