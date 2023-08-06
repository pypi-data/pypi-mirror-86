# Bad Formatting

This is gets rid (or at least moves) all those pesky '{', '}' and ';' that we all hate (dont we?)

## Web version
No need to install anything - if you prefer you can just head over [here](https://format.johnmontgomery.tech) in order to shitify your code online!

## Installation

Use the package manager [pip](https://pypi.org/project/badFormatter/) to install bad formatting.

```bash
pip install badFormatter
```
or clone this repo and run in the same way

## Usage (for Pip)

```python
import badFormatter

badFormatter.shitify_print(filename) # prints the code given a filename
badFormatter.shitify_return(filename) # returns the code given a filename
badFormatter.shitify_print_text(text) # prints the code reformatted from the input
badFormatter.shitify_return_text(text) # returns the code reformatted from the input
```

## License
[MIT](https://choosealicense.com/licenses/mit/)