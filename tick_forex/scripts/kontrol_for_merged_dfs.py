
def kontrol(first_df, sec_df, sec_df_column_to_lookup, column_to_check, checks: list):
    '''
    first_df arg must be dataframe consist of only one column and index
    :param first_df: yollanan dataframe 1
    :param sec_df: yollanan dataframe 2
    :param sec_df_column_to_lookup: lookup column name in second dataframe
    :param column_to_check: value column name in second dataframe
    :param checks: check edilecek value larin indexleri
    :return: True means no problem ,False means that 2 dataframe not merged properly,some values for same column value are different for dataframes
    '''
    for i in checks:
        if first_df[i] == sec_df.loc[sec_df[sec_df_column_to_lookup] == first_df.index[i], column_to_check].values[0]:
            continue
        else:
            return False
    return True
