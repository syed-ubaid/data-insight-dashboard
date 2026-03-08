import pandas as pd
import numpy as np
import datetime

def generate_mock_data(rows=100):
    """
    Generates a mock dataset for business intelligence visualization.
    """
    np.random.seed(42)
    
    dates = [datetime.date(2023, 1, 1) + datetime.timedelta(days=i) for i in range(rows)]
    regions = ['North', 'South', 'East', 'West']
    products = ['SaaS Starter', 'SaaS Pro', 'Enterprise', 'Professional Services']
    
    data = {
        'Date': np.random.choice(dates, rows),
        'Region': np.random.choice(regions, rows),
        'Product': np.random.choice(products, rows),
        'Revenue': np.random.uniform(100, 5000, rows).round(2),
        'Units_Sold': np.random.randint(1, 100, rows),
        'Customer_Type': np.random.choice(['New', 'Returning', 'Dormant'], rows)
    }
    
    df = pd.DataFrame(data)
    df = df.sort_values(by='Date')
    return df

if __name__ == "__main__":
    df = generate_mock_data(200)
    print("Mock Data Sample:")
    print(df.head())
    df.to_csv('mock_business_data.csv', index=False)
    print("\nMock data saved to 'mock_business_data.csv'.")
