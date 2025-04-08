import pandas as pd
import altair as alt
import json
import os


data = pd.read_csv("data/trip_data.csv")
data['started_at'] = pd.to_datetime(data['started_at'])
data['month'] = data['started_at'].dt.to_period('M').astype(str)

# Getting variables aggregated
bike_type_counts = data.groupby(['month', 'rideable_type']).size().reset_index(name='count')
bike_type_counts['category'] = 'Bike Type'
bike_type_counts = bike_type_counts.rename(columns={'rideable_type': 'subcategory'})

member_type_counts = data.groupby(['month', 'member_casual']).size().reset_index(name='count')
member_type_counts['category'] = 'Member Type'
member_type_counts = member_type_counts.rename(columns={'member_casual': 'subcategory'})

avg_duration = data.groupby('month')['duration'].mean().reset_index(name='count')
avg_duration['category'] = 'Average Duration'
avg_duration['subcategory'] = 'Average Duration'

# Combine all into one DataFrame and removing random august month
combined_df = pd.concat([bike_type_counts, member_type_counts, avg_duration], ignore_index=True)
combined_df = combined_df[combined_df['month'] != '2024-08']

# Dropdown param (Altair v5)
category_selector = alt.param(
    name='CategorySelector',
    bind=alt.binding_select(
        options=['Bike Type', 'Member Type', 'Average Duration'],
        name='Y Axis: '
    ),
    value='Bike Type'
)

# Create the chart
chart = alt.Chart(combined_df).transform_filter(
    alt.datum.category == category_selector
).mark_bar().encode(
    x=alt.X('month:N', title='Month', axis=alt.Axis(labelAngle=-40)),
    y=alt.Y('count:Q', title='Count'),  # Default title (won't dynamically update)
    color=alt.Color('subcategory:N', title='Subcategory', scale=alt.Scale(scheme='pastel1')),
    tooltip=['month', 'subcategory', 'count']
).add_params(
    category_selector
).properties(
    width=600,
    height=400,
    title=alt.TitleParams(text='Monthly Trip Data', fontSize=18))


with open('app/viz1_spec.json', 'w') as f:
    json.dump(chart.to_dict(), f)

print("Visualization exported successfully to js/viz1_spec.json")
