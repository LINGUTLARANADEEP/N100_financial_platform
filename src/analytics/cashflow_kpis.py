def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow = Operating Cash Flow + Investing Cash Flow
    """
    return operating_activity + investing_activity


def capex_intensity(investing_activity, operating_activity):

    if operating_activity == 0:
        return None

    return (abs(investing_activity) / operating_activity) * 100


def fcf_conversion(free_cash_flow_value, operating_activity):

    if operating_activity == 0:
        return None

    return (free_cash_flow_value / operating_activity) * 100