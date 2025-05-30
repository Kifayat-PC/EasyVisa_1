# -*- coding: utf-8 -*-
"""GL project K1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15JRT1w8GcqUuwI13JlZPcAcdjrrD28bw

```

# EasyVisa - Problem Statement

### Problem Statement

The increasing demand for skilled professionals in the U.S. has led to a surge in visa applications, making the manual review process inefficient. The Office of Foreign Labor Certification (OFLC) processes thousands of applications annually, requiring a data-driven approach for efficiency. Identifying key factors influencing visa approvals is essential to streamline decision-making. The challenge lies in predicting visa outcomes accurately while ensuring compliance with labor laws. A machine learning model can assist in automating the process, reducing manual workload. This study aims to develop a predictive model to classify visa applications as approved or denied.

### Data Dictionary

The data contains the different attributes of the employee and the employer. The detailed data dictionary is given below.
- case_id: ID of each visa application
- continent: Information of continent the employee
- education_of_employee: Information of education of the employee
- has_job_experience: Does the employee have any job experience? Y= Yes; N = No
- requires_job_training: Does the employee require any job training? Y = Yes; N = No
- no_of_employees: Number of employees in the employer's company
- yr_of_estab: Year in which the employer's company was established
- region_of_employment: Information of foreign worker's intended region of employment in the US.
- prevailing_wage: Average wage paid to similarly employed workers in a specific occupation in the area of intended employment. The purpose of the prevailing wage is to ensure that the foreign worker is not underpaid compared to other workers offering the same or similar service in the same area of employment.
- unit_of_wage: Unit of prevailing wage. Values include Hourly, Weekly, Monthly, and Yearly.
- full_time_position: Is the position of work full-time? Y = Full-Time Position; N = Part-Time Position
- case_status: Flag indicating if the Visa was certified or denied

##Objective
This project aims to analyze visa application data to identify factors affecting approvals. By applying machine learning techniques, we seek to develop a classification model for visa approval prediction. Various models, including Decision Trees, Random Forest, and Boosting techniques, will be implemented and compared. Hyperparameter tuning will be performed to optimize model performance. The best-performing model will be selected based on accuracy and other key metrics. Insights from the analysis will be used to recommend strategies for improving the visa approval process.

### Let us start by importing the required libraries
"""

# Write your code here to import necessary libraries for the project
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

"""### Understanding the structure of the data"""

# from google.colab import drive
# drive.mount('/content/drive')
from google.colab import drive
drive.mount('/content/drive')

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/EasyVisa.csv'
data = pd.read_csv(file_path)

"""#Data Overview

Displaying the first few rows of the dataset
"""

data.head()

"""Checking the shape of the dataset"""

data.shape

"""Checking the data types of the columns for the dataset"""

print(data.info())

"""Statistical summary of the dataset"""

data.describe()

"""# Check for missing values and basic statistics:"""

#  Check for missing values
missing_values = data.isnull().sum()
print("Missing Values:\n", missing_values)

"""Therefore there are no missing values

## Univariate and Bivariate analysis
"""

# Set visual style
sns.set(style="whitegrid")

# Plot case_status distribution
plt.figure(figsize=(6, 4))
sns.countplot(data=data, x="case_status", palette="coolwarm")
plt.title("Distribution of Visa Case Status")
plt.xlabel("Case Status")
plt.ylabel("Count")
plt.show()

# Education level distribution
plt.figure(figsize=(10, 4))
sns.countplot(data=data, y="education_of_employee", order=data["education_of_employee"].value_counts().index, palette="viridis")
plt.title("Distribution of Education Levels")
plt.xlabel("Count")
plt.ylabel("Education Level")
plt.show()

"""## Observations from Univariate Analysis:
Visa Case Status Distribution
- The dataset has a mix of Certified and Denied visa applications.
- There may be class imbalance, which we will analyze further.

Education Level Distribution
- Most applicants hold Bachelor's or Master’s degrees.
- High school and Doctorate applicants are in the minority.

"""

# Group by education level and calculate certification rate
edu_cert_rate = data.groupby("education_of_employee")["case_status"].value_counts(normalize=True).unstack() * 100

# Plot visa approval rates by education level
plt.figure(figsize=(10, 5))
edu_cert_rate.plot(kind="bar", stacked=True, colormap="coolwarm", alpha=0.85)
plt.title("Visa Certification Rate by Education Level")
plt.xlabel("Education Level")
plt.ylabel("Percentage (%)")
plt.legend(["Denied", "Certified"], title="Case Status")
plt.xticks(rotation=45)
plt.show()

