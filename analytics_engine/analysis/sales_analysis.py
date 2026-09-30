from data.data import sales_data
import pandas as pd

#Metrics 
total_revenue = sales_data['total'].sum()
tota_unit_sold = sales_data['quantity'].sum()
most_selling_size = sales_data['size'].value_counts().idxmax()
no_of_sold_unit_each_size = sales_data.groupby('size')['quantity'].sum()
revenue_generated_by_each_product = sales_data.groupby('pname')['price'].sum()

#Insight 


