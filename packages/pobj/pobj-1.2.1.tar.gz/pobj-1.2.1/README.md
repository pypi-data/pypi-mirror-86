# Print Object in Python3.x

- Print your variable/object in beautiful way
- It's easier way to print variable name & it's value
- pobj print any type of value. Like int, str, bool, list, dict, django request, dataframe, ... few more

---
## Install with pip
```
pip install pobj
```

---
## Upgrade with pip
```
pip install pobj --upgrade
```

---
## How to implement
1) install package by `pip install pobj`
2) import pobj by `from pobj import pobj` in class.py
3) use pobj in your code as bellow standards...
```
pobj(your_variable)
```

---
## Demo / Example

### Source Code/File:
```
class Fruits:

    def get_apple_detail(self, price: float = 0.0):
        result = {
            'fruit': 'Apple',
            'price': price or 120,
            'quantity': 2,
            'available': True
        }
        pobj(result)
        return result

```

### OutPut:
```
---result---type:dict---size:240-bytes---
{
  "available": true,
  "fruit": "Apple",
  "price": 120,
  "quantity": 2
}

```