import os
from typing import Annotated

from jinja2 import Environment, FileSystemLoader
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.auth.utils import verify_password, create_access_token
from app.auth.middleware import get_current_user, CurrentUser

from users.models import User, PredictedDiagnosis
from users.schema import FormDiagnosis, RegisterForm

from ml.learning import LearningML
from ml.models import TableML

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates_env = Environment(loader=FileSystemLoader("templates"))
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    path="/upload_csv_file",
    description="Загрузка csv файла для обучения модели.",
    summary="Загрузка csv файла для обучения модели."
)
async def upload_file(file_csv: UploadFile = File(), db: Session = Depends(get_db)):
    upload_folder = "ml/uploads/csv"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file_csv.filename)
    with open(file_path, "wb") as f:
        f.write(await file_csv.read())

    if not (table_ml := db.query(TableML).filter(TableML.id == 1).first()):
        table_ml = TableML()

    table_ml.name = file_csv.filename
    table_ml.file_path = file_path

    db.add(table_ml)
    db.commit()
    db.refresh(table_ml)

    return {"message": 'Файл успешно загружен.'}


@app.post(
    path="/register",
    description="Регистрация пользователя.",
    summary="Регистрация пользователя.",
)
def register(form_data: Annotated[RegisterForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user:
        return {"error_key": "user_already_registered.", "error_message": "Пользователь уже зарегистрирован."}

    # Создание нового пользователя
    new_user = User(
        username=form_data.username,
        password=form_data.password,
        first_name=form_data.first_name,
        last_name=form_data.last_name,
        date_birth=form_data.date_birth,
        gender=form_data.gender,
        race=form_data.race,
    )

    db.add(new_user)
    db.commit()

    return {"success": True}


@app.post(
    path="/login",
    description="Авторизация пользователя.",
    summary="Авторизация пользователя.",
)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        return {"error_key": "user_not_found", "error_message": "Пользователь не существует, пожалуйста, зарегистрируйтесь."}

    if not verify_password(form_data.password, user.password_hash):
        return {"error_key": "user_not_found", "error_message": "Неверное имя пользователя или пароль."}

    # Создание JWT-токена
    access_token = create_access_token(form_data.username)

    return {"access_token": access_token, "token_type": "bearer"}

    # return Token(access_token=access_token, token_type="bearer")


@app.post(
    path="/create_diagnosis_data",
    description="Получение диагноза на основе переданных данных.",
    summary="Получение диагноза на основе переданных данных.",
)
def create_diagnosis_data(
        form_data: Annotated[FormDiagnosis, Depends()],
        current_user: CurrentUser = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = current_user.user
    predict_diagnosis = form_data.create_diagnosis_object(user.id)
    table_ml = db.query(TableML).filter(TableML.id == 1).first()

    ml = LearningML()
    predict_data = ml.get_predict(table_ml.file_path, predict_diagnosis.get_data_for_ml())

    predict_diagnosis.predict_svm_linear = int(predict_data.predict_svm_linear[0]) if len(predict_data.predict_svm_linear) else None
    predict_diagnosis.predict_svm_poly = int(predict_data.predict_svm_poly[0]) if len(predict_data.predict_svm_poly) else None
    predict_diagnosis.predict_svm_rbf = int(predict_data.predict_svm_rbf[0]) if len(predict_data.predict_svm_rbf) else None
    predict_diagnosis.predict_svm_sigmoid = int(predict_data.predict_svm_sigmoid[0]) if len(predict_data.predict_svm_sigmoid) else None
    predict_diagnosis.predict_random_forest = int(predict_data.predict_random_forest[0]) if len(predict_data.predict_random_forest) else None
    predict_diagnosis.report_dict = predict_data.report_dict if predict_data.report_dict else None
    predict_diagnosis.report_dict = predict_data.report_dict if predict_data.report_dict else None
    predict_diagnosis.grade = predict_data.predict

    db.add(predict_diagnosis)
    db.commit()
    db.refresh(predict_diagnosis)

    user.predict_count = user.predict_count + 1
    user.date_last_diagnosis = predict_diagnosis.date_diagnosis
    user.grade_last_diagnosis = predict_diagnosis.grade
    user.balance = user.balance - predict_diagnosis.price

    db.add(user)
    db.commit()
    db.refresh(predict_diagnosis)

    return {"success": True}


@app.get(
    path="/get_user",
    description="Проверка авторизации и получение пользователя.",
    summary="Проверка авторизации и получение пользователя.",
)
def get_user(current_user: CurrentUser = Depends(get_current_user)):
    user = current_user.user
    return {"username": user.username, "price": user.balance}


@app.get("/get_predict")
def get_predict(request: Request, current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    predict_queryset = db.query(PredictedDiagnosis).filter(PredictedDiagnosis.user_id == current_user.user.id).order_by(desc(PredictedDiagnosis.id)).all()

    predict_data_list = []
    for predict in predict_queryset:
        predict_data = {
            "case_id": predict.case_id,
            "price": predict.price,
            "grade": predict.get_grade(),
            "gender": predict.get_gender(),
            "idh1": predict.get_mutated(predict.idh1),
            "tp53": predict.get_mutated(predict.tp53),
            "atrx": predict.get_mutated(predict.atrx),
            "pten": predict.get_mutated(predict.pten),
            "egrf": predict.get_mutated(predict.egrf),
            "cic": predict.get_mutated(predict.cic),
            "muc16": predict.get_mutated(predict.muc16),
            "pik3ca": predict.get_mutated(predict.pik3ca),
            "nf1": predict.get_mutated(predict.nf1),
            "pic3r1": predict.get_mutated(predict.pic3r1),
            "fubp1": predict.get_mutated(predict.fubp1),
            "rb1": predict.get_mutated(predict.rb1),
            "notch1": predict.get_mutated(predict.notch1),
            "bcor": predict.get_mutated(predict.bcor),
            "csmd3": predict.get_mutated(predict.csmd3),
            "smarca4": predict.get_mutated(predict.smarca4),
            "grin2a": predict.get_mutated(predict.grin2a),
            "idh2": predict.get_mutated(predict.idh2),
            "fat4": predict.get_mutated(predict.fat4),
            "pdgfra": predict.get_mutated(predict.pdgfra),
            "date_birth": predict.date_birth.strftime("%d.%m.%Y"),
            "date_diagnosis": predict.date_diagnosis.strftime("%d.%m.%Y"),
            "report_dict": predict.report_dict
        }

        predict_data_list.append(predict_data)

    template = templates_env.get_template("includes/predict_page.html")
    context = {"request": request, "predicts": predict_data_list, "user": {"username": "test", "price": 1000}}
    rendered_template = template.render(context)

    return {"rendered_template": rendered_template}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/authorization")
async def login(request: Request):
    return templates.TemplateResponse("authorization.html", {"request": request})


@app.get("/registration")
async def register(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.get(
    path="/user",
    description="Загрузка страницы пользователя.",
    summary="Загрузка страницы пользователя.",
)
def get_user(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})


@app.get(
    path="/user/predicts",
    description="Загрузка страницы с предыдущими предсказаниями.",
    summary="Загрузка страницы с предыдущими предсказаниями.",
)
def get_user_predicts(request: Request):
    return templates.TemplateResponse("predicts.html", {"request": request})


@app.get(
    path="/user/predict_form",
    description="Загрузка страницы с формой для предсказания",
    summary="Загрузка страницы с формой для предсказания",
)
def predicts(request: Request, ):
    return templates.TemplateResponse("includes/predict_form.html", {"request": request})


@app.get(
    path="/get_user_data",
    description="Получение данных по пользователю",
    summary="Получение данных по пользователю",
)
def get_user_data(auth_data: CurrentUser = Depends(get_current_user)):
    user = auth_data.user
    error_key = auth_data.error_key
    error_message = auth_data.error_message

    if not user:
        return {"error_key": error_key, "error_message": error_message}

    return {
        "user": {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.get_gender(),
            "race": user.get_race(),
            "date_birth": user.date_birth,
            "grade_last_predict": user.get_grade_last_predict(),
            "date_last_predict": user.get_date_last_diagnosis(),
            "predict_count": user.predict_count,
            "balance": user.balance,
        }
    }
