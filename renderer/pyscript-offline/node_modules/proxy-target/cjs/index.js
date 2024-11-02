'use strict';
const { ARRAY, FUNCTION, NULL, OBJECT } = require('./types.js');
const { isArray, reviver, obj } = require('./utils.js');

(m => {
  exports.bound = m.bound;
  exports.unbound = m.unbound;
})(require('./utils.js'));

const target = obj;
exports.target = target;

/**
 * @template T, V
 * @typedef {import("./utils.js").Obj<T, V>} Obj
 */

/**
 * @template V
 * @typedef {import("./utils.js").TypeOf<V>} TypeOf
 */

/**
 * @template W, T, V
 * @typedef {W extends Function ? W : W extends Array ? W : W extends Obj<T, V> ? W["v"] : never} ValueOf
 */

/**
 * @template W, T, V
 * @param {W} wrap
 * @param {typeof reviver} [revive]
 * @returns
 */
const unwrap = (wrap, revive = reviver) => {
  /** @type {string} */
  let type = typeof wrap, value = wrap;
  if (type === OBJECT) {
    if (isArray(wrap))
      type = ARRAY;
    else
      ({ t: type, v: value } = /** @type {Obj<string, any>} */ (wrap));
  }
  return revive(type, /** @type {ValueOf<W, T, V>} */ (value));
};
exports.unwrap = unwrap;

const resolver = (type, value) => (
  type === FUNCTION || type === ARRAY ?
    value : target(type, value)
);

/**
 * @template V
 * @param {V} value
 * @returns {V extends Function ? V : V extends Array ? V : Obj<TypeOf<V>, V>}
 */
const wrap = (value, resolve = resolver) => {
  const type = value === null ? NULL : typeof value;
  return resolve(type === OBJECT && isArray(value) ? ARRAY : type, value);
};
exports.wrap = wrap;
