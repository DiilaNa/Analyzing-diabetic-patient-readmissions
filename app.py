import streamlit as st
import pandas as pd
import plotly.express as px

df =  pd.read_pickle("Assets/Patient_data.pkl")

st.title("Hospital Readmission Analysis")

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
    title_x=0.5,
    xaxis_tickangle=-45
)

fig.update_xaxes(
    title_text="Age Group",
    fixedrange=True
)

fig.update_yaxes(
    title_text="Number of Patients",
    fixedrange=True
)

st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(
    df,
    x="readmitted",
    title="Readmission Status Distribution",
    labels={
        "readmitted": "Readmitted",
        "count": "Number of Patients"
    },
    text_auto=True
)

fig.update_layout(
    width=700,
    height=500,
    template="plotly_white",
    bargap=0.2,
    title_x=0.5
)

fig.update_xaxes(title_text="Readmitted",fixedrange=True)
fig.update_yaxes(title_text="Number of Patients",fixedrange=True)

st.plotly_chart(fig, use_container_width=True)

df_clean = df[
    (df["gender"] != "Unknown/Invalid") &
    (df["race"] != "?")
]

df_clean["readmit_30"] = df_clean["readmitted"].apply(
    lambda x: 1 if x == "<30" else 0
)

rate_df = (
    df_clean
    .groupby(["race", "gender"])["readmit_30"]
    .mean()
    .reset_index()
)

fig = px.bar(
    rate_df,
    x="race",
    y="readmit_30",
    color="gender",
    barmode="group",
    title="Readmission Rate by Race and Gender",
    labels={"readmit_30": "30-Day Readmission Rate"}
)

fig.update_xaxes(
    fixedrange=True            
)

fig.update_yaxes(
    tickformat=".0%",
    fixedrange=True
)

st.plotly_chart(fig, use_container_width=True)
med_rate = (
    df
    .groupby("medication_type")["readmit_30"]
    .mean()
    .reset_index()
)
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
    title_x=0.5
)
fig.update_xaxes(
    fixedrange=True            
)

fig.update_yaxes(
    fixedrange=True,
    tickformat=".0%"
)

st.plotly_chart(fig, use_container_width=True)

change_rate = (
    df
    .groupby("change")["readmit_30"]
    .mean()
    .reset_index()
)
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
    title_x=0.5
)

fig.update_xaxes(
    fixedrange=True            
)

fig.update_yaxes(
    fixedrange=True,
    tickformat=".0%"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    df,
    x="time_in_hospital",
    y="num_lab_procedures",
    trendline="ols",
    title="Time in Hospital vs Number of Lab Procedures"
)

st.plotly_chart(fig, use_container_width=True)

num_cols = ['num_medications', 'num_lab_procedures', 'time_in_hospital']

corr_matrix = df[num_cols].corr()
fig = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    title="Correlation Heatmap of Numerical Features"
)

fig.update_layout(
    width=600,
    height=500,
    title_x=0.5
)
st.plotly_chart(fig, use_container_width=True)

df_subset = df[df['readmitted'].isin(['NO', '<30'])]

fig = px.box(
    df_subset,
    x='readmitted',
    y='time_in_hospital',
    color='readmitted',
    title="Time in Hospital by Readmission Status",
    labels={'readmitted': 'Readmitted', 'time_in_hospital': 'Time in Hospital (days)'}
)

fig.update_layout(width=700, height=450, title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

df_subset2 = df[df['discharge_disposition_desc'].isin([
    'Discharged to home', 
    'Discharged/transferred to a Skilled Nursing Facility (SNF)'
])]

readmit_counts = df_subset2.groupby(['discharge_disposition_desc', 'readmitted']).size().unstack(fill_value=0)

readmit_rates = readmit_counts.div(readmit_counts.sum(axis=1), axis=0) * 100

df_subset2['discharge_disposition_desc'] = df_subset2['discharge_disposition_desc'].replace(
    'Discharged/transferred to a Skilled Nursing Facility (SNF)',
    'Transferred to Nursing Room'
)

readmit_rates_30 = df_subset2.groupby('discharge_disposition_desc')['readmit_30'].mean().reset_index()

fig = px.bar(
    readmit_rates_30,
    x='discharge_disposition_desc',
    y='readmit_30',
    text_auto=True,
    title='30-Day Readmission Rate by Discharge Disposition',
    labels={'discharge_disposition_desc': 'Discharge Disposition', 'readmit_30': '30-Day Readmission Rate'},
    color_discrete_sequence=[["#1fb48f","#2CB104"]]
)

fig.update_yaxes(tickformat=".0%")
fig.update_layout(width=700, height=450, title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

readmission_by_risk = (
    df
    .groupby('VCI_Risk')['readmitted_30']
    .mean()
    .reset_index()
)
readmission_by_risk['Readmission_Percentage'] = (
    readmission_by_risk['readmitted_30'] * 100
)

fig = px.bar(
    readmission_by_risk,
    x='VCI_Risk',
    y='Readmission_Percentage',
    text='Readmission_Percentage',
    labels={'Readmission_Percentage': 'Readmission Rate (%)'},
    title='30-Day Readmission Rate by VCI Risk Group'
)

fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(
    yaxis=dict(range=[0, 20]),
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

