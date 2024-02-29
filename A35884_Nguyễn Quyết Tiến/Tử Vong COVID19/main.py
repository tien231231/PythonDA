from fastapi import FastAPI, Query
import pandas as pd
import numpy as np
import json

app = FastAPI()

#Tạo dataframe
df = pd.read_csv("death_data.csv")
country_column = df['Country']
totals = df.iloc[:, -1]
data_death_total = {'Country': country_column, 'Total': totals}
new_df = pd.DataFrame(data_death_total)
data_death_dict=new_df.to_dict(orient="records")
data_death_dict_backup=new_df.to_dict(orient="records")

#Lưu dữ liệu vào file Json
data_death_file = "death_total_data.json"
with open(data_death_file) as d:
    data_death_dict = json.load(d)
#Giới thiệu
@app.get("/")
async def introduce_NguyenQuyetTien(description= "Đây là trang Swagger của Nguyễn Quyết Tiến"):
    return{"Đây là bài code của Nguyễn Quyết Tiến"}
#GET
@app.get("/filter_death_data")
async def filter_death_data(country: str = Query(...)):
    filtered_df = df[df["Country"] == country]
    data = filtered_df.to_dict(orient="records")
    return {"data":data}

#POST
@app.post("/update_death_total")
async def update_death_total(country: str, new_total: int):
    for item in data_death_dict:
        if item["Country"] == country:
            item["Total"] = new_total
            with open(data_death_file, "w") as f:
                json.dump(data_death_dict, f, indent=4)
        # return {"data":data_dict}
            return {"message": f"{country} có số ca chết do Covid 19 là {new_total}"}
    return {"message": f"{country} not found"}

@app.post("/add_death_case")
async def add_death_case(country:str, add_case:int):
        for item in data_death_dict:
            if item["Country"] == country:
                item["Total"] += add_case
                with open(data_death_file, "w") as f:
                    json.dump(data_death_dict, f, indent=4)
                return {"message": f"{country} có số ca chết do Covid 19 là {str(item['Total'])}"}

#NUMPY        
@app.get("/highest_cases_country")
def get_highest_cases_country():
    latest_date = df.columns[-1]
    column_data = df[latest_date].values 
    highest_cases_idx = np.argmax(column_data)
    highest_cases_country = df.loc[highest_cases_idx, 'Country']
    return {"Đất nước có số người chết nhiều nhất là: ": highest_cases_country}
       
#PANDAS
@app.get("/filter_death_total_dataJSON")
async def filter_death_total_dataJSON(country: str):
    for item in data_death_dict:
        if item["Country"] == country:
            return {"message": f"{country} có số ca chết do Covid 19 là {str(item['Total'])}"}
    return {"message": f"{country} not found"}



