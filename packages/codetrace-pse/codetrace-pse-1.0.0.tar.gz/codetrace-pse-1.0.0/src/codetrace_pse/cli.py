import argparse
import pkg_resources

from .lib.scrape import get_info

# VERSION = pkg_resources.require("codetrace_pse")[0].version
VERSION = '1.0.0'


def build_parser():
    parser = argparse.ArgumentParser(description=f"CoDeTRAce PSE-CLI v{VERSION}")
    parser.add_argument('-s', '--symbol', required=True,
                        help="Symbol of the stock you want to check. (e.g. BPI, JFC)")
    arguments = parser.parse_args()
    return arguments


class BColors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'


def get_stock_details(stock_symbol):
    stock_details = get_info(stock_symbol)
    return stock_details


def main():
    symbol = build_parser().symbol
    d = get_stock_details(symbol.upper())
    if d['status'] != 'OK':
        print(d['status'])
    else:
        print("")
        print("================================================")
        print(f"CoDeTRAce PSE-CLI v{VERSION}")
        print("================================================")
        print(f"Name\t\t: {d['name']}")
        print(f"Symbol\t\t: {d['sym']}")
        print(f"Current Price\t: {d['curr_price']}")

        # add color indicator # FIX001
        '''
        print(f"Current Price\t:", end=" ")        
        if '-' in str(d['curr_price']):
            print(BColors.RED + f"{d['curr_price']}" + BColors.ENDC)
        else:
            print(BColors.GREEN + f"{d['curr_price']}" + BColors.ENDC)
        '''

        print(f"Previous Price\t: {d['prev_price']}")
        print(f"Open\t\t: {d['open']}")
        print(f"Volume\t\t: {d['volume']}")
        print(f"52-Week High\t: {d['high_52_week']}")
        print(f"52-Week Low\t: {d['low_52_week']}")
        print(f"Shares\t    \t: {d['shares']}")
        print("================================================")
        print(f"Source : {d['source_url']}")
        print("================================================")
        print("")


if __name__ == "__main__":
    main()