# Group by continent and calculate certification rate
cont_cert_rate = data.groupby("continent")["case_status"].value_counts(normalize=True).unstack() * 100

# Plot visa approval rates by continent
plt.figure(figsize=(10, 5))
cont_cert_rate.plot(kind="bar", stacked=True, colormap="viridis", alpha=0.85)
plt.title("Visa Certification Rate by Continent")
plt.xlabel("Continent")
plt.ylabel("Percentage (%)")
plt.legend(["Denied", "Certified"], title="Case Status")
plt.xticks(rotation=45)
plt.show()

"""##Insights from Bivariate Analysis:
Education Level and Visa Certification
- Applicants with higher education (Master’s and Doctorate) have higher certification rates.
- High School graduates face the most rejections, possibly due to skill shortages.

Continent-wise Visa Certification
- North America and Europe have the highest approval rates.
- Africa and Asia see more denials, indicating possible stricter regulations or documentation issues.
"""

# Group by job experience and calculate certification rate
exp_cert_rate = data.groupby("has_job_experience")["case_status"].value_counts(normalize=True).unstack() * 100

# Plot visa approval rates by job experience
plt.figure(figsize=(6, 4))
exp_cert_rate.plot(kind="bar", stacked=True, colormap="coolwarm", alpha=0.85)
plt.title("Visa Certification Rate by Job Experience")
plt.xlabel("Has Job Experience")
plt.ylabel("Percentage (%)")
plt.legend(["Denied", "Certified"], title="Case Status")
plt.xticks(rotation=0)
plt.show()

"""####Insights on Job Experience and Visa Certification
- Applicants with job experience have a higher chance of visa approval.
- Freshers (No experience) face more rejections, possibly due to skill gaps.
"""

# Group by pay unit and calculate certification rate
wage_cert_rate = data.groupby("unit_of_wage")["case_status"].value_counts(normalize=True).unstack() * 100

# Plot visa approval rates by pay unit
plt.figure(figsize=(8, 4))
wage_cert_rate.plot(kind="bar", stacked=True, colormap="viridis", alpha=0.85)
plt.title("Visa Certification Rate by Pay Unit")
plt.xlabel("Pay Unit")
plt.ylabel("Percentage (%)")
plt.legend(["Denied", "Certified"], title="Case Status")
plt.xticks(rotation=0)
plt.show()

"""####Insights on Pay Unit and Visa Certification
- Yearly wage offers have the highest approval rates, indicating that stable, long-term positions are preferred.
- Hourly wage applicants face the most denials, possibly due to job type instability or lower wages.
"""

# Boxplot of prevailing wage by case status
plt.figure(figsize=(8, 5))
sns.boxplot(data=data, x="case_status", y="prevailing_wage", palette="coolwarm")
plt.ylim(0, data["prevailing_wage"].quantile(0.95))
plt.title("Prevailing Wage vs Visa Status")
plt.xlabel("Case Status")
plt.ylabel("Prevailing Wage")
plt.show()

plt.figure(figsize=(10, 5))
sns.boxplot(x=data["case_status"], y=data["prevailing_wage"], palette="Set2")
plt.yscale("log")
plt.title("Prevailing Wage Distribution by Visa Status")
plt.xlabel("Visa Status (0 = Certified, 1 = Denied)")
plt.ylabel("Prevailing Wage (Log Scale)")
plt.show()

"""####Insights on Prevailing Wage and Visa Certification
- Certified visas generally have higher prevailing wages than denied ones.
- Lower-wage applications see more denials, possibly due to concerns about labor market impact.
"""

sns.set(style="whitegrid")

# Calculate proportion
visa_counts = data["case_status"].value_counts(normalize=True) * 100
print("Visa Approval Rates:\n", visa_counts)

#Are certain U.S. regions more favorable?
plt.figure(figsize=(12, 6))
region_vs_visa = data.groupby("region_of_employment")["case_status"].value_counts(normalize=True).unstack()
region_vs_visa.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="viridis")
plt.title("Visa Approval Rates by U.S. Region")
plt.ylabel("Proportion of Applications")
plt.xlabel("Region of Employment")
plt.legend(["Certified", "Denied"])
plt.xticks(rotation=45)
plt.show()

