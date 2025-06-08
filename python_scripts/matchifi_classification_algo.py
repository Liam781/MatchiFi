
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from joblib import dump, load

import sys
from decimal import Decimal, InvalidOperation, getcontext
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
)

"""trains the classification model"""

data_df=pd.read_excel(r'C:\Users\ifb21-044\OneDrive - Botswana Accountancy College\Documents\FNBB hackathon\MatchiFi\Loan.xlsx',header=2)
print(data_df.head())

#defines the predictor and target variables for the model
x=data_df.drop(['Unnamed: 0','Company Name','Loan_Status'],axis=1)
y=data_df['Loan_Status']

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


class MatchiFiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MatchiFi - Check Application status")
        self.setGeometry(100, 100, 500, 500)

        self.layout = QVBoxLayout()

        # Input fields with labels
        self.layout.addWidget(QLabel("Enter debt to equity:"))
        self.debt_to_equity_input = QLineEdit()
        self.layout.addWidget(self.debt_to_equity_input)

        self.layout.addWidget(QLabel("Enter return on assets:"))
        self.return_on_assets_input = QLineEdit()
        self.layout.addWidget(self.return_on_assets_input)

        self.layout.addWidget(QLabel("Enter return on equity (P):"))
        self.return_on_equity_input = QLineEdit()
        self.layout.addWidget(self.return_on_equity_input)

        self.layout.addWidget(QLabel("Enter interest coverage ratio (P):"))
        self.interest_coverage_ratio_input = QLineEdit()
        self.layout.addWidget(self.interest_coverage_ratio_input)

        self.layout.addWidget(QLabel("Enter profit margin (P):"))
        self.profit_margin_input = QLineEdit()
        self.layout.addWidget(self.profit_margin_input)

        # Button
        self.predict_button = QPushButton("Get application status")
        self.predict_button.clicked.connect(self.make_prediction)
        self.layout.addWidget(self.predict_button)

        # Result display (multiline & scrollable)
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.layout.addWidget(self.result_display)

        self.setLayout(self.layout)
       
    def make_prediction(self):
        # Parse inputs safely as Decimals
       
        results_dict={
            'Debt_to_Equity':float(Decimal(self.debt_to_equity_input.text())),
            'Profit_Margin':float(Decimal(self.profit_margin_input.text())),
            'Return_on_Assets':float(Decimal(self.return_on_assets_input.text())),
            'Return_on_Equity':float(Decimal(self.return_on_equity_input.text())),
            'Interest_Coverage_Ratio':float(Decimal(self.interest_coverage_ratio_input.text()))
            }
            
        df=pd.DataFrame(results_dict,index=['0'])
        
        """out of sample data is fit to the trained model"""
        
        prediction=pred_model.predict(df)
            
        output_text = (
                "---Probable outcome of the loan application---\n"
                    )
        output_text += f"Application status: {prediction}"
        
        self.result_display.setPlainText(output_text)
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatchiFiApp()
    window.show()
    sys.exit(app.exec_())


