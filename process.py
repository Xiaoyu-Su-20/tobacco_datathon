import pandas as pd

from utils import get_all_countries


data_folder_name = "data"

df_sales = pd.read_csv(f"{data_folder_name}/sales_per_day.csv")
df_production = pd.read_csv(f"{data_folder_name}/tobacco_production.csv")
df_popularity = pd.read_csv(f"{data_folder_name}/tobacco_use_ww.csv")
df_policy = pd.read_csv(f"{data_folder_name}/stop_smoking.csv")

# get the unique countries to see the mergability of the countries
print("sales data")
df_sales = get_all_countries(df_sales, "Entity", "Code")

print("production data")
df_production = get_all_countries(df_production, "Country or Area")

print("popularity data")
df_popularity = get_all_countries(df_popularity, "Location", "SpatialDimValueCode")

print("policy data")
df_policy = get_all_countries(df_policy, "Entity", "Code")

# first merge
df_merge = df_policy.merge(
    df_popularity, how="left", left_on="Code", right_on="SpatialDimValueCode"
)
print(f"The initial number of countries for policy: {len(df_merge)}")
print(
    f"How many countries are joinable from the popularity dataset:\
    {len(df_merge[df_merge['SpatialDimValueCode'].notnull()])}"
)

# second merge
df_merge = df_merge.merge(
    df_production, how="left", left_on="Entity", right_on="Country or Area"
)
print(
    f"How many countries are joinable from the production dataset:\
    {len(df_merge[df_merge['Country or Area'].notnull()])}"
)

# third merge
df_merge = df_merge.merge(df_sales, how="left", left_on="Code", right_on="Code")
print(
    f"How many countries are joinable from the sales dataset:\
    {len(df_merge[df_merge['Entity_y'].notnull()])}"
)

# find out which countries are not joinable
production_set = set(df_merge["Country or Area"])
print("The unjoinable countries from production dataset:")
print(df_production[~df_production["Country or Area"].isin(production_set)])


sales_set = set(df_merge["Entity_y"])
print("The unjoinable countries from sales dataset:")
print(df_sales[~df_sales["Entity"].isin(sales_set)])


df_merge.to_csv("df_merge.csv", index=False)
