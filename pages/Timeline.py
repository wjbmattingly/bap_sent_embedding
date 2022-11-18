import streamlit as st
import json
from streamlit_timeline import timeline

@st.cache(allow_output_mutation=True)
def load_data():
    with open('./data/vol7_timeline.json', "r") as f:
        data = json.load(f)
    return data

# use full page width
st.set_page_config(layout="wide")
data = load_data()
display_events = []
years = st.sidebar.multiselect("Select Years", [i for i in range(1960, 2000)])
years.sort()
if years:
    for event in data["events"]:
        if event["start_date"]["year"] in years:
            display_events.append(event)
    final_display = {"title": {"text": {"headline": f"Timeline of the {len(display_events)} HRVs in the TRC Vol 7 for Years {', '.join([str(year) for year in years])}"}}, "events": display_events}
    st.write(f"Total of {len(display_events)} Results")
    # render timeline
    timeline(final_display, height=800)
