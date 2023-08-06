from collections import namedtuple
import yaml
from optionstracker.vesting import vested
from optionstracker.value import value


Grant = namedtuple('Grant', 'quantity price date vesting transactions')
Vesting = namedtuple('Vesting', 'interval rate')
Value = namedtuple('Value', 'vested exercised unexercised unvested')
Transaction = namedtuple('Transaction', 'quantity price date')


def grant_from_dict(grant):
    return Grant(
            grant['quantity'], grant['price'], grant['grant-date'],
            vesting_from_dict(grant['vesting']),
            transactions_from_list(grant['transactions'])
            if 'transactions' in grant else [])


def vesting_from_dict(vesting):
    return Vesting(vesting['interval'], vesting['rate'])


def transactions_from_list(transactions):
    return [Transaction(t['quantity'], t['price'], t['date'])
            for t in transactions]


def value_grant(grant, market_price, value_at_date):
    vested_quantity, unvested_quantity = vested(
            grant.quantity, value_at_date, grant.date, grant.vesting.rate,
            grant.vesting.interval)
    vested_value = value(vested_quantity, grant.price, market_price)
    exercised_value = sum(
            [(t.price - grant.price) * t.quantity
             for t in grant.transactions])
    exercised_quantity = sum([t.quantity for t in grant.transactions])
    unexercised_value = value(
            vested_quantity - exercised_quantity, grant.price,
            market_price)
    unvested_value = value(unvested_quantity, grant.price, market_price)
    return Value(
            vested_value, exercised_value, unexercised_value, unvested_value)


def grants_from_file(filepath):
    with open(filepath) as file:
        config = yaml.safe_load(file)
    return [grant_from_dict(o) for o in config['options']]
