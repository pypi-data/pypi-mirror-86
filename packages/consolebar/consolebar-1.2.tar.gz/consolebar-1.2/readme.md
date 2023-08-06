# ConsoleBar

Python Module which creates stunning progress bars for showing progress of loops and iterables in python.

## Installation

Simply using PyPi: 

```
pip install consolebar
```
## Usage

Simply run the following python code:

```python
from consolebar import ConsoleBar

for item in ConsoleBar(object'''(list(), tuple(), dict(), range(), iterable, etc.)''', optional_params):
    #Do your stuff
```

Thats it!

## Parameters

- **loop_to_execute (Required):** Python loop parameter (list(), dictionary(), tuple(), str(), range(), etc.) i.e. iterable object for which progress bar is shown.
- **prefix (Optional):** A string which is shown before the progress bar to describe the progress bar (Default: "Progress:").
- **suffix (Optional):** A string which is shown after the progress bar to describe the progress percentage shown after the progress bar (Default: "Complete").
- **length (Optional):** Length of the progress bar in charecters. Can be adjusted according to one's console charecter width (Default: 50).

Highly useful when you want to run huge loops but don't want to just see the blinking cursor of the console while it is executing.
