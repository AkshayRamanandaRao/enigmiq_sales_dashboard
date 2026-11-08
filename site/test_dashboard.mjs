import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

class Element {
  constructor() { this.children = []; this.textContent = ''; this.value = ''; }
  append(...items) { this.children.push(...items); }
  replaceChildren(...items) { this.children = items; }
  addEventListener() {}
}

const elements = Object.fromEntries(
  ['#query', '#filter', '#cards', '#resultcount', '#researched', '#drafted', '#contacted', '#conversations', '#stages', '#refresh']
    .map(key => [key, new Element()])
);
elements['#filter'].value = 'all';
const document = { querySelector: key => elements[key], createElement: () => new Element() };
const issue = {
  title: '[research] Example Machines', html_url: 'https://github.com/example/issues/1', updated_at: '2026-11-08T10:00:00Z',
  body: 'Public source: https://example.com/\nPublic contact route: info@example.com\nWhy this company fits: Makes fixtures.\nOffer (EnigmiQ CAD or custom integration): Pilot one fixture.\nNext action: Review draft.\n## Email draft — approval required',
};
const html = readFileSync(new URL('./dist/index.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script);
vm.runInNewContext(script, {
  document,
  fetch: async () => ({ ok: true, json: async () => [issue] }),
  Date,
  console,
});
await new Promise(resolve => setTimeout(resolve, 0));
assert.equal(elements['#researched'].textContent, 1);
assert.equal(elements['#drafted'].textContent, 1);
assert.equal(elements['#stages'].children.length, 7);
assert.equal(elements['#cards'].children.length, 1);
assert.match(elements['#cards'].children[0].children[2].textContent, /Pilot one fixture/);
assert.match(elements['#cards'].children[0].children.at(-1).children[1].textContent, /info@example.com/);

