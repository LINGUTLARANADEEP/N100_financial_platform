import os
import pandas as pd

from tearsheet import generate_tearsheet


# -------------------------
# PATHS
# -------------------------

COMPANY_FILE = "output/financial_ratios.csv"

OUTPUT_DIR = "reports/tearsheets"

SKIPPED_FILE = "output/skipped_tearsheets.csv"


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


def get_companies():

    df = pd.read_csv(
        COMPANY_FILE
    )

    companies = (
        df["company_id"]
        .drop_duplicates()
        .tolist()
    )

    return companies



def validate_company(company_id):

    df = pd.read_csv(
        COMPANY_FILE
    )


    company_data = df[
        df["company_id"] == company_id
    ]


    years = company_data["year"].nunique()


    # skip companies having less than 3 years data

    if years < 3:
        return False


    return True




def run_batch():


    companies = get_companies()


    skipped = []

    generated = 0


    print(
        f"Total companies found: {len(companies)}"
    )



    for company in companies:


        try:


            print(
                f"Generating report: {company}"
            )


            if not validate_company(company):

                skipped.append(
                    {
                        "company_id": company,
                        "reason": "Less than 3 years data"
                    }
                )

                continue



            generate_tearsheet(
                company
            )


            generated += 1



        except Exception as e:


            skipped.append(
                {
                    "company_id": company,
                    "reason": str(e)
                }
            )


            print(
                "Failed:",
                company,
                e
            )



    if skipped:


        pd.DataFrame(
            skipped
        ).to_csv(
            SKIPPED_FILE,
            index=False
        )



    print("===================")

    print(
        "Generated:",
        generated
    )

    print(
        "Skipped:",
        len(skipped)
    )

    print("===================")



if __name__ == "__main__":

    run_batch()