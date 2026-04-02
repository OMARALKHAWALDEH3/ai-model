import pandas as pd

df1 = pd.read_csv("big_data.csv")
df2 = pd.read_csv("big_data_generated.csv")

df = pd.concat([df1, df2], ignore_index=True)

df.to_csv("big_data_final.csv", index=False)

print("✅ Final dataset ready!")
