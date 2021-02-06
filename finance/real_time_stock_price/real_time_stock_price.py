from yahoo_fin import stock_info
import sys
import time

"""
Author:         Nick Loden

Last Update:    02/06/2021

Description:    This script will take in a stock ticker and an optional refresh frequency in seconds, and output
                near real time statistics about the stock specified. This script utilizes the yahoo finance api
                to obtain the prices for the tickers provided.
                
Input:          sys.argv[1] = ticker symbol
                sys.argv[2] = optional refresh frequency
                
Standard Form:  python real_time_stock.price.py <string: ticker> <int: frequency>

Installation/Configuration Guidance:

    Option 1:
        pip install -r requirements.txt
        
    Option 2:
        pip install pandas
        pip install requests
        pip install requests_html
        pip install yahoo_fin
"""


def validate_input():
    """
    validate_input ensures that the run time arguments provided by the user meet the execution requirements for
    this script. It ensures that there is at least one argument provided for the ticker, but no more than two provided
    to account for the ticker and refresh frequency.
    :return: A list containing at least one element representing a validated ticker string. Said list may contain a
    second element which will represent the refresh frequency.
    """

    # initialize variables
    validated_args = []

    if len(sys.argv) < 2 or len(sys.argv) > 3:  # note: sys.arv[0] is counted, so need to up by 1
        print("Error: You must provide at least one runtime argument.")
        print("Standard Form: python {} <stock ticker> <optional: refresh frequency>".format(sys.argv[0]))
        sys.exit()

    # validate input for second argument for update frequency if exists
    if len(sys.argv) == 3:
        # ensure argument is all numeric characters
        if not sys.argv[2].isnumeric():
            print("Error: The refresh frequency provided must be an integer/whole number.")
            sys.exit()
        elif int(sys.argv[2]) < 1 or int(sys.argv[2]) > 60:
            print("Error: The refresh frequency provided must be in the range 1 - 60.")
            sys.exit()

        # argument 2 passed validation. add to return list
        validated_args.append(sys.argv[2])

    # validate input for first argument for stock ticker
    # ensure argument is of type string
    if not sys.argv[1].isalpha():
        print("Error: The ticker provided must be a string of letters (a - z).")
        sys.exit()
    # ensure length of string is greater than 0 and less than 5
    elif len(sys.argv[1]) < 1 or len(sys.argv[1]) > 5:
        print("Error: The ticker provided must contain 1 - 5 alpha characters.")
        sys.exit()

    # test single yahoo finance api call to see if ticker provided is legit
    try:
        test_ticker = "{:.2f}".format(stock_info.get_live_price(sys.argv[1]))
    except Exception:
        print("Error: Invalid ticker provided.")
        sys.exit()

    # argument 1 passed validation. add to first position of return list
    validated_args.insert(0, sys.argv[1])

    # return list of vetted argument(s)
    return validated_args


def symbol_checker():
    up_arrow = ''
    down_arrow = ''

    try:
        up_arrow = u'\u2191'  # up arrow symbol
        down_arrow = u'\u2193'  # down arrow symbol

        output_string = "\r{} {}".format(up_arrow, down_arrow)
        print(output_string)
    except Exception:
        up_arrow = '^'  # up arrow symbol
        down_arrow = 'v'  # down arrow symbol
    finally:
        sys.stdout.flush()

    return up_arrow, down_arrow


def get_stock_price(ticker):
    """
    get_stock_price will utilize the yahoo_fin library and call the get_live_price method with the ticker passed into
    this function.
    :param ticker: this is the first run time parameter provided by the user that designates the stock to be queried.
    :return: the current price of the stock specified in string form. This string will be represented as a fractional
    value with 2 decimal point precision.
    """

    return "{:.2f}".format(stock_info.get_live_price(ticker))


def dynamic_stock_price_output(ticker, frequency=2):
    """
    dynamic_stock_price_output will consume both the ticker and frequency variables as input, and then output
    dynamic text to standard out and continue to update the time and stock price values until the program is terminated
    with a control+c input.
    :param ticker: this is the first run time parameter provided by the user that designates the stock to be queried.
    :param frequency: this is the second optional run time parameter provided by the user that designates the refresh
    frequency of the stock price and time. If a value of 5 is provided, then the yahoo finance api will be called
    every 5 seconds, and the result will be output to standard out.
    :return: None. Nothing is directly returned from this function, but there will be content output to standard out.
    """

    # declare function variables
    old_price = 0.0
    new_price = 0.0
    up_arrow, down_arrow = symbol_checker()

    # print out static information:
    print(' ------------------------')
    print('| Real Time Stock Prices |')
    print(' ------------------------')
    print('(press control+c to quit.)')
    print('Ticker:  {}'.format(ticker.upper()))
    print('Date:    {}'.format(time.strftime('%m/%d/%Y')))
    print('Refresh: {}'.format(frequency) + ' second(s)')

    # loop until keyboard interrupt is detected (control+c)
    while True:
        try:
            # call get_stock_price function to obtain current stock price
            new_price = float(get_stock_price(ticker))

            # compare current price against previous price
            if new_price > old_price:
                arrow = up_arrow  # up arrow symbol
            elif new_price < old_price:
                arrow = down_arrow  # down arrow symbol
            else:
                arrow = ''  # blank arrow indicating no price change

            # output dynamic text with current date/time stamp and price with arrow
            print('\r', end='')
            print("Time: {} | Price: {:.2f} {}".format(time.strftime('%H:%M:%S'), new_price, arrow), end='', flush=True)

            # original way to display dynamic text output - python 2.x preferred way
            # output_string = "\rTime: {} | Price: {:.2f} {}".format(time.strftime('%H:%M:%S'), new_price, arrow)
            # sys.stdout.write(output_string)
            # sys.stdout.flush()

            # set old price to new price to compare for next loop cycle
            old_price = new_price
            time.sleep(int(frequency))  # sleep for 2 seconds
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    # validate run time arguments, and pass them back in list
    input_list = validate_input()

    # check length of argument list, and call primary stock price function with appropriate amount of arguments.
    if len(input_list) == 1:  # only one argument provided
        dynamic_stock_price_output(input_list[0])
    elif len(input_list) == 2:  # two arguments provided
        dynamic_stock_price_output(input_list[0], input_list[1])
