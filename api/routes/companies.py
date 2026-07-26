from fastapi import APIRouter, HTTPException

from api.database import get_connection


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.get("/")
def get_companies():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            company_name,
            website
        FROM companies
        LIMIT 20
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "company_name": row[1],
            "website": row[2]
        }
        for row in rows
    ]


@router.get("/{company_id}")
def get_company(company_id:str):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        (company_id,)
    )


    row = cursor.fetchone()


    conn.close()


    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )


    return {
        "id": row[0],
        "company_name": row[1],
        "website": row[2]
    }