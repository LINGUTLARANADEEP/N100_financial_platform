def sector_summary(company, broad_sector, sub_sector,
                   index_weight, market_cap):

    return {
        "Company": company,
        "Broad Sector": broad_sector,
        "Sub Sector": sub_sector,
        "Index Weight %": float(index_weight),
        "Market Cap": market_cap
    }