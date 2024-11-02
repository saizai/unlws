function index (callback = this) {
  return String(callback).replace(
    /^(async\s*)?(\bfunction\b)?(.*?)\(/,
    (_, isAsync, fn, name) => (
      name && !fn ?
        `${isAsync || ""}function ${name}(` :
        _
    ),
  );
}

export { index as default };
