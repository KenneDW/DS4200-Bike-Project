import pandas as pd
import altair as alt
import json
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go

def plt1():
    data = pd.read_csv("Final/DS4200-Bike-Project/data/trip_data.csv")
    data['started_at'] = pd.to_datetime(data['started_at'])
    data['month'] = data['started_at'].dt.to_period('M').astype(str)

    # Getting variables aggregated
    bike_type_counts = data.groupby(['month', 'rideable_type']).size().reset_index(name='count')
    bike_type_counts['category'] = 'Bike Type'
    bike_type_counts = bike_type_counts.rename(columns={'rideable_type': 'subcategory'})

    member_type_counts = data.groupby(['month', 'member_casual']).size().reset_index(name='count')
    member_type_counts['category'] = 'Member Type'
    member_type_counts = member_type_counts.rename(columns={'member_casual': 'subcategory'})


    # Combine all into one DataFrame and removing random august month
    combined_df = pd.concat([bike_type_counts, member_type_counts], ignore_index=True)
    combined_df = combined_df[combined_df['month'] != '2024-08']

    combined_df['percent'] = combined_df.groupby(['month', 'category'])['count'].transform(lambda x: x / x.sum() * 100)
    combined_df['percent'] = combined_df['percent'].round(1)

    # dropdown
    category_selector = alt.param(
        name='CategorySelector',
        bind=alt.binding_select(
            options=['Bike Type', 'Member Type'],
            name='Y Axis: '
        ),
        value='Bike Type')

    # [;pt ]
    chart = alt.Chart(combined_df).transform_filter(
        alt.datum.category == category_selector
    ).mark_bar().encode(
        x=alt.X('month:N', title='Month', axis=alt.Axis(labelAngle=-40)),
        y=alt.Y('count:Q', title='Count'),
        color=alt.Color('subcategory:N', title='Subcategory', scale=alt.Scale(scheme='pastel1')),
        tooltip=[
            alt.Tooltip('month:N'),
            alt.Tooltip('subcategory:N'),
            alt.Tooltip('count:Q', format=','),
            alt.Tooltip('percent:Q', title='Percent', format='.1f')]
    ).add_params(
        category_selector
    ).properties(
        width=600,
        height=400,
        title=alt.TitleParams(text='Monthly Trip Data', fontSize=18))


    with open('Final/DS4200-Bike-Project/app/viz1.json', 'w') as f:
        json.dump(chart.to_dict(), f)

    print("Visualization exported successfully to js/viz1_spec.json")


def plt4():

    df = pd.read_csv("Final/DS4200-Bike-Project/data/trip_data.csv")

    # Preprocess the data
    df["started_at"] = pd.to_datetime(df["started_at"])
    df["ended_at"] = pd.to_datetime(df["ended_at"])
    df["month"] = df["started_at"].dt.month_name()
    df["manhattan_distance"] = abs(df["start_lat"] - df["end_lat"]) + abs(df["start_lng"] - df["end_lng"])
    valid_months = ["April", "September", "December"]
    df_filtered = df[df["month"].isin(valid_months)]


    # Define pastel1 colors for bike types
    color_map = {"classic_bike": pc.qualitative.Pastel1[0], "electric_bike": pc.qualitative.Pastel1[1]}

    fig = go.Figure()
    visibility_map = []

    for month in valid_months:
        month_data = df_filtered[df_filtered["month"] == month]
        visible = month == "April"

        for bike_type in ["classic_bike", "electric_bike"]:
            data = month_data[month_data["rideable_type"] == bike_type]
            fig.add_trace(
                go.Box(
                    y=data["manhattan_distance"],
                    name=bike_type.replace("_", " ").title(),
                    boxpoints="outliers",
                    marker_color=color_map[bike_type],
                    visible=visible
                )
            )
        visibility_map.append([month == m for m in valid_months for _ in range(2)])


    fig.update_layout(
        title="Distribution of Manhattan Distances",
        yaxis_title="Calculated Manhattan Distance",
        updatemenus=[
            dict(
                buttons=[
                    dict(label=month,
                        method="update",
                        args=[
                            {"visible": vis},
                            {"title": f"Distribution of Manhattan Distances - {month}"}
                        ])
                    for month, vis in zip(valid_months, visibility_map)],
                direction="down",
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.15,
                yanchor="top")])
    fig.write_html("viz4_plotly.html", include_plotlyjs='cdn', full_html=False)

def plt5():
    df = pd.read_csv("data/trip_data.csv")

    df['started_at'] = pd.to_datetime(df['started_at'])
    df['hour'] = df['started_at'].dt.hour
    df['day_of_week'] = df['started_at'].dt.day_name().str[:3]
    df['month'] = df['started_at'].dt.month_name()

    agg_df = df.groupby(['month', 'day_of_week', 'hour']).size().reset_index(name='ride_count')

    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Make selector
    month_select = alt.selection_point(
        fields=['month'],
        bind=alt.binding_select(options=agg_df['month'].unique().tolist(), name='Month:'),
        value={'month': 'April'}
    )

    # Build the heatmap
    chart = alt.Chart(agg_df).mark_rect().encode(
        x=alt.X('hour:O', title='Hour of Day'),
        y=alt.Y('day_of_week:N', sort=day_order, title='Day of Week'),
        color=alt.Color('ride_count:Q', scale=alt.Scale(scheme='blues'), title='Number of Rides'),
        tooltip=['day_of_week:N', 'hour:O', 'ride_count:Q']
    ).add_params(
        month_select
    ).transform_filter(
        month_select
    ).properties(
        width=500,
        height=300,
        title='Bluebike Rides by Day of Week and Hour'
    )

    chart.save("altair_heatmap.html")


def main():
    plt1()
if __name__ == "__main__":
    main()
