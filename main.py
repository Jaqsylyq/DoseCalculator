from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
import models
from pydantic import BaseModel, Field
from models import Meds
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class MedsRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)


@app.get("/meds", status_code=status.HTTP_200_OK)
async def get_all_meds(db: db_dependency):
    return db.query('Meds').all()


@app.post("/meds", status_code=status.HTTP_201_CREATED)
async def add_med(db: db_dependency, med_request: MedsRequest):
    medication_model = Meds(**med_request.model_dump())

    db.add(medication_model)
    db.commit()


@app.put("/meds/{med_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_med(db: db_dependency, med_request: MedsRequest, med_id: int = Path(gt=0)):
    medication_model = db.query(Meds).filter(Meds.id == med_id).first()
    if medication_model is None:
        raise HTTPException(status_code=404, detail='Medication not found.')
    medication_model.title = med_request.title
    medication_model.description = med_request.description

    db.add(medication_model)
    db.commit()


@app.delete(f"/meds/med_i)", status_code=status.HTTP_204_NO_CONTENT)
async def delete_med(db: db_dependency, med_id: int = Path(gt=0)):
    medication_model = db.query(Meds).filter(Meds.id == med_id).first()
    if medication_model is None:
        raise HTTPException(status_code=404, detail='Medication not found.')
    db.query(Meds).filter(Meds.id == med_id).delete()
    db.commit()


