# Reverse bar detector
## Introduction
From box work only with MT5 with AlfaForex. \
This program need for detect current or previous reverse bar in all pairs with next conditions:
- Previous period bear reverse bar (red) at least third above Bill Williams Alligator indicator (Alligator next) is the highest extremum, and close lower than open.
- Current period bear reverse bar (pink) at least third above Alligator, and high price is the highest extremum, and close lower than open.
- Previous period bull reverse bar (green) at least third below Alligator, and low price is the lowest extremum, and close higher than open.
- Current period bull reverse bar (light green) at least third below Alligator, and low price is the lowest extremum, and close higher than open.
- For all types updates work only if bar time progress > 50%
- In all rows you have a field for notes

## Old version screenshot
![Example running on AlfaForex](https://github.com/makhnanov/meta-trader-5-python-reverse-bars/blob/master/reverse.jpg?raw=true)

## ToDo:
- Auto-save notes
- Increase update speed
- Update screenshot
- Make adaptive interface
- Add settings for save pairs for work with not only AlfaForex
- Use QThread for unblocked updates
- Add requirements file
