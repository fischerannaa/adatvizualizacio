import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data
data = {
    'Year': ['2010', '2011', '2012', '2013', '2014'],
    'Sales': [100, 150, 200, 250, 300]
}

# Create a DataFrame
df = pd.DataFrame(data).set_index('Year')

# Streamlit App
def main():
    st.title('Projekt')
    
    # Plotting
    st.subheader('Sales Trend')
    st.line_chart(df)
    
    # Discussion
    st.subheader('Discussion')
    st.write("The sales data shows a steady increase over the years. In 2010, sales were at $100, and by 2014, they had increased to $300. This indicates a positive growth trend for the company.")
    st.write("Factors contributing to this growth could include market demand, effective marketing strategies, and improvements in product quality.")
    st.write("However, it's important to note that without further analysis, we cannot attribute the entire increase to these factors. External factors such as economic conditions and competition may also have played a role.")
    st.write("Further analysis could involve comparing sales growth to industry benchmarks, conducting customer surveys, or examining sales data by region or product category.")

# Function to plot dat

if __name__ == "__main__":
    main()

    # streamlit run .\weboldal.py  inditas