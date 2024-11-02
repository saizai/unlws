export default function (callback = this) {
  return String(callback).replace(
    /^(async\s*)?(\bfunction\b)?(.*?)\(/,
    (_, isAsync, fn, name) => (
      name && !fn ?
        `${isAsync || ""}function ${name}(` :
        _
    ),
  );
};
