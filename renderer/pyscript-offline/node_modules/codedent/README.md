# codedent

[![build status](https://github.com/WebReflection/codedent/actions/workflows/node.js.yml/badge.svg)](https://github.com/WebReflection/codedent/actions) [![Coverage Status](https://coveralls.io/repos/github/WebReflection/codedent/badge.svg?branch=main)](https://coveralls.io/github/WebReflection/codedent?branch=main)


Usable both as template literal tag or just as callback for strings, removes all spaces found at the very first line of code encountered while sanitizing, keeping everything else around.

```js
import dedent from 'codedent';

dedent`
  def this_is_fine():
    return "fine"
`;

/**
def this_is_fine():
  return "fine"
*/
```

Differently from [dedent module](https://github.com/dmnd/dedent), this one doesn't care about code starting in one line then indented in others ... it's just code as you pass it along, no magic involved.
