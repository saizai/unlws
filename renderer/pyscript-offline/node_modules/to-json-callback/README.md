# to-json-callback

[![build status](https://github.com/WebReflection/to-json-callback/actions/workflows/node.js.yml/badge.svg)](https://github.com/WebReflection/to-json-callback/actions) [![Coverage Status](https://coveralls.io/repos/github/WebReflection/to-json-callback/badge.svg?branch=main)](https://coveralls.io/github/WebReflection/to-json-callback?branch=main)

Did you know that some function in *JS* can't be serialized as string and be evaluated as such somewhere else?

If you did, you are in the right project, if you didn't though, you still are in the right project.

### what does this solve

```js
const obj = {method() {}};

const str = String(obj.method);
// method() {}

eval(str);
// Uncaught SyntaxError: Unexpected token '{'
```

now ... let's try this again:
```js
import toJSONCallback from 'to-json-callback';

const obj = {method() {}};

const str = toJSONCallback(obj.method);
// function method() {}

eval(str);
// no error whatsoever
```

This is also compatible with all `async` variant of functions, as 100% code-coverage test proves.

**And that's all folks!**
