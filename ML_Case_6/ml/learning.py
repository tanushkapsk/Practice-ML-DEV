import pandas as pd
import numpy as np

from typing import Union, Optional, NamedTuple
from pandas import DataFrame
from pandas import Series
from pandas.io.parsers import TextFileReader
from numpy import ndarray

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier

from users.utils import get_age, get_race
from .config import MUTAGEN_CATEGORY, EXCLUDE_VALUE
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class PredictionML(NamedTuple):
    linear: LinearRegression
    svm: SVC
    random_forest: RandomForestRegressor
    y_test: Optional[str]
    report: Optional[str]


class PredictionData(NamedTuple):
    # Predict
    predict_svm_linear: list = []
    predict_svm_poly: list = []
    predict_svm_rbf: list = []
    predict_svm_sigmoid: list = []
    predict_random_forest: list = []
    predict: list = []

    # Classification report
    report_dict: dict = {}


class LearningML:
    """
    Обучение модели и предсказание диагноза на основе обученной модели.
    """

    def __init__(self):
        self.encoder = OneHotEncoder(sparse=False)
        self.data_csv: Optional[Union[DataFrame, TextFileReader]] = None

        self.svm_linear: SVC = SVC(kernel='linear')
        self.svm_poly: SVC = SVC(kernel='poly')
        self.svm_rbf: SVC = SVC(kernel='rbf')
        self.svm_sigmoid: SVC = SVC(kernel='sigmoid')
        self.random_forest: RandomForestRegressor = RandomForestRegressor(max_depth=2, random_state=42)
        self.report_dict: dict = {}

    def learn(self, url_file: str):
        self.data_csv = pd.read_csv(url_file)
        self._update_mutagen_category_column()
        self.data_csv.dropna(subset=['Gender', 'Age_at_diagnosis', 'Primary_Diagnosis', 'Race', ])
        self._update_value_in_columns()

        X = self.data_csv.drop(columns=['Gender', 'Project', 'Case_ID', 'Primary_Diagnosis'])
        y = self.data_csv['Grade']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.svm_linear.fit(X_train, y_train)
        self.svm_poly.fit(X_train, y_train)
        self.svm_rbf.fit(X_train, y_train)
        self.svm_sigmoid.fit(X_train, y_train)
        self.random_forest.fit(X_train, y_train)

        y_pred_svm_linear = self.svm_linear.predict(X_test)
        y_pred_svm_poly = self.svm_poly.predict(X_test)
        y_pred_svm_rbf = self.svm_rbf.predict(X_test)
        y_pred_svm_sigmoid = self.svm_sigmoid.predict(X_test)
        y_pred_random_forest = self.random_forest.predict(X_test)

        self._get_report_dict("svm_linear", y_test, y_pred_svm_linear)
        self._get_report_dict("svm_poly", y_test, y_pred_svm_poly)
        self._get_report_dict("svm_rbf", y_test, y_pred_svm_rbf)
        self._get_report_dict("svm_sigmoid", y_test, y_pred_svm_sigmoid)
        self._get_report_dict("random_forest", y_test, y_pred_random_forest)

    def _get_report_dict(self, name: str, y_test: Series, y_pred: ndarray):
        if name not in self.report_dict:
            self.report_dict[name] = {
                "accuracy": round(float(accuracy_score(y_test, y_pred)), 2),
                "precision": round(float(precision_score(y_test, y_pred)), 2),
                "recall": round(float(recall_score(y_test, y_pred)), 2),
                "f1": round(float(f1_score(y_test, y_pred)), 2),
            }

    def get_predict(self, url_file: str, data: list[list[Union[float, int]]]) -> PredictionData:
        self.learn(url_file)

        predict_svm_linear = self.svm_linear.predict(data)
        predict_svm_poly = self.svm_poly.predict(data)
        predict_svm_rbf = self.svm_rbf.predict(data)
        predict_svm_sigmoid = self.svm_sigmoid.predict(data)
        predict_random_forest = self.random_forest.predict(data)
        final_prediction = (predict_svm_linear + predict_svm_poly + predict_svm_rbf + predict_svm_sigmoid + predict_random_forest) / 5
        predict = round(final_prediction[0])

        return PredictionData(
            predict_svm_linear=predict_svm_linear,
            predict_svm_poly=predict_svm_poly,
            predict_svm_rbf=predict_svm_rbf,
            predict_svm_sigmoid=predict_svm_sigmoid,
            predict_random_forest=predict_random_forest,
            predict=predict,
            report_dict=self.report_dict
        )

        # # predicted_linear = ml_data.linear.predict(data)
        # # predicted_random_forest = ml_data.random_forest.predict(data)
        # # predicted_svm = ml_data.svm.predict(data)
        # # final_prediction = (predicted_linear + predicted_random_forest + predicted_svm) / 3
        # # print('final_prediction', final_prediction)
        # #
        # # print('predicted_linear', predicted_linear)
        # # print('predicted_random_forest', predicted_random_forest)
        # # print('predicted_svm', predicted_svm)
        # # print()
        #
        # return predicted_svm, ml_data.report

    def _update_mutagen_category_column(self):
        for column in self.data_csv.columns:
            if column in MUTAGEN_CATEGORY:
                self.data_csv[column] = self.data_csv[column].apply(lambda value: self._check_value(value, 'MUTATED'))
            else:
                self.data_csv[column] = self.data_csv[column].apply(lambda value: self._check_exclude_value(value))

    @staticmethod
    def _check_exclude_value(value: str) -> Optional[str]:
        return '' if value in EXCLUDE_VALUE else value

    @staticmethod
    def _check_value(value: str, value_comparison: str) -> int:
        return 1 if value == value_comparison else 0

    def _update_value_in_columns(self):
        self.data_csv['Grade'] = self.data_csv['Grade'].apply(lambda value: self._check_value(value, 'GBM'))
        self.data_csv['Gender'] = self.data_csv['Gender'].apply(lambda value: self._check_value(value, 'Female'))
        self.data_csv['Age_at_diagnosis'] = self.data_csv['Age_at_diagnosis'].apply(lambda value: get_age(value))
        self.data_csv['Race'] = self.data_csv['Race'].apply(lambda value: get_race(value))
