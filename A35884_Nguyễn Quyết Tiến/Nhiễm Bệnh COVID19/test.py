import numpy as np
from fastapi import FastAPI, Response
import pandas as pd

app = FastAPI()

df = pd.read_csv("confirmed_data.csv")


confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
confirmed_df.set_index('Country/Region', inplace=True)

@app.get("/")
async def introduce_NguyenQuyetTien(description= "Đây là trang Swagger của Nguyễn Quyết Tiến"):
    return{"Đây là bài code của Nguyễn Quyết Tiến"}
@app.get("/confirmed_data/{country}/{start_col}/{end_col}")
async def get_confirmed_data(country: str, start_col: int, end_col: int):
    selected_cols = confirmed_df.loc[country, confirmed_df.columns[start_col:end_col]].to_dict()
    return selected_cols


@app.get("/Vietnam_min_max_confirmed")
async def vietnam_min_max_confirmed():
    vn_confirmed = confirmed_df[confirmed_df['Country/Region'] == 'Vietnam']
    vn_confirmed = vn_confirmed.drop(columns=['Province/State', 'Country/Region', 'Lat', 'Long'])
    min_confirmed = np.min(vn_confirmed.values)
    max_confirmed = np.max(vn_confirmed.values)
    results = {
        "min_confirmed": int(min_confirmed),
        "max_confirmed": int(max_confirmed)
    }
    return results

@app.post("/confirmed/country")
def get_country_confirmed(countries: list[str]):
    confirmed_data = df[df['Country'].isin(countries)]
    total_confirmed = confirmed_data.iloc[:, 4:].sum()

    return {"confirmed_cases": total_confirmed.to_dict()}

@app.get("/mean")
def calculate_mean(numbers: str):
    arr = np.array(numbers.split(','), dtype=int)
    return {"mean": np.mean(arr)}

