def get_sign(value):
    """
    Returns +, -, or 0
    """
    if value > 0:
        return "+"
    elif value < 0:
        return "-"
    else:
        return "0"


def classify_pattern(cfo, cfi, cff):
    """
    Capital Allocation Pattern Classifier
    """

    cfo_sign = get_sign(cfo)
    cfi_sign = get_sign(cfi)
    cff_sign = get_sign(cff)

    pattern = "Unknown"

    if cfo_sign == "+" and cfi_sign == "-" and cff_sign == "-":
        pattern = "Reinvestor"

    elif cfo_sign == "+" and cfi_sign == "+" and cff_sign == "-":
        pattern = "Liquidating Assets"

    elif cfo_sign == "-" and cfi_sign == "+" and cff_sign == "+":
        pattern = "Distress Signal"

    elif cfo_sign == "-" and cfi_sign == "-" and cff_sign == "+":
        pattern = "Growth Funded by Debt"

    elif cfo_sign == "+" and cfi_sign == "+" and cff_sign == "+":
        pattern = "Cash Accumulator"

    elif cfo_sign == "-" and cfi_sign == "-" and cff_sign == "-":
        pattern = "Pre-Revenue"

    elif cfo_sign == "+" and cfi_sign == "-" and cff_sign == "+":
        pattern = "Mixed"

    return {
        "cfo_sign": cfo_sign,
        "cfi_sign": cfi_sign,
        "cff_sign": cff_sign,
        "pattern": pattern
    }