#Does requiring job training impact visa approvals?
plt.figure(figsize=(6, 4))
sns.countplot(x=data["requires_job_training"], hue=data["case_status"], palette="Set1")
plt.title("Impact of Job Training Requirement on Visa Status")
plt.xlabel("Requires Job Training (Y/N)")
plt.ylabel("Count")
plt.legend(["Certified", "Denied"])
plt.show()

#Work Experience + No Training Requirement
plt.figure(figsize=(6, 4))
sns.barplot(x=data["has_job_experience"], y=data["case_status"], hue=data["requires_job_training"], palette="coolwarm")
plt.title("Work Experience, Training & Visa Approval")
plt.ylabel("Denial Rate")
plt.xlabel("Has Job Experience (Y/N)")
plt.legend(["No Training Required", "Training Required"])
plt.show()

#Interaction Between Wage Levels & Education
plt.figure(figsize=(10, 5))
sns.boxplot(x=data["education_of_employee"], y=data["prevailing_wage"], hue=data["case_status"], showfliers=False, palette="coolwarm")
plt.yscale("log")
plt.title("Salary & Education Influence on Visa Approval")
plt.xlabel("Education Level")
plt.ylabel("Prevailing Wage (Log Scale)")
plt.legend(["Certified", "Denied"])
plt.xticks(rotation=45)
plt.show()

# Full-Time vs. Part-Time Positions
plt.figure(figsize=(6, 4))
sns.countplot(x=data["full_time_position"], hue=data["case_status"], palette="viridis")
plt.title("Impact of Full-Time vs. Part-Time Work on Visa Approval")
plt.xlabel("Full-Time Position (Y/N)")
plt.ylabel("Count")
plt.legend(["Certified", "Denied"])
plt.show()

# Checking the Spread of Company Size
plt.figure(figsize=(8, 5))
sns.boxplot(x=data["no_of_employees"], color="green")
plt.title("Boxplot of Company Size (No. of Employees)")
plt.xlabel("Number of Employees")
plt.show()

"""# Correlation Check"""

data_encoded = data.copy()

# Encoding categorical variables for correlation analysis
data_encoded["has_job_experience"] = data_encoded["has_job_experience"].map({"Y": 1, "N": 0})
data_encoded["requires_job_training"] = data_encoded["requires_job_training"].map({"Y": 1, "N": 0})
data_encoded["full_time_position"] = data_encoded["full_time_position"].map({"Y": 1, "N": 0})
data_encoded["case_status"] = data_encoded["case_status"].map({"Certified": 1, "Denied": 0})

# Dropped non-numeric columns before correlation analysis
numeric_data = data_encoded.select_dtypes(include=["number"])

correlation_matrix = numeric_data.corr()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix of Features")
plt.show()


plt.figure(figsize=(8, 5))
sns.histplot(data["prevailing_wage"], bins=50, kde=True, color="blue")
plt.title("Distribution of Prevailing Wage")
plt.xlabel("Prevailing Wage")
plt.ylabel("Count")
plt.show()

"""#  Outlier Detection & Treatment"""

# Plot boxplots to detect outliers
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Prevailing Wage Outliers
sns.boxplot(data=data, y="prevailing_wage", ax=axes[0], palette="coolwarm")
axes[0].set_title("Boxplot of Prevailing Wage")

# Number of Employees Outliers
sns.boxplot(data=data, y="no_of_employees", ax=axes[1], palette="viridis")
axes[1].set_title("Boxplot of Number of Employees")

plt.tight_layout()
plt.show()


# Capping outliers at 95th percentile
wage_cap = data["prevailing_wage"].quantile(0.95)
emp_cap = data["no_of_employees"].quantile(0.95)

data["prevailing_wage"] = data["prevailing_wage"].clip(upper=wage_cap)
data["no_of_employees"] = data["no_of_employees"].clip(upper=emp_cap)

# Verify outlier treatment with updated boxplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(data=data, y="prevailing_wage", ax=axes[0], palette="coolwarm")
axes[0].set_title("Boxplot of Prevailing Wage (After Outlier Treatment)")
sns.boxplot(data=data, y="no_of_employees", ax=axes[1], palette="viridis")
axes[1].set_title("Boxplot of Number of Employees (After Outlier Treatment)")
plt.tight_layout()
plt.show()

"""####Outlier Treatment :
- The extreme outliers have been capped at the 95th percentile.
This prevents extreme values from skewing the model.

# Train Test split
"""

