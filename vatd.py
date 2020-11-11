"""Simple tool for removing the amount of UK VAT applied to a total receipt.
   Over-engineered to explore Python's ArgParse library."""

import argparse
import sys


def get_options(args):
    """Returns an argparse dictionary object with application version
    number, total value, value_added-tax rate and verbosity attributes."""
    parser = argparse.ArgumentParser(
        prog='VATDeductor',
        description='Displays the VAT deductable from a total receipt value')
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.1')
    parser.add_argument(
        '--rate',
        type=float,
        action='store',
        nargs='?',
        default='1.2',
        help='enter VAT rate as a decimal. Default is 1.2')
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='displays Total Amount, VAT deductable & pretax values')
    parser.add_argument(
        'total',
        metavar='T',
        type=float,
        action='store',
        help='amount of TOTAL receipt value for processing')
    return vars(parser.parse_args())


def calculate_net(options):
    """Calculates the receipt value without the addition of VAT applied."""
    total_value = options['total']
    vat_rate = options['rate']
    net_value = round(total_value / vat_rate, 2)
    return net_value


def calculate_refund(options):
    """Calculates total receipt minus the net, rounded to 2 decimal places.
    The returned value is the VAT deductable."""
    refund_value = round(options['total'] - calculate_net(options), 2)
    return refund_value


def verbosity(options):
    """Presents calculation values in a cleaner but more verbose manner."""
    template = f"""
************************
Total Receipt:  £{options['total']}
Net Value:      £{calculate_net(options)}
Deductable VAT: £{calculate_refund(options)}
************************"""
    return template


def main(args):
    options = get_options(args)
    if options['verbose']:
        print(verbosity(options))
    else:
        print(calculate_refund(options))


if __name__ == "__main__":
    main(sys.argv[1:])
