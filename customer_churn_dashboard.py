import streamlit as st
st.set_page_config(page_title='🏦 European bank Customer Churn Dashboard', layout='wide')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
# Load the cleaned dataset
df = pd.read_csv("European_Bank_Cleaned.csv")

st.markdown("""<style>
.stApp {
    background-color: #61155c;                            
}
[data-testid="stSidebar"] {
    background-color: #4e124a;
    overflow: hidden !important;
}

[data-testid="stSidebar"] *{
    color: #40d2d7 ;
}
          
/* Style for select boxes */
div[data-baseweb="select"] > div {
    background-color: #dce19d2e !important;
    border-radius: 10px !important;
    border: 2px solid #e1bd78 !important;
}
            
/* Style for the marquee container and text(title)*/
.marquee {
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
    box-sizing: border-box;
}
            
/* Style for the marquee text and animation to it */
.marquee span {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 12s linear infinite;
    color: #e1bd78;
    font-size: 36px;
    font-weight: 500;
    margin-bottom: 50px;
}
            
/* Keyframes for the marquee animation */
@keyframes marquee {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-100%); }
}
/* # h2 used for section titles */
h2{           
    font-size: 28px;
    font-weight: 400;   
}
  
[data-testid="stMetricValue"] {
    color: #4DE49D !important;
    font-size: 25px;

}
            
[data-testid="stMetricLabel"] {
    color: #CFD75D !important;
    font-weight: bold;
}
            
/* Style for sidebar buttons */
[data-testid="stSidebar"] button {
    background-color: #dce19d2e !important;
    color: #61155c !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 6px 12px !important;
    margin-left: 150px !important;
}
            
/* Hover effect for sidebar buttons */
[data-testid="stSidebar"] button:hover {    
    background-color: #e77f90 !important;
    color: black !important;
}
            
/* Style for expander summary */
details summary {      
    color: #87d3e1 !important;           
    font-size: 16px !important;
    font-weight: 600 !important;
}

            
</style>
<div class="marquee"><span>Customer Segmentation & Churn Pattern Analytics in European Banking 💳 </span></div>""", unsafe_allow_html=True)
st.markdown("""
<div style='background-color:#7C2078; padding:12px;color:#4DE49D; border-radius:10px; margin-bottom:20px;'>

📌 <b>About This Dashboard</b><br>
This dashboard analyzes customer churn patterns in a European bank dataset.  
It helps identify key risk segments based on geography, customer activity, balance, and product usage.
            
</div>
""", unsafe_allow_html=True)
with st.expander("📂 Dataset Information"):
    st.markdown("""<div style='color: #CFD75D; font-size: 16px;'>
- Rows: ~10,000 customers <br>
- Target Variable: Exited (1 = Churned, 0 = Retained)  <br>
- Key Features: Age, Balance, Geography, Tenure, Products  <br>

🎯 **Goal:** Identify patterns and reduce customer churn.
</div>""", unsafe_allow_html=True)
filtered_df = df.copy()
st.sidebar.markdown("""
<div style='color:#e1bd78; font-size:16px; margin-top:10px;'>

🎯 <b>Business Objective:</b>  
Reduce churn by identifying high-risk segments and improving customer engagement strategies.

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div style= 'color:#e0b098; font-size: 5; font-weight: 500;'>🔍 Use Filters To Explore Churn Pattern</div>" , unsafe_allow_html=True) 

# Filters

selected_age = st.sidebar.multiselect("Select Age Group", filtered_df['Age_Group'].unique(),key="age_filter")
selected_balance = st.sidebar.multiselect("Select Balance Group", filtered_df['Balance_Group'].unique(),key="balance_filter")
filtered_df['Geography'] = np.select(
    [
        filtered_df['Geography_Germany'] == 1,
        filtered_df['Geography_Spain'] == 1
    ],
    [
        "Germany",
        "Spain"
    ],
    default="France",
)
selected_geo = st.sidebar.multiselect("Select Geography", filtered_df['Geography'].unique(),key="geography_filter")




# Apply filters
if selected_age:
    filtered_df = filtered_df[filtered_df['Age_Group'].isin(selected_age)]
# Apply filters
if selected_balance:
    filtered_df = filtered_df[(filtered_df['Balance_Group'].isin(selected_balance))]
if selected_geo:
    filtered_df = filtered_df[filtered_df['Geography'].isin(selected_geo)]

def reset_filters():
    st.session_state["age_filter"] = []
    st.session_state["balance_filter"] = []
    st.session_state["geography_filter"] = []
st.sidebar.button("🔄 Reset Filters", on_click=reset_filters)
    
# 1. Overall Churn Rate
overall_churn_rate = filtered_df['Exited'].mean()

# 2. Segment Churn Rate (using Age Group as segment)
segment_churn_rate = filtered_df.groupby('Age_Group')['Exited'].mean()

# 3. High-Value Churn Ratio
high_value = filtered_df[filtered_df['Balance_Group'] == 'High-balance']
high_value_churn = high_value['Exited'].mean()


# 4. Geographic Risk Index (max churn among regions)
geo_germany = filtered_df[filtered_df['Geography_Germany'] == 1]['Exited'].mean()
geo_spain = filtered_df[filtered_df['Geography_Spain'] == 1]['Exited'].mean()
geo_france = filtered_df[(filtered_df['Geography_Germany'] == 0) & (filtered_df['Geography_Spain'] == 0)]['Exited'].mean()
geo_rates = {
    "France": filtered_df[
        (filtered_df['Geography_Germany'] == 0) & 
        (filtered_df['Geography_Spain'] == 0)
    ]['Exited'].mean(),

    "Spain": filtered_df[filtered_df['Geography_Spain'] == 1]['Exited'].mean(),

    "Germany": filtered_df[filtered_df['Geography_Germany'] == 1]['Exited'].mean()
}

geo_risk = max(geo_rates.values())

# 6. Engagement Drop Indicator
engagement = filtered_df.groupby('IsActiveMember')['Exited'].mean()
engagement_drop = engagement.get(0, 0) - engagement.get(1, 0)



st.markdown("<h2 style='color:#87d3e1;'>🗺️ Risk Indicators</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

col1.metric(
    "Geographic Risk Index",
    f"{geo_risk:.2%}" if pd.notnull(geo_risk) else "0%"
)

col2.metric(
    "Engagement Drop Indicator",
    f"{engagement_drop:.2%}"
)

st.markdown("<p style='color:#87d3e1; font-size: 20px; font-weight: 500;'>📍 Key Churn Metrics</p>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("Overall Churn Rate", f"{overall_churn_rate:.2%}" )
col2.metric("High-Value Churn", f"{high_value_churn:.2%}" if pd.notnull(high_value_churn) else "0%")
segment_value = segment_churn_rate.iloc[0] if not segment_churn_rate.empty else 0

col3.metric("Segment Churn", f"{segment_value:.2%}")

with st.expander("📘 KPI Explanation"):
    st.markdown("""<div style='color: #CFD75D; font-size: 16px;'>
- Churn Rate: % of customers who left the bank <br>
- High-Value Churn: Churn among high balance customers <br>
- Segment Churn: Churn rate within specific age groups <br>
- Engagement drop Risk: inactive customer behavior <br>
- Geographic Risk Index: Geographical churn Risk <br>

💡 Helps business focus on retention strategies.
<div>""", unsafe_allow_html=True)
    

# Find highest churn geography
geo_dict = {
    "France": geo_france,
    "Spain": geo_spain,
    "Germany": geo_germany
}
highest_geo = max(geo_dict, key=geo_dict.get)

# Engagement gap
engagement_gap = engagement.get(0, 0) - engagement.get(1, 0)

st.sidebar.markdown(
f"""
<div style="background-color:#4e124a; padding:15px; border-radius:10px;">

🔑 **Key Insights**

• 📍 **{highest_geo} has the highest churn**, indicating regional risk concentration  

• 📉 **Inactive customers churn {engagement_gap:.2%} more than active users**, highlighting engagement impact  

• 💰 **High-value customers show elevated churn**, suggesting potential revenue risk  

• 🎯 **Churn is not evenly distributed**, indicating targeted retention strategies are needed 

</div>
""",
unsafe_allow_html=True
)


st.sidebar.markdown("<h2 style='color:#e1bd78;font-size: 16px;margin-left: 150px;'>📥 Export Data</h2>", unsafe_allow_html=True)

st.sidebar.download_button(
"Download Data",
filtered_df.to_csv(index=False),
file_name="churn_data.csv"
)



st.markdown("<h2 style='color:#87d3e1;'> 📊 Overall Churn Distribution & Correlation</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
churn_counts = filtered_df['Exited'].value_counts().reset_index()
churn_counts.columns = ['Exited', 'Count']

churn_counts['Status'] = churn_counts['Exited'].map({0: "Retained", 1: "Churned"})
fig1, ax1 = plt.subplots(figsize=(2,2))
# Create pie
fig1 = px.pie(churn_counts,names='Status',values='Count',color='Status',color_discrete_map={"Retained": "#e1bd78","Churned": "#CFD75D"})
fig1.update_layout(paper_bgcolor="#61155c",plot_bgcolor="#61155c",font=dict(color="#87d3e1", size=15), showlegend=False)
fig1.update_traces(textinfo="percent+label",textfont=dict(color="#61155c"),pull=[0.05, 0] )
fig1.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}")
col1.plotly_chart(fig1, use_container_width=True)



numeric_df = filtered_df.select_dtypes(include=['number'])
# Correlation
corr = numeric_df.corr()
fig2, ax2 = plt.subplots(figsize=(9,6))
fig2 = px.imshow(corr,text_auto=".2f",color_continuous_scale=["#dfdfdf","#e1bd78", "#B3BE0D", "#d8a48f" ],aspect="auto")
fig2.update_layout(plot_bgcolor="#61155c",paper_bgcolor="#61155c",font=dict(color="#87A73E"))
fig2.update_xaxes(tickangle=45,side="bottom",tickfont=dict(color="#87A73E", size=15))
fig2.update_yaxes(tickangle=0,tickfont=dict(color="#87A73E", size=15))
fig2.update_xaxes(showgrid=False, zeroline=False)
fig2.update_yaxes(showgrid=False, zeroline=False)
fig2.update_coloraxes(colorbar=dict(title=dict(text="Correlation",font=dict(color="#87A73E", size =15)),tickfont=dict(color="#84B5CD", size=15)))
col2.plotly_chart(fig2, use_container_width=True)



st.markdown("<h2 style='color:#87d3e1;'> 👥 Age & Tenure Churn Comparison</h2>", unsafe_allow_html=True)
col3, col4 = st.columns(2)
# Age chart
age_churn = filtered_df.groupby('Age_Group')['Exited'].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(12,6))
fig3 = px.bar(age_churn,x='Age_Group',y='Exited',text='Exited')
fig3.update_traces(marker=dict(color="#e1bd78",line=dict(color="black", width=1)),opacity=0.7,texttemplate='%{text:.2%}',textposition='inside')
fig3.update_layout(plot_bgcolor="#61155c",paper_bgcolor="#61155c",font=dict(color="#87A73E", size=15))
fig3.update_xaxes(showgrid=False,zeroline=False,showline=False,title="", tickfont=dict(color="#87A73E", size=15))
fig3.update_yaxes(showgrid=False,zeroline=False,showline=False,title="", tickfont=dict(color="#87A73E", size=15))
col3.plotly_chart(fig3)




# Tenure chart
tenure_churn = filtered_df.groupby('Tenure_Group')['Exited'].mean().reset_index()
fig4, ax4 = plt.subplots(figsize=(12,6))
fig4 = px.bar(tenure_churn,x='Tenure_Group',y='Exited',color='Exited',color_continuous_scale=["#e1bd78",  "#e8d6cf", "#d8a48f"])
fig4.update_layout(plot_bgcolor="#61155c",paper_bgcolor="#61155c",font=dict(color="#87A73E")  )
fig4.update_xaxes(title="",showgrid=False,zeroline=False,showline=False,tickfont=dict(color="#87A73E", size=15))
fig4.update_yaxes(title="",showgrid=False,zeroline=False,showline=False,tickfont=dict(color="#87A73E", size=15))
fig4.update_coloraxes(colorbar=dict(title=dict(text="Exited",font=dict(color="#87A73E", size=15)),tickfont=dict(color="#84B5CD", size=15)))
col4.plotly_chart(fig4, use_container_width=True)



st.markdown("<h2 style='color:#87d3e1;'>📈 Area & Product-Based Churn Analysis</h2>", unsafe_allow_html=True)
col5, col6 = st.columns(2)

geo_churn = {
    "France": filtered_df[
        (filtered_df['Geography_Germany'] == 0) & 
        (filtered_df['Geography_Spain'] == 0)
    ]['Exited'].mean(),
        
    "Spain": filtered_df[filtered_df['Geography_Spain'] == 1]['Exited'].mean(),
        
    "Germany": filtered_df[filtered_df['Geography_Germany'] == 1]['Exited'].mean()
}
geo_df = pd.DataFrame(list(geo_churn.items()), columns=["Country", "Churn Rate"])

fig5, ax5 = plt.subplots(figsize=(12,6))
fig5 = px.bar(geo_df,x="Country",y="Churn Rate",text="Churn Rate")
fig5.update_traces(marker=dict(color="#e3b76c",line=dict(color="black", width=1)   ),texttemplate='%{text:.2%}')
fig5.update_layout(plot_bgcolor="#61155c",paper_bgcolor="#61155c",  font=dict(color="#87A73E"))
fig5.update_xaxes(showgrid=False,showline=False,zeroline=False, tickfont=dict(color="#87A73E", size=15))
fig5.update_yaxes(showgrid=False,showline=False,zeroline=False, tickfont=dict(color="#87A73E", size=15))
fig5.update_xaxes(title="")
fig5.update_yaxes(title="")
col5.plotly_chart(fig5, use_container_width=True)



product_churn = filtered_df.groupby('NumOfProducts')['Exited'].mean().reset_index()
fig6, ax6 = plt.subplots(figsize=(12,6))
fig6 = px.bar(product_churn,x='NumOfProducts',y='Exited',color='Exited',color_continuous_scale=["#dfdfdf","#ad8b4b", "#5CCF8A", "#d8a48f"],)
fig6.update_layout(plot_bgcolor="#61155c",paper_bgcolor="#61155c",font=dict(color="#87A73E"))
fig6.update_xaxes(title="",showgrid=False,zeroline=False,showline=False,color="#87A73E", tickfont=dict(color="#87A73E", size=15))
fig6.update_yaxes(title="",showgrid=False,zeroline=False,showline=False,color="#87A73E", tickfont=dict(color="#87A73E", size=15))
fig6.update_coloraxes(colorbar=dict(title=dict(text="Exited",font=dict(color="#87A73E", size=15)),tickfont=dict(color="#84B5CD", size=15)))
col6.plotly_chart(fig6, use_container_width=True)



col7 = st.columns(1)

st.markdown("<h2 style='color:#87d3e1;'>💰 High-Value Customer Churn</h2>", unsafe_allow_html=True)
# Check if High-balance data exists after filtering
high_value = filtered_df[filtered_df['Balance_Group'] == 'High-balance']

if high_value.empty:
    st.warning("No High-Value Customer data available for the selected filters.")
    st.stop()
else:
    high_value = high_value.copy()

high_value['Exited_Label'] = high_value['Exited'].map({
    0: "Retained",
    1: "Churned"
})

# Balance vs churn
fig7, ax7 = plt.subplots(figsize=(15,5))
fig7 = px.histogram(high_value,x="Balance",color="Exited_Label",nbins=30,barmode="overlay",color_discrete_map={"Retained": "#e1bd78", "Churned": "#CFD75D"})
fig7.update_traces(opacity=0.7)
fig7.update_layout(colorway=["#e1bd78", "#CFD75D"])
fig7.update_layout(plot_bgcolor="#61155c",paper_bgcolor="#61155c",font=dict(color="#87A73E"))
fig7.update_xaxes(showgrid=False,zeroline=False,showline=False,title="",tickfont=dict(color="#87A73E", size=15))
fig7.update_yaxes(showgrid=False,zeroline=False,showline=False,title="",tickfont=dict(color="#87A73E", size=15))
fig7.update_layout(legend=dict(font=dict(size=14, color="#84B5CD"),orientation="v",y=1,x=0.7,title=dict(text="Exited",font=dict(size=16, color="#87A73E")  )))
st.plotly_chart(fig7, use_container_width=True)



