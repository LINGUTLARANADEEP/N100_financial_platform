def current_price(prices):
    """
    Latest stock price
    """
    return prices[-1]


def highest_price(prices):
    """
    Highest stock price
    """
    return max(prices)


def lowest_price(prices):
    """
    Lowest stock price
    """
    return min(prices)


def annual_return(prices, years):
    """
    Calculate annual return (%)

    years = 1, 3, 5
    """

    months = years * 12

    if len(prices) <= months:
        return 0.0

    start = prices[-months-1]
    end = prices[-1]

    if start == 0:
        return 0.0

    return ((end - start) / start) * 100