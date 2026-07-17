import pandas as pd

validation_errors = []


def check_nulls(df, table_name):
    null_count = df.isnull().sum().sum()

    if null_count > 0:
        print(f"{table_name}: {null_count} missing values found")
        validation_errors.append(
            {"table": table_name, "error": f"{null_count} missing values"}
        )
    else:
        print(f"{table_name}: No missing values")


def check_duplicates(df, column_name):
    duplicates = df[column_name].duplicated().sum()

    if duplicates > 0:
        print(f"{column_name}: {duplicates} duplicate values found")
        validation_errors.append(
            {"column": column_name, "error": f"{duplicates} duplicate values"}
        )
    else:
        print(f"{column_name}: No duplicates found")


def check_negative_values(df, column_name):
    negative_count = (df[column_name] < 0).sum()

    if negative_count > 0:
        print(f"{column_name}: {negative_count} negative values found")
        validation_errors.append(
            {"column": column_name, "error": f"{negative_count} negative values"}
        )
    else:
        print(f"{column_name}: No negative values found")


if __name__ == "__main__":

    companies = pd.read_excel(
        "data/raw/companies.xlsx",
        header=1
    )

    print(companies.columns)

    check_nulls(companies, "companies")

    check_duplicates(companies, "id")

    check_negative_values(companies, "face_value")
    check_negative_values(companies, "book_value")

    pd.DataFrame(validation_errors).to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print("Validation report saved successfully!")