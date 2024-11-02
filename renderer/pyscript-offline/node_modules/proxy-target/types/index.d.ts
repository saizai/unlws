export const target: <T, V>(t: T, v: V) => import("./utils.js").Obj<T, V>;
export function unwrap<W, T, V>(wrap: W, revive?: (<Value>(type: string, value: Value) => Value) | undefined): ValueOf<W, T, V>;
export function wrap<V>(value: V, resolve?: (type: any, value: any) => any): V extends Function ? V : V extends any[] ? V : Obj<import("./utils.js").TypeOf<V>, V>;
export type Obj<T, V> = import("./utils.js").Obj<T, V>;
export type TypeOf<V> = import("./utils.js").TypeOf<V>;
export type ValueOf<W, T, V> = W extends Function ? W : W extends any[] ? W : W extends Obj<T, V> ? W["v"] : never;
export { bound, unbound } from "./utils.js";
