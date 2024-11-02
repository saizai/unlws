export function invoke(value: any): any;
export function reviver<Value>(type: string, value: Value): Value;
export function obj<T, V>(t: T, v: V): Obj<T, V>;
export function bound<V>(value: V): Ctx<V>;
export function unbound<V, T>(value: V): V extends Ctx<T> ? ReturnType<V> : V;
export type Arr<V> = [V];
export type Ctx<V> = () => V;
export type Obj<T, V> = {
    t: T;
    v: V;
};
export type TypeOf<V> = V extends bigint ? "bigint" : V extends boolean ? "boolean" : V extends null ? "null" : V extends number ? "number" : V extends string ? "string" : V extends symbol ? "symbol" : V extends undefined ? "undefined" : V extends object ? "object" : never;
export const isArray: (arg: any) => arg is any[];
