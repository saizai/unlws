'use strict';
// this file exists to simply be able to switch to it
// whenever doubts or checks around performance are meant
// or whenever debugging is needed to see if its this module
// fault if something goes "bananas"

const typedSet = () => Set;
exports.typedSet = typedSet;
const typedWeakSet = () => WeakSet;
exports.typedWeakSet = typedWeakSet;

const typedMap = () => Map;
exports.typedMap = typedMap;
const typedWeakMap = () => WeakMap;
exports.typedWeakMap = typedWeakMap;
