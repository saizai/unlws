# sticky-module

[![build status](https://github.com/WebReflection/sticky-module/actions/workflows/node.js.yml/badge.svg)](https://github.com/WebReflection/sticky-module/actions) [![Coverage Status](https://coveralls.io/repos/github/WebReflection/sticky-module/badge.svg?branch=main)](https://coveralls.io/github/WebReflection/sticky-module?branch=main)

A Symbol based leaky utility to store or retrieve a module, so that libraries can actually be sure if these are re-bundled elsewhere they still work as expected or do not bootstrap twice.

```js
import stickyModule from 'sticky-module';

let [{a, b}, known] = stickyModule('@custom/name', {
  a: Math.random(),
  b: 'let it'
});

known;    // `false`
({a, b}); // the random value and the string "let it"

// on a further attempt it will return exact same object
// hence exact same random value `a` had before
[{a, b}, known] = stickyModule('@custom/name', {
  a: Math.random(),
  b: 'nope, already there'
});

known;    // this time it's `true`
({a, b}); // the same previous random value and the same string "let it"
```
