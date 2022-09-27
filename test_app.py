import pandas as pd
import numpy as np
import json
import streamlit as st


diff_schools = ['Business School', 'Engineering School', 'Education School']
def data_import_prep(json_name, csv_name):
	df = pd.read_csv(csv_name)

	f = open(json_name)
	data_dict = json.load(f)
	# Compile different keys on each level on json dictionaries
	schools = list(data_dict.keys())


	# Topic choices list for checkboxes
	blocks = list(data_dict[schools[0]].keys())
	df.index=df['School']
	df.drop(columns=['School'],inplace=True)

	return df, data_dict, schools, blocks

with st.container():
	school_filter = st.selectbox('Select the school', diff_schools)

if school_filter == 'Business School':
	df, data_dict, schools, blocks = data_import_prep("Business School Data.json", 'grad_business_school_data.csv')

elif school_filter == 'Engineering School':
	df, data_dict, schools, blocks = data_import_prep("Engineering School Data 2.json", 'Engineering School Data.csv')

elif school_filter == 'Education School':
	df, data_dict, schools, blocks = data_import_prep("Education School Data.json", 'Education School Data.csv')
# container for multiselect bar
with st.container():
	# display and take the input from the multiselect bar
	topics = st.multiselect('Choose the Topics of information', blocks)

	# initiate filter columns
	cols = []

	# taking all values from each topics into columns
	for t in topics:
		temp = list(data_dict[schools[0]][t].keys())
		for c in temp:
			cols.append(c)
# container for ranking filter
with st.container():
	# display slider 
	ranking = st.slider(
		'Ranking Range',
		value = [0,len(schools)]
		)

	# set range based on slider value
	filter_rank = schools[ranking[0]:ranking[1]]

# container for data display
with st.container():
	st.dataframe(df[cols].loc[filter_rank])


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df[cols].loc[filter_rank])

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Combined Business grad school info.csv',
    mime='text/csv'
)
