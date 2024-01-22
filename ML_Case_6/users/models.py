import math

from typing import Union
from datetime import datetime

from app.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship

from app.auth.utils import get_password_hash


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    first_name = Column(String)
    last_name = Column(String)

    gender = Column(Integer)
    race = Column(Integer)
    date_birth = Column(Date)

    balance = Column(Integer, default=100000)
    predict_count = Column(Integer, default=0)
    date_last_diagnosis = Column(Date)
    grade_last_diagnosis = Column(Integer)

    predicted_diagnosis = relationship("PredictedDiagnosis", back_populates="user")

    def __init__(self, username: str, password: str, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.password_hash = get_password_hash(password)

    def get_grade_last_predict(self) -> str:
        if not self.grade_last_diagnosis:
            return "Не было предсказаний"

        return "GBR" if self.grade_last_diagnosis == 1 else "LGG"

    def get_date_last_diagnosis(self) -> str:
        if not self.date_last_diagnosis:
            return "Не было предсказаний"

        return self.date_last_diagnosis.strftime("%d.%m.%Y")

    def get_predict_count(self) -> str:
        return "GBR" if self.grade_last_diagnosis == 0 else "LGG"

    def get_gender(self) -> str:
        return 'FEMALE' if self.gender == 1 else 'MALE'

    def get_race(self) -> str:
        if self.race == 1:
            return "BLACK OR AFRICAN AMERICAN"

        if self.race == 2:
            return "ASIAN"

        if self.race == 3:
            return "AMERICAN INDIAN OR ALASKA NATIVE"

        return "WHITE"


class PredictedDiagnosis(Base):
    __tablename__ = "predicted_diagnosis"

    id = Column(Integer, primary_key=True, index=True)

    price = Column(Integer, default=0)
    case_id = Column(String)

    idh1 = Column(Integer)
    tp53 = Column(Integer)
    atrx = Column(Integer)
    pten = Column(Integer)
    egrf = Column(Integer)
    cic = Column(Integer)
    muc16 = Column(Integer)
    pik3ca = Column(Integer)
    nf1 = Column(Integer)
    pic3r1 = Column(Integer)
    fubp1 = Column(Integer)
    rb1 = Column(Integer)
    notch1 = Column(Integer)
    bcor = Column(Integer)
    csmd3 = Column(Integer)
    smarca4 = Column(Integer)
    grin2a = Column(Integer)
    idh2 = Column(Integer)
    fat4 = Column(Integer)
    pdgfra = Column(Integer)

    grade = Column(Integer)
    gender = Column(Integer)
    race = Column(Integer)
    date_birth = Column(Date)
    date_diagnosis = Column(Date)

    report_dict = Column(JSON)
    predict_svm_linear = Column(Integer)
    predict_svm_poly = Column(Integer)
    predict_svm_rbf = Column(Integer)
    predict_svm_sigmoid = Column(Integer)
    predict_random_forest = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="predicted_diagnosis")

    def get_data_for_ml(self) -> list[list[Union[float, int]]]:
        return [[
            self.gender,
            self.get_age(),
            self.race,
            self.idh1,
            self.tp53,
            self.atrx,
            self.pten,
            self.egrf,
            self.cic,
            self.muc16,
            self.pik3ca,
            self.nf1,
            self.pic3r1,
            self.fubp1,
            self.rb1,
            self.notch1,
            self.bcor,
            self.csmd3,
            self.smarca4,
            self.grin2a,
            self.idh2,
            self.fat4,
            self.pdgfra,
        ]]

    def get_age(self) -> float:
        date_birth = datetime(self.date_birth.year, self.date_birth.month, self.date_birth.day)
        date_diagnosis = datetime(self.date_diagnosis.year, self.date_diagnosis.month, self.date_diagnosis.day)

        difference = date_diagnosis - date_birth

        years = difference.days // 365  # Отбрасываем остаток от деления
        remaining_days = difference.days % 365  # Остаток дней

        if (date_birth.year + years + 1) % 4 == 0:
            leap_year = True
        else:
            leap_year = False

        if remaining_days >= 59 and leap_year:
            remaining_days -= 1

        if remaining_days > 0:
            percent = math.ceil(remaining_days / 3.65)
            return years + percent / 100

        return float(years)

    @staticmethod
    def get_mutated(value: int) -> str:
        return 'MUTATED' if value == 1 else 'NOT_MUTATED'

    def get_race(self) -> str:
        if self.race == 1:
            return "BLACK OR AFRICAN AMERICAN"

        if self.race == 2:
            return "ASIAN"

        if self.race == 3:
            return "AMERICAN INDIAN OR ALASKA NATIVE"

        return "WHITE"

    def get_gender(self) -> str:
        return 'FEMALE' if self.gender == 1 else 'MALE'

    def get_grade(self) -> str:
        return "GBR" if self.grade == 1 else "LGG"
