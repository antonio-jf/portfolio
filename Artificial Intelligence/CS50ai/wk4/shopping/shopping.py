# Trains K Nearest Neighbors models to classify wether a user will make a purchase on a website
# Model is tested for K = 1:N and returns the best possible K for the model according to specificity and sensitivity  

import csv
import sys
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Amount of data to use for training
TEST_SIZE = 0.6
# Number of neighbors over which to train the model
# The model will train over 1:N to determine best number of neighbors
N = 15

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Initialize variables for testing
    sensitivity = 0
    specificity = 0
    K = 0
    # Train model for K neighbors from 1 to 15 and make predictions
    for k in range(1, N):
        model = train_model(X_train, y_train, k)
        predictions = model.predict(X_test)
        
        sens, spec = evaluate(y_test, predictions)
        # Compare current sensitivity and specificity, if better keep them
        if (sens + spec) > (sensitivity + specificity):
            sensitivity = sens
            specificity = spec
            # Keep track of the amount of neighbors
            K = k

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"Best K number of neighbors: {K}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).
    """
    # Load file as dataframe for ease of data wrangling
    df = pd.read_csv("shopping.csv")
    # Convert months to integers
    df['Month'].replace({"Jan": 0, 'Feb': 1, 'Mar': 2,
                         'Apr': 3, 'May': 4, 'June': 5, 
                         'Jul': 6, 'Aug': 7, 'Sep': 8,
                         'Oct': 9, 'Nov': 10, 'Dec': 11}, inplace=True)

    # Convert VisitorType, Weekend and Revenue columns to binary
    df.loc[df['VisitorType'] == "Returning_Visitor", 'VisitorType'] = 1
    df.loc[df['VisitorType'] != 1, 'VisitorType'] = 0
    df['Weekend'].replace({True: 1, False: 0}, inplace=True)
    df['Revenue'].replace({True: 1, False: 0}, inplace=True)

    # Subset dataframe and select labels and evidence
    dimensions = df.shape
    evidence_df = df.iloc[0:dimensions[0], 0:(dimensions[1] - 1)]
    labels_df = df.iloc[0:dimensions[0], (dimensions[1] - 1)]
    
    # Convert to lists
    evidence = evidence_df.values.tolist()
    labels = labels_df.values.tolist()

    return (evidence, labels)        

def train_model(evidence, labels, k):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model trained on the data.
    """
    # K neaigbors for model
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(evidence, labels)
    
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).
    """
    true_positives = 0
    true_negatives = 0
    sensitivity = 0
    specificity = 0
    
    for label, prediction in zip(labels, predictions):
        true_positives = (true_positives) + 1 if label == 1 else true_positives
        true_negatives = (true_negatives) + 1 if label == 0 else true_negatives
        
        if label == prediction:
            if label == 1:
                sensitivity += 1
            else:
                specificity += 1

    return (sensitivity/float(true_positives), specificity/float(true_negatives))


if __name__ == "__main__":
    main()
