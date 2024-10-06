import pandas as pd
import numpy as np
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)
# Load your data
df = pd.read_csv('co-emissions-per-capita.csv')

df = df[df['Annual CO₂ emissions (per capita)'] > 0]
df['Annual CO₂ emissions (per capita)_lag1'] = df['Annual CO₂ emissions (per capita)'].shift(1)
df['Annual CO₂ emissions (per capita)_lag2'] = df['Annual CO₂ emissions (per capita)'].shift(2)
df['MA_3'] = df['Annual CO₂ emissions (per capita)'].rolling(window=3).mean()
df.dropna(inplace=True)

cities = df['Entity'].unique().tolist()  # Assuming 'Country Name' is the city column

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_city = request.form['city']
        city_data = df[df['Entity'] == selected_city]
        
        # Plotting the chart
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=city_data, x='Year', y='Annual CO₂ emissions (per capita)')
        plt.title(f'CO₂ Emissions per Capita for {selected_city}')
        plt.xlabel('Year')
        plt.ylabel('CO₂ Emissions per Capita')
        chart_path = f'static/{selected_city}_chart.png'
        plt.savefig(chart_path)
        plt.close()

        return render_template('result.html', city=selected_city, chart_path=chart_path, table=city_data.to_html(classes='data', header=True, index=False))

    return render_template('index.html', cities=cities)

if __name__ == '__main__':
    app.run(debug=True)