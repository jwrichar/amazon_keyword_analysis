import pandas as pd
from scrape import get_product_info
from tokenizer import get_token_counts

data_source = 'data/Sponsored_Products_adgroup_search_terms_Jul_6_2020.csv'

print('Loading data from %s' % data_source)
df = pd.read_csv(data_source)


def is_asin(s):
    if (len(s) == 10) and (s[0] == 'b') and len(s.split()) == 1:
        return True
    return False

df_asins = df.loc[df['Customer search term'].apply(is_asin)]

print('Getting info for all products')
product_info = df_asins['Customer search term'].apply(
    lambda x: pd.Series(get_product_info(x)))

# Token count matrix for titles:
tokens_title = get_token_counts(product_info['title'])

# Document count for titles
tkn_doc_count_title = (tokens_title > 0).sum(axis=0)
tkn_doc_count_title.sort_values(ascending=False)
tkn_doc_count_title.head(20)