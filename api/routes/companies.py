from fastapi import APIRouter

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