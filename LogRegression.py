import pandas as pd
from sklearn import datasets, linear_model, metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

earnings = pd.read_csv('Earnings.csv')
# print(earnings)

X = pd.DataFrame(columns=['Earnings','Surprise','Volume','ReportTime','OvernightChange'])
Y = pd.DataFrame(columns=['Change','Binary'])

formatEarnings = lambda x: 1 if x > 0 else 0
formatSurprise = lambda x: 1 if x > 0 and x < 100 else 0
formatVolume = lambda x: 1 if x > 5000000 else 0
formatReportTime = lambda x: 1 if x == "AMC" else 0
formatOvernightChange = lambda x: 1 if x > 1 else 0
formatY = lambda x: 1 if x > 1 else 0

X['Earnings'] =  earnings['Earnings'] / earnings['Open After Earnings']
X['Surprise'] = earnings['Earnings Surprise (%)']
X['Volume'] = earnings['Volume Before Earnings'] * earnings['Close Before Earnings']
X['Volume'] = X['Volume'].map(formatVolume)
X['ReportTime'] = earnings['Report Time'].map(formatReportTime)
X['OvernightChange'] = earnings['Open After Earnings'] / earnings['Close Before Earnings']
# X['OvernightChange'] = X['OvernightChange'].map(formatOvernightChange)

Y['Change'] = earnings['Close After Earnings'] / earnings['Open After Earnings']
Y['Binary'] = Y['Change'].map(formatY)

X, Y = shuffle(X, Y)

# print(X)

# print(X.values)
# print(Y.values)

X_train, X_test, y_train, y_test = train_test_split(X.values, Y.values, test_size=0.01)
model = linear_model.LogisticRegression(C = 1.0, penalty='l2', solver='lbfgs')
y_train = [i[1] for i in y_train]
model.fit(X_train,y_train)

y_predict = model.predict(X_test)

right = 0
mult = 1

for i in range(len(y_test)):
    if y_predict[i] == y_test[i][1]:
        right += 1
    if y_predict[i] == 1:
        mult *= y_test[i][0]
        print(y_test[i][0])

print(right)
print(len(y_test))
print(right/len(y_test))
print(mult)