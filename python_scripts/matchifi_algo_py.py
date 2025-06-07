import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from joblib import dump, load

#loads historical loan data to be used for model training
data_df=pd.read_excel('/content/drive/MyDrive/Loan.xlsx',header=2,)
data_df.head()

#defines the predictor and target variables for the model
x=data_df.drop(['Unnamed: 0','Company Name','Loan status'],axis=1)
y=data_df['Loan status']

# splits train data
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3, shuffle=True, random_state=50)

# fits ml model
model=LogisticRegression(C=10,penalty='l2',solver='saga',max_iter=10000)

pred_model=model.fit(x_train,y_train)

y_pred=pred_model.predict(x_test)
y_pred

#saves the trained model for reuse
dump(pred_model,'logistic_model.joblib')

accuracy=accuracy_score(y_test,y_pred)
print(accuracy)

# a function that takes in a dataframe of financial metrics and returns the possible outcome
def fetch_nd_recommend(df):

    for i in df.columns:
        if i=='Company Name':
            features=df.drop('Company Name',axis=1)
        else:
            features=df
    status=list(pred_model.predict(features))
    return status

# MODIFIED: load_data_from_db function (only the sql_query part shown)
def load_data_from_db(engine):
    sql_query = """
    SELECT
        cd.debt_to_eq AS client_debt_to_eq, -- From client_detail
        cd.gross_pm,                -- From client_detail
        cd.net_pm AS client_net_pm, -- From client_detail
        cd.return_on_assets,        -- From client_detail
        cd.return_on_equity,        -- From client_detail
        cd.interest_coverage,       -- From client_detail
    FROM
        loan_applications la
    JOIN
        clients c ON la.company_id = c.company_id
    JOIN
        client_detail cd ON la.company_id = cd.company_id
    JOIN
        sectors s ON cd.sector_id = s.sector_id
    JOIN
        loan_products lp ON la.product_id = lp.product_id;
    """
    data_df = pd.read_sql_query(sql_query, engine)
    print("Data loaded from database successfully.")
    return data_df

#model is fit using out-of-sample data to yield the outcome
pred_model.predict(data_df)

