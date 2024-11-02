'use strict';
const { BIGINT, BOOLEAN, FUNCTION, NULL, NUMBER, OBJECT, STRING, SYMBOL, UNDEFINED } = require('./types.js');

const { isArray } = Array;

exports.isArray = isArray;

const invoke = value => /** @type {Function} */ (value)();
exports.invoke = invoke;

/**
 * @template Value
 * @param {string} type
 * @param {Value} value
 * @returns {Value}
 */
const reviver = (type, value) => value;
exports.reviver = reviver;

/**
 * @template V
 * @typedef {[V]} Arr
 */

/**
 * @template V
 * @typedef {() => V} Ctx
 */

/**
 * @template T, V
 * @typedef {{t:T, v:V}} Obj
 */

/**
 * @template V
 * @typedef {V extends bigint ? BIGINT : V extends boolean ? BOOLEAN : V extends null ? NULL : V extends number ? NUMBER : V extends string ? STRING : V extends symbol ? SYMBOL : V extends undefined ? UNDEFINED : V extends object ? OBJECT : never} TypeOf
 */

/**
 * @template T, V
 * @param {T} t
 * @param {V} v
 * @returns {Obj<T, V>}
 */
const obj = (t, v) => ({t, v});
exports.obj = obj;

/**
 * @template V
 * @param {V} value
 * @returns {Ctx<V>}
 */
const bound = value => Context.bind(value);
exports.bound = bound;

/**
 * @template V, T
 * @param {V} value
 * @returns {V extends Ctx<T> ? ReturnType<V> : V}
 */
const unbound = value => (
  typeof value === FUNCTION ? invoke(value) : value
);
exports.unbound = unbound;

// This is needed to unlock *both* apply and construct
// traps otherwise one of these might fail.
// The 'use strict' directive is needed to allow
// also primitive types to be bound.
function Context() {
  'use strict';
  return this;
}

// TODO: is this really needed in here?
// const { hasOwn } = Object;
// const isConstructable = value => hasOwn(value, 'prototype');
// const isFunction = value => typeof value === FUNCTION;
