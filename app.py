import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_pickle("Assets/Patient_data.pkl")

st.title("Hospital Readmission Analysis")

st.markdown("""
Hospital readmissions within 30 days are a big challenge for healthcare and can increase costs for hospitals. To understand this, we used patient data to find who is more likely to be readmitted and to help hospitals make better decisions. In this project, we collected and cleaned patient data, checked missing values, updated column types, and combined extra data for better analysis. We studied patient demographics, hospital stay details, clinical info, and medication patterns. We found that readmissions are not very common but important. Gender and race showed little difference in readmission rates. Patients with medication changes during their stay had higher readmission rates, and emergency admissions also increased risk. The Vitality Complexity Index (VCI) was a strong predictor of risk, showing which patients are more likely to come back soon. This analysis helps hospitals see the real reasons behind readmissions, not just totals or averages. It shows that patients with high VCI scores, emergency admissions, and medication changes are the main reasons for early readmission. Hospitals can use this to focus care on high-risk patients, adjust nurse staffing, and give extra attention to patients going to nursing homes. Using this data-driven approach can help reduce readmissions and lower costs.
""")


# ------------------- Age Distribution of Patients----------------------------
fig = px.histogram(
    df,
    x="age",
    title="Age Distribution of Patients",
    text_auto=True
)

fig.update_layout(
    width=950,
    height=500,
    bargap=0.2,
    template="plotly_white",
    title_x=0.3
)
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This chart shows how patients are distributed across different age ranges. 
It helps identify which age groups are most commonly admitted to the hospital 
and may indicate patterns in readmission risk among different ages.
""")

# ------------------- Readmission Status Distribution----------------------------
fig = px.histogram(
    df,
    x="readmitted",
    title="Readmission Status Distribution",
    labels={"readmitted": "Readmitted", "count": "Number of Patients"},
    text_auto=True
)

fig.update_layout(
    width=700,
    height=500,
    template="plotly_white",
    bargap=0.2,
    title_x=0.3
)
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This chart shows the distribution of patients by readmission status. 
It highlights how many patients were readmitted within 30 days compared to those who were not.
""")

# ------------------- Readmission Rate by Race and Gender----------------------------
df_clean = df[(df["gender"] != "Unknown/Invalid") & (df["race"] != "?")]
df_clean["readmit_30"] = df_clean["readmitted"].apply(lambda x: 1 if x == "<30" else 0)

rate_df = df_clean.groupby(["race", "gender"])["readmit_30"].mean().reset_index()

fig = px.bar(
    rate_df,
    x="race",
    y="readmit_30",
    color="gender",
    barmode="group",
    title="Readmission Rate by Race and Gender",
    labels={"readmit_30": "30-Day Readmission Rate"}
)

fig.update_layout(title_x=0.3)
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(tickformat=".0%", fixedrange=True)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This chart shows differences in 30-day readmission rates across races and genders. 
It helps identify demographic groups that may require closer monitoring to reduce readmissions.
""")

# ------------------- Readmission Rate by Medication Type----------------------------
med_rate = df.groupby("medication_type")["readmit_30"].mean().reset_index()

fig = px.bar(
    med_rate,
    x="medication_type",
    y="readmit_30",
    title="30-Day Readmission Rate by Medication Type",
    labels={"readmit_30": "30-Day Readmission Rate"}
)

fig.update_layout(
    width=750,
    height=500,
    template="plotly_white",
    bargroupgap=0.1,
    title_x=0.3
)
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True, tickformat=".0%")

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This chart shows how 30-day readmission rates vary depending on the type of medication patients receive. 
It indicates whether patients on insulin, oral medication, or no medication are at higher risk.
""")

# ------------------- Readmission Rate by Medication Change----------------------------
change_rate = df.groupby("change")["readmit_30"].mean().reset_index()

fig = px.bar(
    change_rate,
    x="change",
    y="readmit_30",
    title="30-Day Readmission Rate by Medication Change",
    labels={"readmit_30": "30-Day Readmission Rate"}
)

