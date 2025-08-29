def data_filter(df, anime_title, filter_18=False, filter_rating=0.0): 

    if filter_18:
        df_filtered_18 = df[~df['18+']].reset_index(drop=True)
    else:
        df_filtered_18 = df.reset_index(drop=True)

    df_filtered_rating = df_filtered_18[df_filtered_18['Rating'] >= filter_rating].reset_index(drop=True)

    return df_filtered_rating