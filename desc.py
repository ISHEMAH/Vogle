import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder




merged_df_500k = merged_df.head(500000) # type: ignore


print(merged_df.describe()) # type: ignore


merged_df = merged_df.fillna({ # type: ignore
    'order_amount': merged_df['order_amount'].mean(),
    'status': 'Unknown',  
    'email': 'Unknown',
    'phone_number': 'Unknown'  
})


merged_df = merged_df.drop_duplicates()


label_encoder = LabelEncoder()
merged_df['encoded_status'] = label_encoder.fit_transform(merged_df['status'])

# Normalize numeric columns
scaler = StandardScaler()
merged_df[['order_amount']] = scaler.fit_transform(merged_df[['order_amount']])  


merged_df['staff_order_ratio'] = merged_df['order_amount'] / (merged_df['staff_id'] + 1e-9)  
merged_df['email_domain'] = merged_df['email'].apply(lambda x: x.split('@')[1] if pd.notnull(x) else 'Unknown')


if 'date_of_birth' in merged_df.columns:
    merged_df['age'] = pd.to_datetime('today').year - pd.to_datetime(merged_df['date_of_birth']).dt.year

# Output some of the processed data
print(merged_df.head())

# If needed, export the processed data
merged_df.to_csv("processed_merged_data.csv", index=False)
