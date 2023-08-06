# mendi

Simple wrapper that helps you write a menu-driven program easily.

> A menu-driven program is one, which the user is provided a list of choices.
> A particular action is done when the user chooses a valid choice.
> There is also an exit option, to break out of the loop.
> Error message is shown on selecting a wrong choice.

## Installation

```shell
pip install mendi
```

## Usage

This is a simple snippet showing you the use of `mendi`

```python
from mendi import drive_menu

a = int(input('Enter a number: '))

def add():
    print(a+1)

def substract():
    print(a-1)

options = {}

options['1'] = {'desc': 'Add', 'func': add}
options['2'] = {'desc': 'Substract', 'func': substract}

drive_menu('Calculate', options)

```

Here is a sample output:

![output](images/mendi.gif)
