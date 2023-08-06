# Options Tracker [![pipeline status](https://gitlab.com/OldIronHorse/options-tracker/badges/master/pipeline.svg)](https://gitlab.com/OldIronHorse/options-tracker/-/commits/master) [![coverage report](https://gitlab.com/OldIronHorse/options-tracker/badges/master/coverage.svg)](https://gitlab.com/OldIronHorse/options-tracker/-/commits/master)


How much are my stock options worth today?

Vested and unvested.

## Installation

You need python 3.6+

`pip install options-tracker`

## Usage: options-tracker

Basic (this should work for your Mirriad options):

`options-tracker <granted quantity> <grant price>`

Have a look at the help for more options:

`options-tracker --help`

## Usage: options-file-tracker

Read option grant details from a YAML file (default: .options-tracker.yaml)

`options-file-tracker`

File format:

```
options:
  - quantity: N
    price: N
    grant-date: YYYY-MM-DD
    vesting:
      interval: y|m
      rate: D
    transactions:
      - quantity: N
        price: N
        date: YYYY-MM-DD
```
