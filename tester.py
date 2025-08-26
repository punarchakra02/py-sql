import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://neondb_owner:npg_EZ0FVkaeyv4t@ep-aged-salad-afq5e4ty-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

df = pd.read_csv("C:/Users/punar/Desktop/streamlit-app/data/customers.csv")
df.to_sql("customers", engine, if_exists="replace", index=False)

df = pd.read_csv("C:/Users/punar/Desktop/streamlit-app/data/geolocation.csv")
df.to_sql("geolocation", engine, if_exists="replace", index=False)

df = pd.read_csv("C:/Users/punar/Desktop/streamlit-app/data/order_items.csv")
df.to_sql("order_items", engine, if_exists="replace", index=False)

df = pd.read_csv("C:/Users/punar/Desktop/streamlit-app/data/orders.csv")
df.to_sql("orders", engine, if_exists="replace", index=False)

df = pd.read_csv("C:/Users/punar/Desktop/streamlit-app/data/payments.csv")
df.to_sql("payments", engine, if_exists="replace", index=False)

df = pd.read_csv("C:/Users/punar/Desktop/streamlit-app/data/products.csv")
df.to_sql("products", engine, if_exists="replace", index=False)

df = pd.read_csv("C:/Users/punar/Desktop/streamlit-app/data/sellers.csv")
df.to_sql("sellers", engine, if_exists="replace", index=False)