from sklearn.model_selection import train_test_split

# Define features and target variable
X = data.drop(columns=["case_id", "case_status"])
y = data["case_status"]

# Split data into 80% train and 20% test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Confirm the split
X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""# Decision Tree Model

###Data Preprocessing
"""

from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ea copy of X_train and X_test
X_train_encoded = X_train.copy()
X_test_encoded = X_test.copy()

# Identify categorical columns
categorical_cols = X_train_encoded.select_dtypes(include=["object"]).columns

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X_train_encoded[col] = le.fit_transform(X_train_encoded[col])
    X_test_encoded[col] = le.transform(X_test_encoded[col])
    label_encoders[col] = le

dt_confusion_matrix = confusion_matrix(y_test, y_pred_dt)

print("\nConfusion Matrix for Basic Decision Tree:\n", dt_confusion_matrix)

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Denied", "Certified"], yticklabels=["Denied", "Certified"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(title)
    plt.show()

plot_confusion_matrix(y_test, y_pred_dt, "Confusion Matrix: Initial Decision Tree")

"""###Train a Decision Tree Using Entropy"""

# Train Decision Tree Classifier using entropy
dt_model_entropy = DecisionTreeClassifier(criterion="entropy", random_state=42)
dt_model_entropy.fit(X_train_encoded, y_train)

# Predictions on Test Data
y_pred_dt = dt_model_entropy.predict(X_test_encoded)

# itsPerformance
dt_accuracy = accuracy_score(y_test, y_pred_dt)
dt_classification_report = classification_report(y_test, y_pred_dt)
dt_confusion_matrix = confusion_matrix(y_test, y_pred_dt)

# Display results
print(f"Decision Tree Accuracy: {dt_accuracy:.4f}")
print("\nClassification Report:\n", dt_classification_report)
print("\nConfusion Matrix:\n", dt_confusion_matrix)

"""###Hyperparameter Tuning"""

from sklearn.model_selection import GridSearchCV

# parameter grid for hyperparameter tuning
param_grid = {
    "criterion": ["gini", "entropy"],
    "max_depth": [3, 5, 10, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 5, 10]
}

dt = DecisionTreeClassifier(random_state=42)

