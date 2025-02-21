import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# Load Data
file_path = r"C:\Users\Asus\Music\CodeWithEhtisham\AddRover-pipeline\cleaned_data.csv"
data = pd.read_csv(file_path)


# Data Preparation
data['time'] = pd.to_datetime(data['time'])
data['hour'] = data['time'].dt.hour
data['day'] = data['time'].dt.day_name()
data['month'] = data['time'].dt.month_name()

# Streamlit Page Configuration
st.set_page_config(page_title="📊 Visitor Analytics Dashboard", page_icon="📊", layout="wide")

# Custom CSS for Enhanced Styling and Responsiveness
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    body {
        font-family: 'Poppins', sans-serif;
        background: #f0f2f6;
        color: #333;
    }

    /* Add a bright and professional background */
    .stApp {
        background: linear-gradient(135deg, #ffffff, #f0f2f6);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    /* Responsive Title Bar */
    .title-bar {
        background: linear-gradient(90deg, #007bff, #00c6ff);
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }

    /* Responsive KPI Cards */
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 10px;
        margin: 20px 0;
    }

    .kpi-card {
        flex: 1 1 calc(25% - 20px);
        background: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #333;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }

    .kpi-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
    }

    /* Responsive Sidebar */
    .sidebar-box {
        background: linear-gradient(135deg, #007bff, #00c6ff);
        padding: 15px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }

    .sidebar-box:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
    }

    /* Responsive Charts */
    .chart-container {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        margin-bottom: 20px;
    }

    .chart-container:hover {
        transform: scale(1.02);
    }

    /* Media Queries for Mobile and Tablet */
    @media (max-width: 768px) {
        .title-bar {
            font-size: 24px;
            padding: 15px;
        }

        .kpi-card {
            flex: 1 1 calc(50% - 10px);
            font-size: 16px;
            padding: 15px;
        }

        .sidebar-box {
            padding: 10px;
            font-size: 14px;
        }

        .chart-container {
            padding: 10px;
        }
    }

    @media (max-width: 480px) {
        .title-bar {
            font-size: 20px;
            padding: 10px;
        }

        .kpi-card {
            flex: 1 1 100%;
            font-size: 14px;
            padding: 10px;
        }

        .sidebar-box {
            padding: 8px;
            font-size: 12px;
        }

        .chart-container {
            padding: 8px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Dashboard Title
st.markdown("<div class='title-bar'>📊 Visitor Analytics Dashboard</div>", unsafe_allow_html=True)

# Sidebar Filters
with st.sidebar:
    min_date = data['time'].min().date()
    max_date = data['time'].max().date()
    default_start_date = max_date - timedelta(days=7)
    
    st.markdown("<div class='sidebar-box'>📅 Select Date Range</div>", unsafe_allow_html=True)
    date_range = st.date_input("", [default_start_date, max_date], min_value=min_date, max_value=max_date)
    start_date, end_date = date_range
    
    st.markdown("<div class='sidebar-box'>📺 Filter by Ad ID</div>", unsafe_allow_html=True)
    ad_filter = st.multiselect("", options=data['ad_id'].unique(), default=data['ad_id'].unique())
    
    st.markdown("<div class='sidebar-box'>🎂 Filter by Age</div>", unsafe_allow_html=True)
    age_filter = st.slider("", min_value=int(data['age'].min()), max_value=int(data['age'].max()), value=(int(data['age'].min()), int(data['age'].max())))

# Filter Data
filtered_data = data[
    (data['time'].dt.date >= start_date) & 
    (data['time'].dt.date <= end_date) & 
    (data['ad_id'].isin(ad_filter)) & 
    (data['age'].between(age_filter[0], age_filter[1]))
]

# KPI Metrics
total_users = len(filtered_data)
unique_ads = filtered_data['ad_id'].nunique()
most_common_gender = filtered_data['gender'].mode()[0] if not filtered_data.empty else "N/A"
average_age = round(filtered_data['age'].mean()) if not filtered_data.empty else 0

# KPI Cards
st.markdown(
    f"""
    <div class="kpi-container">
        <div class="kpi-card"><span>👥 Total Visitors <br> {total_users}</span></div>
        <div class="kpi-card"><span>📢 Unique Ads <br> {unique_ads}</span></div>
        <div class="kpi-card"><span>📌 Most Gender <br> {most_common_gender}</span></div>
        <div class="kpi-card"><span>📊 Average Age <br> {average_age}</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Gender Distribution Pie Chart
gender_icons = {"Male": "👨", "Female": "👩", "Other": "⚧"}
gender_count = filtered_data['gender'].value_counts().reset_index()
gender_count.columns = ['Gender', 'Count']

# Remove "?" and replace unknown genders with "Other"
gender_count['Gender'] = gender_count['Gender'].replace("?", "Other")

# Create labels with icons
gender_count['Label'] = gender_count.apply(
    lambda row: f"{gender_icons.get(row['Gender'], '⚧')} {row['Gender']} Visitors ({row['Count']})", axis=1
)

# Professional and Attractive Color Palette
color_palette = ['#007bff', '#00c6ff', '#ff6f61']

fig_gender_pie = px.pie(
    gender_count, names="Label", values="Count", color="Gender",
    color_discrete_sequence=color_palette,
    hole=0.25
)

fig_gender_pie.update_traces(
    textinfo='label+percent',
    texttemplate="%{label}: %{percent:.0%}",
    pull=[0.1 if i == gender_count['Count'].idxmax() else 0.05 for i in range(len(gender_count))],
    marker=dict(line=dict(color='black', width=2)),
    hoverinfo="label+percent+value",
)

fig_gender_pie.update_layout(
    title={
        'text': "Gender Distribution Of Visitors",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    font=dict(size=16, color="#333"),
    showlegend=True,
    height=400,
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    margin=dict(t=50, b=10, l=10, r=10),
    legend=dict(title="🧑‍🤝‍🧑 Gender", font=dict(size=14, color="#333"))
)

# Enhanced CSS for mobile responsiveness
st.markdown("""
    <style>
    .chart-container {
        width: 100%;
        max-width: 100%;
        height: auto;
    }
    @media (max-width: 600px) {
        .chart-container {
            height: auto !important;
            font-size: 14px !important;
        }
        .chart-container .plotly-graph-div .main-svg {
            width: 100% !important;
            height: auto !important;
        }
        .chart-container .plotly .main-svg g {
            transform: scale(0.9) !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_gender_pie, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)



# Age Distribution Bar Chart
if 'age' in filtered_data.columns:
    age_bins = [0, 10, 20, 30, 40, 50, 60, 100]  # Added 0-10 and 60+ groups
    age_labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60+']  # Updated labels

    filtered_data['age_group'] = pd.cut(filtered_data['age'], bins=age_bins, labels=age_labels, right=False)
    
    age_count = filtered_data['age_group'].value_counts().reindex(age_labels, fill_value=0).reset_index()
    age_count.columns = ['Age Group', 'Count']

    # Use the same colors as the pie chart (lightened versions)
    color_palette = ['#007bff', '#00c6ff']  # Lightened Blue and Cyan

    fig_age_bar = px.bar(
        age_count, x='Age Group', y='Count', text='Count',
        color='Age Group', category_orders={"Age Group": age_labels},
        color_discrete_sequence=color_palette  # Light colors
    )

    fig_age_bar.update_traces(
        textposition='outside',
        marker=dict(line=dict(color="black", width=1.5))  # Stronger border for clarity
    )

    fig_age_bar.update_layout(
        title={
            'text': "Age Distribution of Visitors",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20}
        },
        xaxis=dict(title="🎂 Age Group", tickfont=dict(size=14, color="#333")),
        yaxis=dict(title="👥 Total Number of Visitors", tickfont=dict(size=14, color="#333")),
        font=dict(size=16, color="#333"),
        showlegend=False,
        height=400,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(t=50, b=10, l=10, r=10)
    )

    # Adjust the y-axis to ensure labels fit
    fig_age_bar.update_layout(yaxis=dict(range=[0, max(age_count['Count']) * 1.2]))

    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.plotly_chart(fig_age_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)




# Number of Visitors Over Time
time_series = filtered_data.groupby('time')['total_persons'].sum().reset_index()

fig_time = px.line(
    time_series, x="time", y="total_persons", markers=True,
    color_discrete_sequence=["#007bff"],
    labels={"time": "⏳ Time", "total_persons": "👥 Total Number of Visitors"}
)

fig_time.update_traces(
    line=dict(width=4),
    marker=dict(size=10, symbol="circle", color="#007bff")
)

fig_time.update_layout(
    title={
        'text': "Number of Visitors Over Time",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    xaxis=dict(title="⏳ Time", tickfont=dict(size=14, color="#333")),
    yaxis=dict(title="👥 Total Number of Visitors", tickfont=dict(size=14, color="#333")),
    font=dict(size=16, color="#333"),
    template="plotly_white",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    margin=dict(t=50, b=40, l=40, r=20)
)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_time, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# Number of Visitors Per Ad
persons_per_ad = filtered_data.groupby('ad_id')['total_persons'].sum().reset_index()

# Use the same colors as the pie chart (lightened versions)
color_palette = ['#007bff', '#00c6ff']

fig_persons = px.bar(
    persons_per_ad, x="ad_id", y="total_persons", 
    color="total_persons", color_discrete_sequence=color_palette,
    labels={"ad_id": "📢 Ad ID", "total_persons": "👥 Total Number of Visitors"}
)

fig_persons.update_traces(
    marker=dict(line=dict(color="black", width=2)),
    hoverinfo="x+y",
    opacity=0.9
)

fig_persons.update_layout(
    title={
        'text': "Number of Visitors Per Ad",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    xaxis=dict(title="📢 Ad ID", tickfont=dict(size=14, color="#333")),
    yaxis=dict(title="👥 Total Number of Visitors", tickfont=dict(size=14, color="#333")),
    font=dict(size=16, color="#333"),
    template="plotly_white",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    margin=dict(t=50, b=40, l=40, r=20)
)

# Enhanced CSS for mobile responsiveness
st.markdown("""
    <style>
    .chart-container {
        width: 100%;
        max-width: 100%;
        height: auto;
    }
    @media (max-width: 600px) {
        .chart-container {
            height: auto !important;
            font-size: 14px !important;
        }
        .chart-container .plotly-graph-div .main-svg {
            width: 100% !important;
            height: auto !important;
        }
        .chart-container .plotly .main-svg g {
            transform: scale(0.9) !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_persons, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# Number of Visitors by Hour and Day
bar_data = filtered_data.groupby(['hour', 'day']).size().reset_index(name='Count')

fig_area = px.area(
    bar_data, x="hour", y="Count", color="day",
    labels={"hour": "🕒 Hour of the Day", "Count": "👥 Total Number of Visitors", "day": "📅 Day"},
    line_group="day",
    color_discrete_sequence=["#007bff", "#00c6ff", "#ff6f61", "#ffd700", "#32cd32", "#8a2be2"],
)

fig_area.update_layout(
    title={
        'text': "Number of Visitors by Hour and Day",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20, 'color': 'black'}  # Title in black color
    },
    xaxis=dict(title="🕒 Hour of the Day", tickfont=dict(size=14, color="#333")),
    yaxis=dict(title="👥 Total Number of Visitors", tickfont=dict(size=14, color="#333")),
    font=dict(size=16, color="#333"),
    template="plotly_white",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    margin=dict(t=50, b=40, l=40, r=20),
    legend=dict(title="📅 Day", font=dict(size=14, color="#333"))
)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_area, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# Data Summary Table
if 'filtered_data' in locals():
    summary_data = filtered_data.copy()
    summary_data['date'] = summary_data['time'].dt.date
    summary_data['time_only'] = summary_data['time'].dt.time
    summary_data = summary_data[['date', 'time_only', 'ad_id', 'total_persons', 'gender', 'age']]
    summary_data.columns = ['📅 Date', '⏰ Time', '📢 Ad ID', '👥 Total Visitors', '⚧ Gender', '🎂 Age']

    st.markdown("<h2 style='text-align: center; color: black;'>Data Summary Table</h2>", unsafe_allow_html=True)
    st.markdown("<div class='summary-container' style='border: 2px solid #007bff; padding: 10px; background-color: #f0f8ff;'>", unsafe_allow_html=True)
    st.dataframe(
        summary_data.tail(10),  # Show last 10 records
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("❌ Error: 'filtered_data' is not available. Please check your dataset.")