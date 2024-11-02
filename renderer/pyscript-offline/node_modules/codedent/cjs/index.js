'use strict';
const content = (m => /* c8 ignore start */ m.__esModule ? m.default : m /* c8 ignore stop */)(require('plain-tag'));

const dedent = {
  object(...args) {
    return this.string(content(...args));
  },
  string(content) {
    for (const line of content.split(/[\r\n]+/)) {
      // skip initial empty lines
      if (line.trim().length) {
        // trap indentation at the very first line of code
        if (/^(\s+)/.test(line))
          content = content.replace(new RegExp('^' + RegExp.$1, 'gm'), '');
        // no indentation? all good: get out of here!
        break;
      }
    }
    return content;
  }
};

/**
 * Usable both as template literal tag or just as callback for strings, removes all spaces found
 * at the very first line of code encountered while sanitizing, keeping everything else around.
 * @param {string | TemplateStringsArray} tpl either code as string or as template, when used as tag
 * @param  {...any} values the template interpolations, when used as tag
 * @returns {string} code without undesired indentation
 */
const codedent = (tpl, ...values) => dedent[typeof tpl](tpl, ...values);

module.exports = codedent;
