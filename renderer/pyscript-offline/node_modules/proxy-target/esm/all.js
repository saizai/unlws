import { ARRAY, FUNCTION, NULL, OBJECT } from './types.js';
import { isArray, bound, invoke, reviver, obj } from './utils.js';

export { bound, unbound } from './utils.js';

/**
 * @template V
 * @typedef {import("./utils.js").Arr<V>} Arr
 */

/**
 * @template V
 * @typedef {import("./utils.js").Ctx<V>} Ctx
 */

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
 * @typedef {W extends Ctx<V> ? ReturnType<W> : W extends Arr<V> ? W[0] : W extends Obj<T, V> ? W["v"] : never} ValueOf
 */

/**
 * @template {string} T
 * @template V
 * @param {T} type
 * @param {V} value
 * @returns {T extends typeof FUNCTION ? Ctx<V> : T extends typeof ARRAY ? Arr<V> : Obj<T, V>}
 */
export const target = (type, value) =>
// @see https://github.com/microsoft/TypeScript/issues/33014
// @ts-ignore
(
  type === ARRAY ?
    (/** @type {Arr<V>} */ ([value])) :
    (type === FUNCTION ?
      bound(value) : obj(type, value))
);

/**
 * @template W, T, V
 * @param {W} wrap
 * @param {typeof reviver} [revive]
 * @returns
 */
export const unwrap = (wrap, revive = reviver) => {
  /** @type {string} */
  let type = typeof wrap, value = wrap;
  if (type === FUNCTION)
    value = invoke(wrap);
  else if (type === OBJECT) {
    if (isArray(wrap)) {
      type = ARRAY;
      value = wrap.at(0);
    }
    else
      ({ t: type, v: value } = /** @type {Obj<string, any>} */ (wrap));
  }
  return revive(type, /** @type {ValueOf<W, T, V>} */ (value));
};

/**
 * @template V
 * @param {V} value
 * @param {Function} [resolve]
 * @returns {V extends Function ? Ctx<V> : V extends Array ? Arr<V> : Obj<TypeOf<V>, V>}
 */
export const wrap = (value, resolve = target) => {
  const type = value === null ? NULL : typeof value;
  return resolve(type === OBJECT && isArray(value) ? ARRAY : type, value);
};
