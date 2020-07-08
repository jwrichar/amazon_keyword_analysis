import pandas as pd
from pandas import ExcelWriter
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

# Create title column in df:
df['title'] = product_info['title']

# TITLES:
# Token count matrix:
tokens_title = get_token_counts(product_info['title'])
# Document count:
tkn_doc_count_title = tokens_title.sum(
    axis=0).sort_values(
    ascending=False)

# bi-grams:
tokens_title_bi = get_token_counts(product_info['title'], ngrams=2)
tkn_doc_count_title_bi = tokens_title_bi.sum(
    axis=0).sort_values(
    ascending=False)

# FEATURES:
tokens_feat = get_token_counts(product_info['features'])
tkn_doc_count_feat = tokens_feat.sum(
    axis=0).sort_values(
    ascending=False)

# bi-grams
tokens_feat_bi = get_token_counts(product_info['features'], ngrams=2)
tkn_doc_count_feat_bi = tokens_feat_bi.sum(
    axis=0).sort_values(
    ascending=False)

# CATEGORY
print(product_info['category'].value_counts())


def save_dfs_as_xls(list_dfs, sheet_names, out_path):
    ''' Save list of DataFrames to single multi-sheet Excel file '''
    with ExcelWriter(out_path) as writer:
        for i, df in enumerate(list_dfs):
            df.to_excel(writer, sheet_names[i])
        writer.save()

to_save = [df,
           tkn_doc_count_title, tkn_doc_count_title_bi,
           tkn_doc_count_feat, tkn_doc_count_feat_bi]
sheet_names = ['Ad Perforance',
               'Title Terms',
               'Title Terms (bigrams)',
               'Feature Terms',
               'Feature Terms (bigrams)']

save_dfs_as_xls(to_save, sheet_names, 'data/amazon_ad_keywords.xlsx')
