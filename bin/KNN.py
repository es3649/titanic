#!/usr/bin/python3.6

"""
MakeTree() takes some parameters and makes a decision tree with them

:param train_X: The training independent variables
:param train_y: The training dependent variable
:param neighbor_ct: The maximum number of neighbors the tree can/should consider
    corresponds directly to the eponymous parameter for KNeighborsClassifier

:returns: a trained DecisionTreeRegressor
"""
def MakeClassifier(train_X, train_y, neighbor_ct=10):
    from sklearn.neighbors import KNeighborsClassifier
    knc = KNeighborsClassifier(n_neighbors=neighbor_ct)
    return knc.fit(train_X, train_y)

def adjust(some_list):
    from math import floor
    for i in range(0,len(some_list)):
        some_list[i] = floor(.5 + some_list[i])
    
    return some_list



"""
EvalMae() takes a model and some test parameters and gets statistics on
    it's predictions.

:param tree: is the model to predict with and evaluate
    anything with a predict() method
:param test_X: the independent variables on which to predict
:param test_y: the dependent variable to test check against
"""
def EvalMae(tree, test_X, test_y):
    from sklearn.metrics import mean_absolute_error
    preds = tree.predict(test_X)
    return mean_absolute_error(adjust(preds), test_y)

def toCSV(tree, out_file):
    preds = tree.predict(test_X)
    passenger_id = preds.PassengerId
    test = pd.DataFrame( { "PassengerId" : passenger_id , "Survived" : data } )
    test = test.astype(int)
    test.to_csv(out_file, index=False)



def main():
    import argparse as ap
    parser = ap.ArgumentParser(description="train and evaluate a decision tree given certain params")

    # get data paths
    parser.add_argument('--train', '-t', dest='train', action='store',
                    type=str, nargs=1)
    parser.add_argument('--test', '-s', dest='test', action='store',
                    type=str, nargs=1)

    # out file?
    parser.add_argument('--out', '-o', dest='out', action='store',
                    type=str, nargs=1, argument_default="")

    # get tree parameters
    parser.add_argument('--leaves', '-l', dest='leaves', action='store',
                    type=int, nargs='+')

    # get data info
    parser.add_argument('--dependent', '-d', dest='dep', action='store',
                    type=str, nargs=1)
    parser.add_argument('--independents', '-i', dest='indeps', action='store',
                    type=str, nargs='+')

    args = parser.parse_args()


    import pandas as pd
    # get and separate the training data
    train = pd.read_csv(args.train[0])
    train_X = train[args.indeps]
    train_y = train[args.dep]

    # get and separate the test data
    test = pd.read_csv(args.test[0])
    test_X = test[args.indeps]
    test_y = test[args.dep]

    for l in args.leaves:
        t = MakeClassifier(train_X, train_y, neighbor_ct=l)
        print("Leaves:", l, "Error:", EvalMae(t, test_X, test_y))
        



if __name__ == "__main__":
    main()