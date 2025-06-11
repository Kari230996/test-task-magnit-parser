import requests
import csv

url = "https://mobile-api.mm.ru/v2/goods/search"

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
    "Accept-Language": "de-DE;q=1.0, ru-DE;q=0.9, en-GB;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "User-Agent": "MagnitMarket/30.0.1 (Marketplace-technologies.KazanExpress; build:93109; iOS 18.5.0) Alamofire/5.5.0",
    "X-App-Version": "30.0.1",
    "X-Device-ID": "C44209F4-3632-4298-80D1-FE805BFD08F9",
    "X-Device-Platform": "iOS",
    "X-Device-Tag": "56062028-D970-4E40-AC09-A2D9D7F06487_9476BD69-D14D-4FCF-B54D-A2B452C2DB89",
    "X-Platform-Version": "18.5",
    "X-Request-Sign": "3637dc37ba20e7877d5a76d7f242f4f31aff045a5eeafa0127712cde8ca4404a19a200f7b9c98a684ac8490b78ff806865bd6bdaa1b22f5e66339a3632f20f2d"
}

data = {
    "includeAdultGoods": False,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzZWFyY2gtZ2F0ZXdheSIsImV4cCI6MTc0OTY3MzM2MiwiUHJvbW90aW9uU2t1R3JvdXBzIjpbNDM3MTg3MywzNzgwNDI0LDM3ODEwMDUsNDg0NTcyNiwzNzgwODM0LDQ4NDY1NTUsMzc4MDQyM10sImluc2VydGVkUHJvbW90aW9uSXRlbXMiOjcsInRvdGFsSW5zZXJ0ZWRQcm9tb3Rpb25JdGVtcyI6NywidG90YWxQcm9tb3Rpb25JdGVtcyI6OCwidG90YWxJdGVtcyI6MTN9.PUEoXbecQuhgqHFlvqm14lAZ3MXRfF0vrz7JhSekMjs",
    "pagination": {
        "offset": 20,
        "limit": 20
    },
    "categories": [
        12993
    ],
    "sort": {
        "type": "popularity",
        "order": "desc"
    },
    "storeType": "market",
    "catalogType": "4",
    "storeCode": "000",
    "cityId": "355"
}

response = requests.post(url, headers=headers, json=data)
print(f"🔁 Status code: {response.status_code}")

if response.status_code == 200:
    response_data = response.json()
    items = response_data.get("items", [])

    if items:
        filename = f"products_category_{data['categories'][0]}.csv"
        with open(f"products_category_{data['categories'][0]}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "regular_price", "promo_price"])

            for item in items:
                regular_price = item.get("promotion", {}).get("oldPrice")
                promo_price = item.get("price")
                name = item.get("name")

                writer.writerow([
                    item.get("id"),
                    name,
                    regular_price / 100 if regular_price else "",
                    promo_price / 100 if promo_price else "",

                ])
        print(f"✅ CSV создан: {filename}")
    else:
        print("❌ Нет товаров. Возможно, неверная категория или токен устарел.")
else:
    print("❌ Ошибка запроса:", response.text)
