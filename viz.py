import pandas as pd
import altair as alt
import json
import os


data = pd.read_csv("Final/DS4200-Bike-Project/data/trip_data.csv")

# Convert timestamp and extract month
data['started_at'] = pd.to_datetime(data['started_at'])
data['month'] = data['started_at'].dt.to_period('M').astype(str)

# Prepare subsets
bike_type_counts = data.groupby(['month', 'rideable_type']).size().reset_index(name='count')
bike_type_counts['category'] = 'Bike Type'
bike_type_counts = bike_type_counts.rename(columns={'rideable_type': 'subcategory'})

member_type_counts = data.groupby(['month', 'member_casual']).size().reset_index(name='count')
member_type_counts['category'] = 'Member Type'
member_type_counts = member_type_counts.rename(columns={'member_casual': 'subcategory'})

avg_duration = data.groupby('month')['duration'].mean().reset_index(name='count')
avg_duration['category'] = 'Average Duration'
avg_duration['subcategory'] = 'Average Duration'

# Combine all
combined_df = pd.concat([bike_type_counts, member_type_counts, avg_duration], ignore_index=True)

# Create selection param (Altair v5)
category_selector = alt.param(
    name='CategorySelector',
    bind=alt.binding_select(options=['Bike Type', 'Member Type', 'Average Duration'], name='Y Axis: '),
    value='Bike Type'
)

# Filtered chart
chart = alt.Chart(combined_df).transform_filter(
    alt.datum.category == category_selector
).mark_bar().encode(
    x=alt.X('month:N', title='Month'),
    y=alt.Y('count:Q', title='Value'),
    color=alt.Color('subcategory:N', title='Subcategory'),
    tooltip=['month', 'subcategory', 'count']
).add_params(
    category_selector
).properties(
    width=600,
    height=400,
    title='Monthly Trip Data'
)

# Display the chart (for when running in a notebook)
chart

# Export the chart to a JSON file for web embedding
with open('Final/DS4200-Bike-Project/app/viz1_spec.json', 'w') as f:
    json.dump(chart.to_dict(), f)

print("Visualization exported successfully to js/viz1_spec.json")
