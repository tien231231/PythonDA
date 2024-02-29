from fastapi import FastAPI, Response
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

app = FastAPI()

df = pd.read_csv("recoveries_data.csv")
#Tạo một DataFrame mới chỉ có 2 cột: Country và Total
country_column = df['Country']
totals = df.iloc[:, 561]
data_total = {'Country': country_column, 'Total': totals}
new_df = pd.DataFrame(data_total)
data_dict_backup=new_df.to_dict(orient="records")
@app.get("/")
async def introduce_TranMinhHai(description= "Đây là trang Swagger của Trần Minh Hải"):
    return{"Đây là bài code của Trần Minh Hải"}

# Tìm tổng số người khỏi bệnh trên toàn thế giới vào ngày 04/08/2021. Sử dụng Numpy
@app.get("/covid-recovery",description= "Tìm tổng số người khỏi bệnh trên toàn thế giới vào ngày 04/08/2021. Sử dụng Numpy")
async def covid_recovery():
    # Tính tổng số lần phục hồi toàn cầu bằng cách tính tổng trên tất cả các quốc gia và khu vực
    global_recoveries = np.sum(df.iloc[:, 561].values)
    #Trả về tổng số lần khôi phục toàn cầu dưới dạng từ điển

    return {"global_recoveries": int(global_recoveries)}
#Tìm quốc gia và tổng số ca khỏi bệnh theo ngày
@app.get("/filter_recovery_data",description= "Tìm quốc gia và tổng số ca khỏi bệnh theo ngày")
async def filter_recovery_data(country: str):
    filtered_df = df[df["Country"] == country]
    data = filtered_df.to_dict(orient="records")
    return {"data":data}
@app.get("/filter_recovery_total_dataJSON",description= "Tìm quốc gia với dữ liệu được cập nhật")
async def filter_recovery_total_dataJSON(country: str):
    for item in data_dict:
        if item["Country"] == country:
            return {"message": f"{country} có số ca khỏi bệnh do Covid 19 là {str(item['Total'])}"}
    return {"message": f"{country} not found"}
#Tìm quốc gia và tổng ca đã khỏi bệnh backup - Endpoint về Pandas
@app.get("/filter_recovery_total_data_backup",description= "Tìm quốc gia và tổng ca đã khỏi bệnh backup")
async def filter_recovery_total_data_backup(country: str):
    for item in data_dict_backup:
        if item["Country"] == country:
            return {"message": f"{country} có số ca khỏi bệnh do Covid 19 là {str(item['Total'])}"}

    return {"message": f"{country} not found"}
#Lưu dữ liệu vào file Json
data_file = "recovery_total_data.json"
with open(data_file) as f:
    data_dict = json.load(f)
# Cập nhật dữ liệu
@app.post("/update_total",description= "Cập nhật dữ liệu")
async def update_total(country: str, new_total: int):
    for item in data_dict:
        if item["Country"] == country:
            item["Total"] = new_total
            with open(data_file, "w") as f:
                json.dump(data_dict, f, indent=4)
        # return {"data":data_dict}
            return {"message": f"{country} có số ca khỏi bệnh do Covid 19 là {new_total}"}
    return {"message": f"{country} not found"}
#Tìm quốc gia với dữ liệu được cập nhật - Endpoint về Pandas

