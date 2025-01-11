from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt 
import seaborn as sns 

MLFLOW_TRACKING_URI='http://localhost:5000'
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

wine = load_wine()

X = wine.data
y = wine.target

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.10, random_state=42)

max_depth = 10
n_estimators = 5

with mlflow.start_run():
    rf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    rf.fit(X_train,y_train)
    
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test,y_pred)
    
    mlflow.log_metric('accuracy',accuracy)
    mlflow.log_param('max_depth',max_depth)
    mlflow.log_param('n_estimators',n_estimators)
    
    
    cm = confusion_matrix(y_test,y_pred)
    plt.figure(figsize=(6,6))
    sns.heatmap(cm, annot=True, xticklabels=wine.target_names,yticklabels=wine.target_names)
    plt.xlabel('predicted')
    plt.ylabel('actual')
    plt.title('confusion matrix')
    
    plt.savefig('confusion_matrix.png')
    
    mlflow.log_artifact('confusion_matrix.png')
    mlflow.log_artifact(__file__)
    
    print(accuracy)
    