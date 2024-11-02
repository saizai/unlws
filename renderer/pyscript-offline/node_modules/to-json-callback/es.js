function n(n=this){return String(n).replace(/^(async\s*)?(\bfunction\b)?(.*?)\(/,((n,t,c,e)=>e&&!c?`${t||""}function ${e}(`:n))}export{n as default};
