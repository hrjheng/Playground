# https://goodinfo.tw/StockInfo/StockDividendPolicyList.asp
data_dividend = {}
n_years = 15
thisyear = 2019

for iyear in range(n_years):
    url = './dividend/DividendPolicyList_%d.html' %(thisyear-iyear)
    dfs = pd.read_html(url, encoding='big-5')
    df = pd.concat([df for df in dfs if df.shape[1] <= 20 and df.shape[1] > 5])
    df.columns = df.columns.map(str)

    col_names = ['市場','代碼','股票名稱','股利發放年度','股利所屬盈餘期間','股利所屬淨利(億)','股利所屬EPS(元)',
                 '股東股利-現金股利-盈餘(元/股)','股東股利-現金股利-公積(元/股)','股東股利-現金股利-合計(元/股)',
                 '股東股利-股票股利-盈餘(元/股)','股東股利-股票股利-公積(元/股)','股東股利-股票股利-合計(元/股)',
                 '股東股利-股利合計(元/股)','股東股利總計-現金(億)','股東股利總計-股票(張)','董監酬勞-合計(億)',
                 '董監酬勞-佔淨利(%)','員工紅利-現金(億)','員工紅利-股票(張)']

    for iname in range(len(col_names)):
        df.rename(columns={'%d' %(iname): col_names[iname]}, inplace=True)

    df.drop(df.head(3).index, inplace=True)
    df = df.reset_index(drop=True)

    print('parsing', (thisyear-iyear), len(df.index))

    df['股東股利-現金股利-盈餘(元/股)'] = pd.to_numeric(df['股東股利-現金股利-盈餘(元/股)'], 'coerce')
    df = df[~df['股東股利-現金股利-盈餘(元/股)'].isnull()]

    data_dividend['%d' %(thisyear-iyear)] = df


# data_dividend['2015']

for k in data_dividend.keys():
    data_dividend[k].index = data_dividend[k]['代碼']

df_dividend = pd.DataFrame({k:df_dividend['股東股利-現金股利-盈餘(元/股)'] for k, df_dividend in data_dividend.items()}).transpose()
df_dividend.index = pd.to_datetime(df_dividend.index)
df_dividend = df_dividend.sort_index()
df_dividend.columns = df_dividend.columns.map(str)

df_dividend

company = '0052'
# avg = 6
# df_dividend[company]
df_dividend[company].plot(label='Dividend',linewidth=3)
# df[company].rolling(avg).mean().plot(label='Moving average (%d months)' %(avg), linewidth=3)

plt.xlabel('Year', fontsize=15)
plt.ylabel('Annual dividend', fontsize=15)
plt.title('Annual dividend over the past %d years \n Company code: '%(n_years)+company,fontsize = 15)
plt.legend(loc='best',fontsize='x-large')