# Grid Search Cross-Validation
grid_search = GridSearchCV(dt, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid_search.fit(X_train_encoded, y_train)

#  parameters
print("Best Hyperparameters:", grid_search.best_params_)

# Train model with best parameters
best_dt_model = grid_search.best_estimator_

# Predictions on test data (Best Model)
y_pred_best = best_dt_model.predict(X_test_encoded)

# Evaluate Model Performance (Best Model)
best_accuracy = accuracy_score(y_test, y_pred_best)
print(f"Best Model Accuracy: {best_accuracy:.4f}")

plot_confusion_matrix(y_test, y_pred_best, "Confusion Matrix: Best Tuned Model")

"""### Checking this for Overfitting

"""

train_accuracy = dt_model_entropy.score(X_train_encoded, y_train)
test_accuracy = dt_model_entropy.score(X_test_encoded, y_test)

print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

if train_accuracy > test_accuracy:
    print("Overfitting detected! Consider pruning the tree.")

"""###Pruning the Decision Tree to Reduce Overfitting"""

# Regularized Decision Tree (Pruned)
clf_pruned = DecisionTreeClassifier(criterion="entropy", random_state=42, max_depth=3, min_samples_leaf=5)
clf_pruned.fit(X_train_encoded, y_train)

# Predictions after pruning
preds_pruned = clf_pruned.predict(X_test_encoded)
preds_pruned_train = clf_pruned.predict(X_train_encoded)

# Performance Evaluation
print("Pruned Model Accuracy (Test Data):", accuracy_score(y_test, preds_pruned))
print("Pruned Model Accuracy (Train Data):", accuracy_score(y_train, preds_pruned_train))

plot_confusion_matrix(y_test, preds_pruned, "Confusion Matrix: Pruned Model")

"""observatins:
-  Pruning reduces overfitting but might lower accuracy.
- If train_accuracy >> test_accuracy, the model is still overfitting.

###Visualizing the Pruned Decision Tree
"""

import graphviz
import pydotplus
from six import StringIO
from IPython.display import Image
from sklearn.tree import export_graphviz

feature_cols = X_train_encoded.columns

dot_data = StringIO()
export_graphviz(clf_pruned, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True, feature_names=feature_cols, class_names=['Denied', 'Certified'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())

"""### Calculating Precision & Recall"""

from sklearn.metrics import precision_score, recall_score

# Conveting categorical labels to numeric:
y_test_numeric = y_test.map({'Certified': 1, 'Denied': 0})
preds_pruned_numeric = [1 if label == 'Certified' else 0 for label in preds_pruned]

# precisioning and recalling
precision = precision_score(y_test_numeric, preds_pruned_numeric)
recall = recall_score(y_test_numeric, preds_pruned_numeric)

print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")

"""# OTHER MODELS ;

### Bagging - Random Forest Model
"""

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_encoded, y_train)
y_pred_rf = rf.predict(X_test_encoded)

print("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))
print("Classification Report:\n", classification_report(y_test, y_pred_rf))
plot_confusion_matrix(y_test, y_pred_rf, "Random Forest Confusion Matrix")

"""### hyperparameter tuning :"""

rf_params = {
    'n_estimators': [50, 100],
    'max_depth': [10, 20],
    'min_samples_split': [5, 10],
}
from sklearn.model_selection import RandomizedSearchCV
rf_random = RandomizedSearchCV(RandomForestClassifier(random_state=42), rf_params,
                               cv=3, scoring='accuracy', n_iter=5, n_jobs=-1, random_state=42)
rf_random.fit(X_train_encoded, y_train)
rf_grid = GridSearchCV(RandomForestClassifier(random_state=42), rf_params, cv=3, scoring='accuracy', n_jobs=2)

"""### Boosting - XGBoost Model"""

# Convert labels to numerical values
y_train_encoded = y_train.map({"Certified": 1, "Denied": 0})
y_test_encoded = y_test.map({"Certified": 1, "Denied": 0})

# Train XGBoost
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb.fit(X_train_encoded, y_train_encoded)

# Predictions
y_pred_xgb = xgb.predict(X_test_encoded)

print("XGBoost Accuracy:", accuracy_score(y_test_encoded, y_pred_xgb))
print("\nClassification Report:\n", classification_report(y_test_encoded, y_pred_xgb))
print("\nConfusion Matrix:\n", confusion_matrix(y_test_encoded, y_pred_xgb))

xgb_params = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2]
}


xgb_grid = GridSearchCV(
    XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
    xgb_params, cv=3, scoring='accuracy', n_jobs=-1
)

# Fit the model with encoded y_train
xgb_grid.fit(X_train_encoded, y_train_encoded)

# Predictions on test set
y_pred_xgb_tuned = xgb_grid.best_estimator_.predict(X_test_encoded)

# Evaluatng the model
xgb_accuracy = accuracy_score(y_test_encoded, y_pred_xgb_tuned)
xgb_conf_matrix = confusion_matrix(y_test_encoded, y_pred_xgb_tuned)
xgb_class_report = classification_report(y_test_encoded, y_pred_xgb_tuned)

# Display results
print(f"XGBoost Tuned Accuracy: {xgb_accuracy:.4f}")
print("\nClassification Report:\n", xgb_class_report)
print("\nConfusion Matrix:\n", xgb_conf_matrix)

"""### Boosting - AdaBoost Model"""

adaboost = AdaBoostClassifier(n_estimators=100, random_state=42)
adaboost.fit(X_train_encoded, y_train)
y_pred_ada = adaboost.predict(X_test_encoded)

print("AdaBoost Accuracy:", accuracy_score(y_test, y_pred_ada))
print("Classification Report:\n", classification_report(y_test, y_pred_ada))
plot_confusion_matrix(y_test, y_pred_ada, "AdaBoost Confusion Matrix")

"""### Boosting - Gradient Boosting Model"""

gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
gb.fit(X_train_encoded, y_train)
y_pred_gb = gb.predict(X_test_encoded)

print("Gradient Boosting Accuracy:", accuracy_score(y_test, y_pred_gb))
print("Classification Report:\n", classification_report(y_test, y_pred_gb))
plot_confusion_matrix(y_test, y_pred_gb, "Gradient Boosting Confusion Matrix")

"""#  Comparing All Models used until now in the above"""

