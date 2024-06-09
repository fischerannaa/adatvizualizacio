import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots

df = pd.read_csv("Arfolyam.csv")
df['Date'] = pd.to_datetime(df['Date'])

df['USD/BGN'] = pd.to_numeric(df['USD/BGN'], errors='coerce')
df['USD/HUF'] = pd.to_numeric(df['USD/HUF'], errors='coerce')
df['USD/EUR'] = pd.to_numeric(df['USD/EUR'], errors='coerce')

figCurrencyHistoryBgn = go.Figure()
figCurrencyHistoryBgn.add_trace(go.Scatter(x=df['Date'], y=df['USD/BGN'], mode='lines', name='USD/BGN', hoverinfo='y'))
figCurrencyHistoryBgn.update_layout(
    title='USD/BGN árfolyam alakulása',
    xaxis_title='Dátum',
    yaxis_title='Árfolyam',
    hovermode='x'
)

figCurrencyHistoryHuf = go.Figure()
figCurrencyHistoryHuf.add_trace(go.Scatter(x=df['Date'], y=df['USD/HUF'], mode='lines', name='USD/HUF', hoverinfo='y'))
figCurrencyHistoryHuf.update_layout(title='USD/HUF árfolyam alakulása',
                  xaxis_title='Dátum',
                  yaxis_title='Árfolyam',
                  hovermode='x')

figCurrencyHistoryEur = go.Figure()
figCurrencyHistoryEur.add_trace(go.Scatter(x=df['Date'], y=df['USD/EUR'], mode='lines', name='USD/EUR', hoverinfo='y'))
figCurrencyHistoryEur.update_layout(title='USD/EUR árfolyam alakulása',
                  xaxis_title='Dátum',
                  yaxis_title='Árfolyam',
                  hovermode='x')

figUnited = make_subplots(specs=[[{"secondary_y": True}]])
figUnited.add_trace(go.Scatter(x=df['Date'], y=df['USD/BGN'], mode='lines', name='USD/BGN', line=dict(color='#050C9C'), hoverinfo='y'))
figUnited.add_trace(go.Scatter(x=df['Date'], y=df['USD/HUF'], mode='lines', name='USD/HUF', line=dict(color='#3572EF'), hoverinfo='y'), secondary_y=True)
figUnited.add_trace(go.Scatter(x=df['Date'], y=df['USD/EUR'], mode='lines', name='USD/EUR', line=dict(color='#3ABEF9'), hoverinfo='y'))
figUnited.update_layout(title='Árfolyamok alakulása',
                  xaxis_title='Dátum',
                  yaxis_title='Árfolyam',
                  yaxis=dict(tickvals=[], ticktext=[]),
                  yaxis2=dict(tickvals=[], ticktext=[]))

dataDdp = pd.read_csv('GDP.csv', encoding='latin1')
dataDdp['Year'] = dataDdp['Year'].str.rstrip('*')
dataDdp['Year'] = pd.to_datetime(dataDdp['Year'])
dataDdp[['GER', 'HUN', 'BUL']] = dataDdp[['GER', 'HUN', 'BUL']].astype(str)
dataDdp[['GER', 'HUN', 'BUL']] = dataDdp[['GER', 'HUN', 'BUL']].apply(lambda x: x.str.replace(',', '').astype(float))

custom_palette = sns.color_palette(["#050C9C", "#3572EF", "#3ABEF9"])
sns.set_palette(custom_palette)

# GER GDP ábrázolása
fig_ger = go.Figure()
fig_ger.add_trace(go.Scatter(x=dataDdp['Year'], y=dataDdp['GER'], mode='lines+markers', name='GER GDP',
                             line=dict(color='#3ABEF9')))

# HUN GDP ábrázolása
fig_hun = go.Figure()
fig_hun.add_trace(go.Scatter(x=dataDdp['Year'], y=dataDdp['HUN'], mode='lines+markers', name='HUN GDP',
                             line=dict(color='#3572EF')))

# BUL GDP ábrázolása
fig_bul = go.Figure()
fig_bul.add_trace(go.Scatter(x=dataDdp['Year'], y=dataDdp['BUL'], mode='lines+markers', name='BUL GDP',
                             line=dict(color='#050C9C')))

# Előrejelzések hozzáadása
forecast_color = 'red'
forecast_years = dataDdp[dataDdp['Year'].dt.year >= 2023]['Year']
for fig in [fig_ger, fig_hun, fig_bul]:
    fig.add_trace(go.Scatter(x=forecast_years, y=dataDdp[fig.data[0].name.split()[0]][dataDdp['Year'].dt.year >= 2023],
                             mode='lines+markers', name=f'{fig.data[0].name} (Előrejelzés)',
                             line=dict(color=forecast_color, dash='dot')))

