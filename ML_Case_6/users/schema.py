import random
import string

from enum import Enum
from datetime import date
from fastapi import Form
from typing_extensions import Annotated

from .models import PredictedDiagnosis


class GradeEnum(Enum):
    LGG = 'LGG'
    GBM = 'GBM'


class GenderEnum(Enum):
    MALE = 'male'
    FEMALE = 'female'


class RaceEnum(Enum):
    WHITE = 'white'
    BLACK_OR_AFRICAN_AMERICAN = 'black_or_african_American'
    ASIAN = 'asian'
    AMERICAN_INDIAN_OR_ALASKA_NATIVE = 'american_indian_or_alaska_native'


class MutatedEnum(Enum):
    NOT_MUTATED = 'NOT_MUTATED'
    MUTATED = 'MUTATED'


class FormDiagnosis:

    def __init__(
            self,
            *,
            date_birth: Annotated[date, Form(description="Дата рождения")],
            gender: Annotated[GenderEnum, Form(description="Пол")],
            race: Annotated[RaceEnum, Form(description="Тип расы")],
            idh1: Annotated[MutatedEnum, Form(description="Мутация IDH1")],
            tp53: Annotated[MutatedEnum, Form(description="Мутация TP53")],
            atrx: Annotated[MutatedEnum, Form(description="Мутация ATRX")],
            pten: Annotated[MutatedEnum, Form(description="Мутация PTEN")],
            egrf: Annotated[MutatedEnum, Form(description="Мутация EGRF")],
            cic: Annotated[MutatedEnum, Form(description="Мутация CIC")],
            muc16: Annotated[MutatedEnum, Form(description="Мутация MUC16")],
            pik3ca: Annotated[MutatedEnum, Form(description="Мутация PIK3CA")],
            nf1: Annotated[MutatedEnum, Form(description="Мутация NF1")],
            pic3r1: Annotated[MutatedEnum, Form(description="Мутация PIC3R1")],
            fubp1: Annotated[MutatedEnum, Form(description="Мутация FUBP1")],
            rb1: Annotated[MutatedEnum, Form(description="Мутация RB1")],
            notch1: Annotated[MutatedEnum, Form(description="Мутация NOTCH1")],
            bcor: Annotated[MutatedEnum, Form(description="Мутация BCOR")],
            csmd3: Annotated[MutatedEnum, Form(description="Мутация CSM3")],
            smarca4: Annotated[MutatedEnum, Form(description="Мутация SMARCA4")],
            grin2a: Annotated[MutatedEnum, Form(description="Мутация GRIN2A")],
            idh2: Annotated[MutatedEnum, Form(description="Мутация IDH2")],
            fat4: Annotated[MutatedEnum, Form(description="Мутация FAT4")],
            pdgfra: Annotated[MutatedEnum, Form(description="Мутация PGDFRA")],
    ):
        self.date_birth = date_birth
        self.gender = gender
        self.race = race
        self.idh1 = idh1
        self.tp53 = tp53
        self.atrx = atrx
        self.pten = pten
        self.egrf = egrf
        self.cic = cic
        self.muc16 = muc16
        self.pik3ca = pik3ca
        self.nf1 = nf1
        self.pic3r1 = pic3r1
        self.fubp1 = fubp1
        self.rb1 = rb1
        self.notch1 = notch1
        self.bcor = bcor
        self.csmd3 = csmd3
        self.smarca4 = smarca4
        self.grin2a = grin2a
        self.idh2 = idh2
        self.fat4 = fat4
        self.pdgfra = pdgfra

    def create_diagnosis_object(self, current_user_id: int) -> PredictedDiagnosis:
        model = PredictedDiagnosis(
            user_id=current_user_id,
            case_id=self._generate_case_id(),
            price=100,
            date_birth=self.date_birth,
            date_diagnosis=date.today(),
            gender=self._get_int_gender(self.gender.value),
            race=self._get_int_race(self.race.value),
            idh1=self._get_int_value(self.idh1.value),
            tp53=self._get_int_value(self.tp53.value),
            atrx=self._get_int_value(self.atrx.value),
            pten=self._get_int_value(self.pten.value),
            egrf=self._get_int_value(self.egrf.value),
            cic=self._get_int_value(self.cic.value),
            muc16=self._get_int_value(self.muc16.value),
            pik3ca=self._get_int_value(self.pik3ca.value),
            nf1=self._get_int_value(self.nf1.value),
            pic3r1=self._get_int_value(self.pic3r1.value),
            fubp1=self._get_int_value(self.fubp1.value),
            rb1=self._get_int_value(self.rb1.value),
            notch1=self._get_int_value(self.notch1.value),
            bcor=self._get_int_value(self.bcor.value),
            csmd3=self._get_int_value(self.csmd3.value),
            smarca4=self._get_int_value(self.smarca4.value),
            grin2a=self._get_int_value(self.grin2a.value),
            idh2=self._get_int_value(self.idh2.value),
            fat4=self._get_int_value(self.fat4.value),
            pdgfra=self._get_int_value(self.pdgfra.value),
        )

        return model

    @staticmethod
    def _get_int_grade(value: str) -> int:
        return 1 if value == GradeEnum.GBM.value else 0

    @staticmethod
    def _get_int_gender(value: str) -> int:
        return 1 if value == GenderEnum.FEMALE.value else 0

    @staticmethod
    def _get_int_race(value: str) -> int:
        if value == RaceEnum.BLACK_OR_AFRICAN_AMERICAN.value:
            return 1

        if value == RaceEnum.ASIAN.value:
            return 2

        if value == RaceEnum.AMERICAN_INDIAN_OR_ALASKA_NATIVE.value:
            return 3

        return 0

    @staticmethod
    def _get_int_value(value: str) -> int:
        return 1 if value == MutatedEnum.MUTATED.value else 0

    @staticmethod
    def _generate_case_id() -> str:
        key1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
        key2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"TCGA-{key1}-{key2}"


class RegisterForm:

    def __init__(
            self,
            *,
            username: Annotated[str, Form(description="Логин")],
            password: Annotated[str, Form(description="Пароль")],
            first_name: Annotated[str, Form(description="Имя")],
            last_name: Annotated[str, Form(description="Фамилия")],
            date_birth: Annotated[date, Form(description="Дата рождения")],
            gender: Annotated[int, Form(description="Пол")],
            race: Annotated[int, Form(description="Раса")],
    ):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.date_birth = date_birth
        self.gender = gender
        self.race = race