fig.update_layout(
    width=750,
    height=500,
    template="plotly_white",
    bargroupgap=0.1,
    title_x=0.3
)
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True, tickformat=".0%")

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This chart shows whether patients who had medication changes during their hospital stay 
are more likely to be readmitted within 30 days.
""")

# ------------------- Scatter Plot: Time in Hospital vs Lab Procedures----------------------------
fig = px.scatter(
    df,
    x="time_in_hospital",
    y="num_lab_procedures",
    trendline="ols",
    title="Time in Hospital vs Number of Lab Procedures"
)

fig.update_layout(title_x=0.3)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This scatter plot explores the relationship between the length of hospital stay and the number of lab procedures performed. 
It helps identify whether longer stays are associated with more lab tests.
""")

# ------------------- Correlation Heatmap of Numerical Features----------------------------
num_cols = ['num_medications', 'num_lab_procedures', 'time_in_hospital']
corr_matrix = df[num_cols].corr()

fig = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    title="Correlation Heatmap of Numerical Features"
)

fig.update_layout(width=600, height=500, title_x=0.3)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This heatmap shows correlations between numerical features such as number of medications, lab procedures, and time in hospital. 
It helps understand relationships that may influence readmission risk.
""")

# ------------------- Box Plot: Time in Hospital by Readmission Status----------------------------
df_subset = df[df['readmitted'].isin(['NO', '<30'])]

fig = px.box(
    df_subset,
    x='readmitted',
    y='time_in_hospital',
    color='readmitted',
    title="Time in Hospital by Readmission Status",
    labels={'readmitted': 'Readmitted', 'time_in_hospital': 'Time in Hospital (days)'}
)

fig.update_layout(width=700, height=450, title_x=0.3)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This box plot compares hospital stay durations between patients readmitted within 30 days and those who were not. 
It helps highlight patterns in stay length that may predict readmission risk.
""")

# ------------------- 30-Day Readmission Rate by Discharge Disposition----------------------------
df_subset2 = df[df['discharge_disposition_desc'].isin([
    'Discharged to home', 
    'Discharged/transferred to a Skilled Nursing Facility (SNF)'
])]

readmit_rates_30 = df_subset2.groupby('discharge_disposition_desc')['readmit_30'].mean().reset_index()
df_subset2['discharge_disposition_desc'] = df_subset2['discharge_disposition_desc'].replace(
    'Discharged/transferred to a Skilled Nursing Facility (SNF)',
    'Transferred to Nursing Room'
)

fig = px.bar(
    readmit_rates_30,
    x='discharge_disposition_desc',
    y='readmit_30',
    text_auto=True,
    title='30-Day Readmission Rate by Discharge Disposition',
    color_discrete_sequence=[["#1fb48f","#2CB104"]]
)

fig.update_yaxes(tickformat=".0%")
fig.update_layout(width=700, height=450, title_x=0.3)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This chart shows how discharge disposition affects 30-day readmission rates. 
Patients discharged to nursing facilities have higher readmission rates.
""")

# ------------------- 30-Day Readmission Rate by VCI Risk Group----------------------------
readmission_by_risk = df.groupby('VCI_Risk')['readmitted_30'].mean().reset_index()
readmission_by_risk['Readmission_Percentage'] = readmission_by_risk['readmitted_30'] * 100

fig = px.bar(
    readmission_by_risk,
    x='VCI_Risk',
    y='Readmission_Percentage',
    text='Readmission_Percentage',
    title='30-Day Readmission Rate by VCI Risk Group',
    color_discrete_sequence=[["#05b387","#05b387","#05b387"]]
)

fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(title_x=0.3, yaxis=dict(range=[0, 20]), template='plotly_white')

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This chart shows how patients' VCI risk classification (Low, Medium, High) relates to 30-day readmission rates. 
Higher VCI scores are associated with higher readmission, helping prioritize patients for monitoring.
""")
