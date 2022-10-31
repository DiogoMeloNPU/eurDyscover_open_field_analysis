import pandas as pd

def organizeDLCinfo(path_predictions_DLC):
    '''
    This function organizes the csv file contanining the DLC predictions for bodypart coordinates 
    (as well as label likelihood) into a more structured and easier to access dataframe.
    '''
    df_DLC = pd.read_csv(path_predictions_DLC)
    df_DLC = df_DLC.drop(columns='scorer')
    df_DLC.iloc[0] + ' ' + '(' + df_DLC.iloc[1] + ')'
    df_DLC.iloc[0] = df_DLC.iloc[0] + ' ' + '(' + df_DLC.iloc[1] + ')'
    df_DLC.drop(index=1)
    df_DLC.columns = df_DLC.iloc[0]
    df_DLC = df_DLC.drop(index=0)
    df_DLC = df_DLC.drop(index=1)
    df_DLC.reset_index(inplace = True, drop = True)
    for column in df_DLC.columns:
        df_DLC[column] = pd.to_numeric(df_DLC[column])

    return df_DLC #dataframe with the DLC predictions