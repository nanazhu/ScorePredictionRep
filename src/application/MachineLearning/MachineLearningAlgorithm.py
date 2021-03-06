import random
import numpy as np


class MachineLearningAlgorithm(object):

    def __init__(self, train_data, train_label, test_data, test_label, train_descirption, test_description):

        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label
        self.train_description = train_descirption
        self.test_description = test_description

    def train(self, ):
        raise NotImplementedError

    def post_score(self, predicted_labels, probability_events):

        accuracy = 0
        for k, v in enumerate(predicted_labels):
            if v == self.test_label[k]:
                accuracy += 1
        print("Accuracy", accuracy/len(predicted_labels))

        for k, v in enumerate(predicted_labels):
            print(self.test_description[k], "\t", self.test_label[k], "\t", v, "\t", probability_events[k])

        return predicted_labels, probability_events

    def predict(self, data):
        raise NotImplementedError


def split_data(split_percentage=0.75, shuffle=True, *datas):
    """

    :param split_percentage:
    :param shuffle:
    :param datas:
    :return:
    """
    data_size = len(datas[0][0])

    for data in datas[0]:
        if len(data) != data_size:
            raise Exception("Input data with different length")

    split_size = int(split_percentage * data_size)
    if shuffle:
        c = list(zip(*datas[0]))
        random.shuffle(c)
        datas = list(zip(*c))
    else:
        c = list(zip(*datas[0]))
        datas = list(zip(*c))
    train_datas = []
    test_datas = []
    for data in datas:
        train_datas.append(data[:split_size])
        test_datas.append(data[split_size:])
    return train_datas, test_datas


from src.application.MachineLearning.my_sklearn.Sklearn import SklearnAlgorithm
from src.application.MachineLearning.my_poisson.poisson import Poisson


def get_machine_learning_algorithm(framework,
                                   method,
                                   data,
                                   data_label,
                                   data_description=None,
                                   train_percentage=0.75,
                                   **params):
    """

    :param framework:
    :param method:
    :param data:
    :param data_label:
    :param data_description:
    :param train_percentage:
    :param params:
    :return:
    """
    if framework != "my_poisson":
        if data_description:
            train_datas, test_datas = split_data(train_percentage, True, [data, data_label, data_description])
        else:
            train_datas, test_datas = split_data(train_percentage, True, [data, data_label])
        train_data = np.asarray(train_datas[0])
        train_label = np.asarray(train_datas[1])
        test_data = np.asarray(test_datas[0])
        test_label = np.asarray(test_datas[1])
        if data_description:
            train_description = train_datas[2]
            test_description = test_datas[2]
        else:
            train_description = [""]*len(train_data)
            test_description = [""]*len(test_data)
    if framework == "Sklearn":

        return SklearnAlgorithm(method,
                                train_data,
                                train_label,
                                test_data,
                                test_label,
                                train_description,
                                test_description,
                                **params)

    elif framework == "my_poisson":
        return Poisson(**params)

    else:
        # use default
        return SklearnAlgorithm(method,
                                train_data,
                                train_label,
                                test_data,
                                test_label,
                                train_description,
                                test_description,
                                **params)


def get_frameworks():
    return ["Sklearn", "my_poisson"]


def get_methods():
    return ["SVM", "KNN", "RandomForest"]


def get_methods_by_framework(framework):
    if framework == "Sklearn":
        return ["SVM", "KNN", "RandomForest"]

    elif framework == "my_poisson":
        return []

    return []


def get_inputs_by_framework(framework):
    if framework == "Sklearn":
        return [1,2,3,4,6]

    elif framework == "my_poisson":
        return [5]

    return []


def get_inputs_by_input(ml_train_input_id):

    if ml_train_input_id == 1 or ml_train_input_id == 2:
        return [1, 2, 3, 4]

    elif ml_train_input_id == 3 or ml_train_input_id == 4 or ml_train_input_id == 5:
        return []

    return []
