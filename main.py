from fastapi import FastAPI, HTTPException, status
from sqlmodel import select, Session

import db_internal

from models import User, PastureRecord, Pasture
from pasture_record_checks import tillage_depth, external_id, crops_in_list

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    db_internal.create_db()


# Users
@app.get("/users", response_model=list[User])
async def get_users():
    with Session(db_internal.engine) as session:
        statement = select(User)
        results = session.execute(statement)
        results = list(i[0] for i in results.all())
    if len(results) == 0:
        return []
    return results


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(User, user_id)
        if not row:
            raise HTTPException(status_code=404, detail="user_id not found")
        session.delete(row)
        session.commit()
        return


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    with Session(db_internal.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


# Pasture CRUD
@app.get("/pasture/{user_id}", response_model=list[Pasture])
async def get_pastures(user_id: int):
    with Session(db_internal.engine) as session:
        statement = select(Pasture).where(Pasture.user_id == user_id)
        results = session.execute(statement)
        results = list(i[0] for i in results.all())
    if len(results) == 0:
        return []
    return results


@app.post("/pasture", status_code=status.HTTP_201_CREATED, response_model=Pasture)
async def create_pasture(paster: Pasture):
    with Session(db_internal.engine) as session:
        session.add(paster)
        session.commit()
        session.refresh(paster)
        return paster


@app.delete("/pasture/{pasture_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pasture(pasture_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(Pasture, pasture_id)
        if not row:
            raise HTTPException(status_code=404, detail="Pasture not found")
        session.delete(row)
        session.commit()
        return


# Pasture Records CRUD
@app.get("/pasture/{pasture_id}/record", response_model=list[PastureRecord])
async def get_pasture_record(pasture_id: int):
    with Session(db_internal.engine) as session:
        statement = select(PastureRecord).where(PastureRecord.pasture_id == pasture_id)
        results = session.execute(statement)
        results = list(i[0] for i in results.all())
        if len(results) == 0:
            return []
        return results


@app.post(
    "/pasture/{pasture_id}/record",
    status_code=status.HTTP_201_CREATED,
    response_model=PastureRecord,
)
async def create_pasture_record(record: PastureRecord):

    if not tillage_depth(record):
        raise HTTPException(
            status_code=400, detail="Tillage Depth out of bounds 0 <= depth < 10 "
        )

    if not external_id(record):
        raise HTTPException(
            status_code=400, detail="External account id does not pass validation check"
        )
    if not crops_in_list(record):
        raise HTTPException(
            status_code=400,
            detail="The crop entered does not appear in the list of known crops",
        )

    with Session(db_internal.engine) as session:
        row = session.get(Pasture, record.pasture_id)
        if not row:
            raise HTTPException(
                status_code=404, detail="Pasture does not exist for this record"
            )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


@app.delete("/pasture/{pasture_id}/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pasture_record(record_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(PastureRecord, record_id)
        if not row:
            raise HTTPException(status_code=404, detail="Record not found")
        session.delete(row)
        session.commit()
        return
