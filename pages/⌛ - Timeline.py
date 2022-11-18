import streamlit as st
from streamlit_timeline import timeline
import pandas as pd

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_feather("data/full_data_00-00-05")
    df = df[df["date"].notna()]
    return df

def filter_data(df, years):
    events = []
    for idx, row in df.iterrows():
        for date in row.date:
            if date.year in years:
                events.append(
                    {"start_date": {"year": date.year, "month": date.month, "day": date.day},
                     "text": {
                         "headline": row.full_name,
                         "text": row.description
                     }})
    final_display = {"title":
    {"text": {"headline": f"Timeline of the {len(events)} HRVs in the TRC Vol 7 for Years {', '.join([str(year) for year in years])}"}},
    "events": events}
    return final_display

# use full page width
st.set_page_config(layout="wide")
df = load_data()
display_events = []
years = st.sidebar.multiselect("Select Years", [i for i in range(1960, 2000)])
years.sort()
if years:
    # for event in data["events"]:
    #     if event["start_date"]["year"] in years:
    #         display_events.append(event)
    # final_display = {"title": {"text": {"headline": f"Timeline of the {len(display_events)} HRVs in the TRC Vol 7 for Years {', '.join([str(year) for year in years])}"}}, "events": display_events}
    display_events = filter_data(df, years)
    st.write(f"Total of {len(display_events['events'])} Results")
    # render timeline
    timeline(display_events, height=800)
