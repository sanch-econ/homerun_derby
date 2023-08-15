''' Main hr_derby script'''

from classes import Schedule, Game, HomerunUpdater, DataframeGenerator
import streamlit as st

# Creates schedule object using start and end date.
sched = Schedule()

# Gets homeruns in schedule
hr_df = sched.create_hr_df()

# Updates homeruns.csv
HomerunUpdater.update(hr_df)

# Creates yearly df that will be displayed
yearly_df = DataframeGenerator.generate()

# Creates monthly df that will be displayed
monthly_df = DataframeGenerator.generate(monthly=True)

# Writes leadboard title to dashboard
st.write("# Leaderboards")

# Defines two equal sized columns for streamlit
col1, col2 = st.columns(2)

with col1:
    # Yearly Homeruns
    st.write('#### Yearly Homeruns')

    # Writes yearly df to dashboard
    st.dataframe(yearly_df, height=980)

with col2:
    # Monthly Homeruns
    st.write('#### Monthly Homeruns')

    # Writes montly df to dashboard
    st.dataframe(monthly_df, height=980)

    