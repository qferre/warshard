# WarShard
A simplified modern wargame designed to be compatible with training AIs, thanks to a custom API.

The rules are based on the SPI series of wargames, the rules of which can be found [here](https://www.spigames.net/rules_downloads.htm).


Rules of the simulator are in ![rules](./doc/rules.md)

![alt text](./screenshot.png)

## Installation

to install : in a terminal at the root of the project, run `pip install .`

## API and usage

See api_example.ipynb notebook in the doc directory

General principle is that you should ask you AI agent to produce putative orders, then pass the list of those orders to the simulation
to see the results of those orders