# Layout beállítása
for fig in [fig_ger, fig_hun, fig_bul]:
    fig.update_layout(title=f'{fig.data[0].name} alakulása', xaxis_title='Year', yaxis_title='GDP',
                      hovermode='x unified', hoverlabel=dict(bgcolor='#333333'))

# Inflation diagram
dataInflation = pd.read_csv('Inflation.csv', encoding='latin1')
dataInflation['Year'] = pd.to_datetime(dataInflation['Year'], format='%Y')
numeric_columns = dataInflation.columns[1:]
dataInflation[numeric_columns] = dataInflation[numeric_columns].apply(pd.to_numeric)

dfInlation = pd.DataFrame(dataInflation)

dfInlation['Year'] = pd.to_datetime(dfInlation['Year'])

custom_palette = sns.color_palette(["#83B4FF", "#1A2130", "#5A72A0"])
sns.set_palette(custom_palette)

fig = plt.figure(figsize=(10, 6))

# Set custom background color for the plot area
fig.patch.set_facecolor('#0e1117')  # Set the figure background color

ax = plt.gca()
ax.set_facecolor('#0e1117')  # Set the axes (plot area) background color

plt.fill_between(dfInlation['Year'], dfInlation['Bulgaria'], color='#FEB941', alpha=0.3, label='Bulgaria')
plt.fill_between(dfInlation['Year'], dfInlation['Germany'], color='#68D2E8', alpha=0.3, label='Germany')
plt.fill_between(dfInlation['Year'], dfInlation['Hungary'], color='#0A6847', alpha=0.3, label='Hungary')

ax.set_xlabel('Year', color='white')
ax.set_ylabel('Inflation Rate (%)', color='white')
ax.set_title('Inflation Rates of Bulgaria, Germany, and Hungary', color='white')
ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_edgecolor('white')

plt.grid(True, color='gray')
plt.tight_layout()

# Inflation comparison

figInflationComparison = go.Figure()

figInflationComparison.add_trace(go.Bar(x=dataInflation['Year'], y=dataInflation['Bulgaria'], name='Bulgaria', marker=dict(color='rgb(55, 83, 109)')))
figInflationComparison.add_trace(go.Bar(x=dataInflation['Year'], y=dataInflation['Hungary'], name='Hungary', marker=dict(color='rgb(26, 118, 255)')))
figInflationComparison.add_trace(go.Bar(x=dataInflation['Year'], y=dataInflation['Germany'], name='Germany', marker=dict(color='rgb(122, 193, 67)')))

figInflationComparison.add_trace(go.Bar(x=dataInflation['Year'], y=dataInflation['Euro area'], name='Euro area', marker=dict(color='rgb(249, 201, 35)')))
figInflationComparison.add_trace(go.Bar(x=dataInflation['Year'], y=dataInflation['European Union'], name='European Union', marker=dict(color='rgb(245, 96, 71)')))

figInflationComparison.update_layout(barmode='stack', title='Inflation Comparison', xaxis_title='Year', yaxis_title='Inflation Rate (%)',
                  hovermode='x unified', hoverlabel=dict(bgcolor='#333333'))

figInflationComparison.update_yaxes(range=[0, 60])

# Streamlit App
def main():
    st.title('Projekt')

    st.subheader('USD/BGN árfolyam alakulása')
    st.plotly_chart(figCurrencyHistoryBgn)
    
    st.subheader('USD/HUF árfolyam alakulása')
    st.plotly_chart(figCurrencyHistoryHuf)

    st.subheader('USD/EUR árfolyam alakulása')
    st.plotly_chart(figCurrencyHistoryEur)

    st.subheader('Árfolyamok alakulása')
    st.plotly_chart(figUnited)

    st.plotly_chart(fig_bul)
    st.plotly_chart(fig_hun)
    st.plotly_chart(fig_ger)

    
    st.pyplot(fig)

    
    st.plotly_chart(figInflationComparison)
    
    # Discussion
    st.subheader('Discussion')
    st.write("The sales data shows a steady increase over the years. In 2010, sales were at $100, and by 2014, they had increased to $300. This indicates a positive growth trend for the company.")
    st.write("Factors contributing to this growth could include market demand, effective marketing strategies, and improvements in product quality.")
    st.write("However, it's important to note that without further analysis, we cannot attribute the entire increase to these factors. External factors such as economic conditions and competition may also have played a role.")
    st.write("Further analysis could involve comparing sales growth to industry benchmarks, conducting customer surveys, or examining sales data by region or product category.")

# Function to plot dat

if __name__ == "__main__":
    main()


    # .\venv\Scripts\activate
    # streamlit run .\weboldal.py  inditas