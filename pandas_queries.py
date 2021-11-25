import pandas as pd
#import xlsx_reader

# queries table for product, check xlsx_reader_test.py to see how it should be run..

def product_query(df, query_product, PK):
    try:
        data = df[df[PK] == query_product]
        data = data.reset_index(drop=True)
        data = data.iloc[0, -1]
    except:
        #Product is not in the tables
        data = "Not Listed"
        return {query_product: data}
    if data <= 0:
        data = "Not Available"
        return {query_product: data}
    return {query_product: data}
def FT_TOP20(df, col_list):
    data = df.sort_values(by=col_list[-1], ascending=False)
    data = data.reset_index(drop=True)
    data = data.head(20)
    return data.to_json(orient='index')
def FT_TOP20_STACK(df_dict,col_list):
    key_list = list(df_dict.keys())
    data = pd.concat([df_dict[key_list[0]],df_dict[key_list[1]],df_dict[key_list[2]]])
    data = FT_TOP20(data, col_list)
    return data
