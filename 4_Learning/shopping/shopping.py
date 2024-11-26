import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):

    with open("shopping.csv") as f:

        reader = csv.reader(f)

        data = []

        for row in reader:

            data.append(row)

    """        

    [['Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay', 'Month', 'OperatingSystems', 'Browser', 'Region', 'TrafficType', 'VisitorType', 'Weekend', 'Revenue'], ['0', '0', '0', 
    '0', '1', '0', '0.2', '0.2', '0', '0', 'Feb', '1', '1', '1', '1', 'Returning_Visitor', 'FALSE', 'FALSE'], ['0', '0', '0', '0', '2', '64', '0', '0.1', '0', 
    '0', 'Feb', '2', '2', '1', '2', 'Returning_Visitor', 'FALSE', 'FALSE'], ['0', '0', '0', '0', '1', '0', '0.2', '0.2', '0', '0', 'Feb', '4', '1', '9', '3', 'Returning_Visitor', 'FALSE', 'FALSE'], ['0', '0', '0', '0', '2', '2.666666667', '0.05', '0.14', '0', '0', 'Feb', '3', '2', '2', '4', 'Returning_Visitor', 'FALSE', 'FALSE'], ['0', '0', '0', '0', '10', '627.5', '0.02', '0.05', '0', '0', 'Feb', '3', '3', '1', '4', 'Returning_Visitor', 'TRUE', 'FALSE']]
    """

    del data[0] #Eliminate header

    evidence = []
    labels = []

    for row in data:

        label_raw = row.pop()
        if label_raw == 'TRUE':
            label = int(1)
        elif label_raw == 'FALSE': 
            label = int(0)
        labels.append(label)

        n = len(row)
        evidence_row = []
        for i in range(n):

            
            if i==0 or i==2 or i==4 or i==11 or i==12 or i==13 or i==14:
                value = int(row[i])

            elif i==1 or i==3 or i==5 or i==6 or i==7 or i==8 or i==9:
                value = float(row[i])

            elif i==10:
                if row[i] == 'Jan':
                    value = int(0)
                if row[i] == 'Feb':
                    value = int(1)
                if row[i] == 'Mar':
                    value = int(2)
                if row[i] == 'Apr':
                    value = int(3)     
                if row[i] == 'May':
                    value = int(4)
                if row[i] == 'June':
                    value = int(5)
                if row[i] == 'Jul':
                    value = int(6)
                if row[i] == 'Aug':
                    value = int(7)  
                if row[i] == 'Sep':
                    value = int(8)
                if row[i] == 'Oct':
                    value = int(9)
                if row[i] == 'Nov':
                    value = int(10)
                if row[i] == 'Dec':
                    value = int(11)

            elif i==15:   
                if row[i] == 'Returning_Visitor':
                    value = int(1)
                else:
                    value = int(0)  

            elif i==16:   
                if row[i] == 'TRUE':  
                    value = int(1)   
                else:
                    value = int(0)   

            evidence_row.append(value)  

        evidence.append(evidence_row) 

    return (evidence,labels)    


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    model.fit(evidence,labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity_dict = {}

    for i in range(len(labels)):

        sensitivity_dict[f"{i}"] = [labels[i],predictions[i]]

    identified_counter = 0
    actual_positive_counter = 0
    for key,value in sensitivity_dict.items():

        if value[0] == 1 and  value[1] == 1:
            identified_counter +=1

        if value[0] == 1:
            actual_positive_counter +=1    

    sensitivity = float(identified_counter/actual_positive_counter)    

    specificity_dict = {}

    for i in range(len(labels)):

        specificity_dict[f"{i}"] = [labels[i],predictions[i]]

    identified_counter = 0
    actual_negative_counter = 0
    for key,value in specificity_dict.items():

        if value[0] == 0 and  value[1] == 0:
            identified_counter +=1

        if value[0] == 0:
            actual_negative_counter +=1    

    specificity = float(identified_counter/actual_negative_counter)     

    return (sensitivity,specificity)


if __name__ == "__main__":
    main()