def evaluate_model(model, X_train, X_test, y_train, y_test):
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Print unique values
    print(f"Unique values in y_test_pred: {set(y_test_pred)}")

    # Check if predictions are strings or numbers
    if isinstance(list(y_test_pred)[0], str):
        label_map = {"Certified": 1, "Denied": 0}
    else:
        label_map = {1: 1, 0: 0}

    # Convert predictions to numeric labels
    y_train_pred_encoded = pd.Series(y_train_pred).map(label_map).fillna(999)
    y_test_pred_encoded = pd.Series(y_test_pred).map(label_map).fillna(999)

    # Check for invalid values
    if 999 in y_train_pred_encoded.values or 999 in y_test_pred_encoded.values:
        raise ValueError(f"Model {model} produced unexpected labels!")

    return {
        "Train Accuracy": accuracy_score(y_train, y_train_pred_encoded),
        "Test Accuracy": accuracy_score(y_test, y_test_pred_encoded),
        "Precision": precision_score(y_test, y_test_pred_encoded),
        "Recall": recall_score(y_test, y_test_pred_encoded),
        "F1 Score": f1_score(y_test, y_test_pred_encoded),
    }

# Evaluate all models
results = {name: evaluate_model(model, X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded)
           for name, model in models.items()}

# Evaluate all models
results = {name: evaluate_model(model, X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded)
           for name, model in models.items()}

# Convert results into a DataFrame
comparison_df = pd.DataFrame.from_dict(results, orient="index")

# Plot comparison of accuracy, precision, recall, and F1-score
plt.figure(figsize=(12, 6))
comparison_df.plot(kind="bar", figsize=(12, 6), colormap="coolwarm")

plt.title("Model Performance Comparison")
plt.ylabel("Score")
plt.xlabel("Model")
plt.xticks(rotation=45)
plt.legend(loc="lower right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show the plot
plt.show()

"""##Observations from the Model Performance Comparison Graph
- Overfitting in Decision Trees:
The Decision Tree model has a very high training accuracy (~100%) but significantly lower test accuracy, indicating overfitting.
This means the model memorized the training data but generalizes poorly to unseen data.

- Pruned Decision Tree Improves Generalization: The Pruned Decision Tree has lower training accuracy but better test accuracy compared to the unpruned tree, reducing overfitting.
However, it still performs worse than ensemble models.

- Random Forest and Boosting Methods Perform Well : Random Forest, AdaBoost, Gradient Boosting, and XGBoost have balanced training and test accuracy, indicating better generalization.
These models also show higher precision, recall, and F1-score, suggesting they are robust classifiers.

- XGBoost Shows the Best Performance: XGBoost has the highest overall test accuracy and F1-score, making it the best-performing model.
This suggests that boosting techniques help improve predictive performance in this dataset.

# Observation:

- Decision Tree Model Overfits:
The Decision Tree model has 100% training accuracy but significantly lower test accuracy, indicating overfitting.
A pruned Decision Tree slightly improves generalization but does not outperform ensemble models.

- Ensemble Models Perform Better : Random Forest, AdaBoost, Gradient Boosting, and XGBoost outperform Decision Trees in test accuracy, precision, recall, and F1-score.
These models effectively handle complex relationships and improve generalization.

- XGBoost is the Best Model: XGBoost consistently provides the highest test accuracy, recall, and F1-score.
It effectively minimizes false negatives, which is crucial for avoiding wrongful visa rejections.
It strikes a good balance between precision and recall, ensuring both correct approvals and denials.

- Importance of Recall in Visa Processing : Recall measures how well the model identifies actual "Certified" visa applications.
A high recall score means fewer qualified candidates are wrongly denied, which is important for ensuring fairness.

#Inference

- Overfitting must be avoided: Decision Trees alone are not reliable due to poor generalization.
- Boosting-based ensemble models (XGBoost, Gradient Boosting) are superior for this classification task.
- XGBoost is the most reliable choice, as it consistently outperforms other models in prediction accuracy.
- Precision-recall trade-offs must be optimized: A higher recall ensures qualified candidates are not wrongly rejected, while a reasonable precision prevents unjustified approvals.

#Conclusions:

- The problem of predicting visa approval (EasyVisa ML Model) benefits from ensemble models, especially XGBoost.
- Decision Trees alone are not sufficient due to overfitting.
- Boosting techniques outperform bagging (Random Forest) in terms of precision and recall.

#Recommendations

- Use XGBoost as the final model for visa approval prediction due to its superior accuracy and F1-score.
- Further fine-tune hyperparameters for Gradient Boosting and XGBoost to enhance performance.
- Consider feature engineering to improve overall prediction quality.
Use cross-validation to further confirm model stability.
"""