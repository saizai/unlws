import{codePointSize as t,codePointAt as e,EditorSelection as o,CharCategory as n,Prec as i,Facet as s,combineConfig as l,StateField as r,StateEffect as a,MapMode as c,RangeValue as h,RangeSet as p,fromCodePoint as f,Annotation as u,Text as d,Transaction as m}from"./codemirror_state-1d1uncXx.js";import{E as g,k as v,D as b,s as w,g as y,V as x,l as C,a as I,W as O}from"./codemirror_view-aIuSN42d.js";import{s as k,i as D}from"./codemirror_language-CJQIaKtn.js";class T{constructor(t,e,o,n){this.state=t,this.pos=e,this.explicit=o,this.view=n,this.abortListeners=[],this.abortOnDocChange=!1}tokenBefore(t){let e=k(this.state).resolveInner(this.pos,-1);for(;e&&t.indexOf(e.name)<0;)e=e.parent;return e?{from:e.from,to:this.pos,text:this.state.sliceDoc(e.from,this.pos),type:e.type}:null}matchBefore(t){let e=this.state.doc.lineAt(this.pos),o=Math.max(e.from,this.pos-250),n=e.text.slice(o-e.from,this.pos-e.from),i=n.search(P(t,!1));return i<0?null:{from:o+i,to:this.pos,text:n.slice(i)}}get aborted(){return null==this.abortListeners}addEventListener(t,e,o){"abort"==t&&this.abortListeners&&(this.abortListeners.push(e),o&&o.onDocChange&&(this.abortOnDocChange=!0))}}function S(t){let e=Object.keys(t).join(""),o=/\w/.test(e);return o&&(e=e.replace(/\w/g,"")),`[${o?"\\w":""}${e.replace(/[^\w\s]/g,"\\$&")}]`}function A(t){let e=t.map((t=>"string"==typeof t?{label:t}:t)),[o,n]=e.every((t=>/^\w+$/.test(t.label)))?[/\w*$/,/\w+$/]:function(t){let e=Object.create(null),o=Object.create(null);for(let{label:n}of t){e[n[0]]=!0;for(let t=1;t<n.length;t++)o[n[t]]=!0}let n=S(e)+S(o)+"*$";return[new RegExp("^"+n),new RegExp(n)]}(e);return t=>{let i=t.matchBefore(n);return i||t.explicit?{from:i?i.from:t.pos,options:e,validFor:o}:null}}function L(t,e){return o=>{for(let e=k(o.state).resolveInner(o.pos,-1);e;e=e.parent){if(t.indexOf(e.name)>-1)return null;if(e.type.isTop)break}return e(o)}}class R{constructor(t,e,o,n){this.completion=t,this.source=e,this.match=o,this.score=n}}function E(t){return t.selection.main.from}function P(t,e){var o;let{source:n}=t,i=e&&"^"!=n[0],s="$"!=n[n.length-1];return i||s?new RegExp(`${i?"^":""}(?:${n})${s?"$":""}`,null!==(o=t.flags)&&void 0!==o?o:t.ignoreCase?"i":""):t}const M=u.define();const B=new WeakMap;function F(t){if(!Array.isArray(t))return t;let e=B.get(t);return e||B.set(t,e=A(t)),e}const j=a.define(),$=a.define();class N{constructor(o){this.pattern=o,this.chars=[],this.folded=[],this.any=[],this.precise=[],this.byWord=[],this.score=0,this.matched=[];for(let n=0;n<o.length;){let i=e(o,n),s=t(i);this.chars.push(i);let l=o.slice(n,n+s),r=l.toUpperCase();this.folded.push(e(r==l?l.toLowerCase():r,0)),n+=s}this.astral=o.length!=this.chars.length}ret(t,e){return this.score=t,this.matched=e,this}match(o){if(0==this.pattern.length)return this.ret(-100,[]);if(o.length<this.pattern.length)return null;let{chars:n,folded:i,any:s,precise:l,byWord:r}=this;if(1==n.length){let s=e(o,0),l=t(s),r=l==o.length?0:-100;if(s==n[0]);else{if(s!=i[0])return null;r+=-200}return this.ret(r,[0,l])}let a=o.indexOf(this.pattern);if(0==a)return this.ret(o.length==this.pattern.length?0:-100,[0,this.pattern.length]);let c=n.length,h=0;if(a<0){for(let l=0,r=Math.min(o.length,200);l<r&&h<c;){let r=e(o,l);r!=n[h]&&r!=i[h]||(s[h++]=l),l+=t(r)}if(h<c)return null}let p=0,u=0,d=!1,m=0,g=-1,v=-1,b=/[a-z]/.test(o),w=!0;for(let s=0,h=Math.min(o.length,200),y=0;s<h&&u<c;){let h=e(o,s);a<0&&(p<c&&h==n[p]&&(l[p++]=s),m<c&&(h==n[m]||h==i[m]?(0==m&&(g=s),v=s+1,m++):m=0));let x,C=h<255?h>=48&&h<=57||h>=97&&h<=122?2:h>=65&&h<=90?1:0:(x=f(h))!=x.toLowerCase()?1:x!=x.toUpperCase()?2:0;(!s||1==C&&b||0==y&&0!=C)&&(n[u]==h||i[u]==h&&(d=!0)?r[u++]=s:r.length&&(w=!1)),y=C,s+=t(h)}return u==c&&0==r[0]&&w?this.result((d?-200:0)-100,r,o):m==c&&0==g?this.ret(-200-o.length+(v==o.length?0:-100),[0,v]):a>-1?this.ret(-700-o.length,[a,a+this.pattern.length]):m==c?this.ret(-900-o.length,[g,v]):u==c?this.result((d?-200:0)-100-700+(w?0:-1100),r,o):2==n.length?null:this.result((s[0]?-700:0)-200-1100,s,o)}result(o,n,i){let s=[],l=0;for(let o of n){let n=o+(this.astral?t(e(i,o)):1);l&&s[l-1]==o?s[l-1]=n:(s[l++]=o,s[l++]=n)}return this.ret(o-i.length,s)}}class U{constructor(t){this.pattern=t,this.matched=[],this.score=0,this.folded=t.toLowerCase()}match(t){if(t.length<this.pattern.length)return null;let e=t.slice(0,this.pattern.length),o=e==this.pattern?0:e.toLowerCase()==this.folded?-200:null;return null==o?null:(this.matched=[0,e.length],this.score=o+(t.length==this.pattern.length?0:-100),this)}}const W=s.define({combine:t=>l(t,{activateOnTyping:!0,activateOnCompletion:()=>!1,activateOnTypingDelay:100,selectOnOpen:!0,override:null,closeOnBlur:!0,maxRenderedOptions:100,defaultKeymap:!0,tooltipClass:()=>"",optionClass:()=>"",aboveCursor:!1,icons:!0,addToOptions:[],positionInfo:H,filterStrict:!1,compareCompletions:(t,e)=>t.label.localeCompare(e.label),interactionDelay:75,updateSyncTime:100},{defaultKeymap:(t,e)=>t&&e,closeOnBlur:(t,e)=>t&&e,icons:(t,e)=>t&&e,tooltipClass:(t,e)=>o=>q(t(o),e(o)),optionClass:(t,e)=>o=>q(t(o),e(o)),addToOptions:(t,e)=>t.concat(e),filterStrict:(t,e)=>t||e})});function q(t,e){return t?e?t+" "+e:t:e}function H(t,e,o,n,i,s){let l,r,a=t.textDirection==b.RTL,c=a,h=!1,p="top",f=e.left-i.left,u=i.right-e.right,d=n.right-n.left,m=n.bottom-n.top;if(c&&f<Math.min(d,u)?c=!1:!c&&u<Math.min(d,f)&&(c=!0),d<=(c?f:u))l=Math.max(i.top,Math.min(o.top,i.bottom-m))-e.top,r=Math.min(400,c?f:u);else{h=!0,r=Math.min(400,(a?e.right:i.right-e.left)-30);let t=i.bottom-e.bottom;t>=m||t>e.top?l=o.bottom-e.top:(p="bottom",l=e.bottom-o.top)}return{style:`${p}: ${l/((e.bottom-e.top)/s.offsetHeight)}px; max-width: ${r/((e.right-e.left)/s.offsetWidth)}px`,class:"cm-completionInfo-"+(h?a?"left-narrow":"right-narrow":c?"left":"right")}}function V(t,e,o){if(t<=o)return{from:0,to:t};if(e<0&&(e=0),e<=t>>1){let t=Math.floor(e/o);return{from:t*o,to:(t+1)*o}}let n=Math.floor((t-e)/o);return{from:t-(n+1)*o,to:t-n*o}}class z{constructor(t,e,o){this.view=t,this.stateField=e,this.applyCompletion=o,this.info=null,this.infoDestroy=null,this.placeInfoReq={read:()=>this.measureInfo(),write:t=>this.placeInfo(t),key:this},this.space=null,this.currentClass="";let n=t.state.field(e),{options:i,selected:s}=n.open,l=t.state.facet(W);this.optionContent=function(t){let e=t.addToOptions.slice();return t.icons&&e.push({render(t){let e=document.createElement("div");return e.classList.add("cm-completionIcon"),t.type&&e.classList.add(...t.type.split(/\s+/g).map((t=>"cm-completionIcon-"+t))),e.setAttribute("aria-hidden","true"),e},position:20}),e.push({render(t,e,o,n){let i=document.createElement("span");i.className="cm-completionLabel";let s=t.displayLabel||t.label,l=0;for(let t=0;t<n.length;){let e=n[t++],o=n[t++];e>l&&i.appendChild(document.createTextNode(s.slice(l,e)));let r=i.appendChild(document.createElement("span"));r.appendChild(document.createTextNode(s.slice(e,o))),r.className="cm-completionMatchedText",l=o}return l<s.length&&i.appendChild(document.createTextNode(s.slice(l))),i},position:50},{render(t){if(!t.detail)return null;let e=document.createElement("span");return e.className="cm-completionDetail",e.textContent=t.detail,e},position:80}),e.sort(((t,e)=>t.position-e.position)).map((t=>t.render))}(l),this.optionClass=l.optionClass,this.tooltipClass=l.tooltipClass,this.range=V(i.length,s,l.maxRenderedOptions),this.dom=document.createElement("div"),this.dom.className="cm-tooltip-autocomplete",this.updateTooltipClass(t.state),this.dom.addEventListener("mousedown",(o=>{let{options:n}=t.state.field(e).open;for(let e,i=o.target;i&&i!=this.dom;i=i.parentNode)if("LI"==i.nodeName&&(e=/-(\d+)$/.exec(i.id))&&+e[1]<n.length)return this.applyCompletion(t,n[+e[1]]),void o.preventDefault()})),this.dom.addEventListener("focusout",(e=>{let o=t.state.field(this.stateField,!1);o&&o.tooltip&&t.state.facet(W).closeOnBlur&&e.relatedTarget!=t.contentDOM&&t.dispatch({effects:$.of(null)})})),this.showOptions(i,n.id)}mount(){this.updateSel()}showOptions(t,e){this.list&&this.list.remove(),this.list=this.dom.appendChild(this.createListBox(t,e,this.range)),this.list.addEventListener("scroll",(()=>{this.info&&this.view.requestMeasure(this.placeInfoReq)}))}update(t){var e;let o=t.state.field(this.stateField),n=t.startState.field(this.stateField);if(this.updateTooltipClass(t.state),o!=n){let{options:i,selected:s,disabled:l}=o.open;n.open&&n.open.options==i||(this.range=V(i.length,s,t.state.facet(W).maxRenderedOptions),this.showOptions(i,o.id)),this.updateSel(),l!=(null===(e=n.open)||void 0===e?void 0:e.disabled)&&this.dom.classList.toggle("cm-tooltip-autocomplete-disabled",!!l)}}updateTooltipClass(t){let e=this.tooltipClass(t);if(e!=this.currentClass){for(let t of this.currentClass.split(" "))t&&this.dom.classList.remove(t);for(let t of e.split(" "))t&&this.dom.classList.add(t);this.currentClass=e}}positioned(t){this.space=t,this.info&&this.view.requestMeasure(this.placeInfoReq)}updateSel(){let t=this.view.state.field(this.stateField),e=t.open;if((e.selected>-1&&e.selected<this.range.from||e.selected>=this.range.to)&&(this.range=V(e.options.length,e.selected,this.view.state.facet(W).maxRenderedOptions),this.showOptions(e.options,t.id)),this.updateSelectedOption(e.selected)){this.destroyInfo();let{completion:o}=e.options[e.selected],{info:n}=o;if(!n)return;let i="string"==typeof n?document.createTextNode(n):n(o);if(!i)return;"then"in i?i.then((e=>{e&&this.view.state.field(this.stateField,!1)==t&&this.addInfoPane(e,o)})).catch((t=>C(this.view.state,t,"completion info"))):this.addInfoPane(i,o)}}addInfoPane(t,e){this.destroyInfo();let o=this.info=document.createElement("div");if(o.className="cm-tooltip cm-completionInfo",null!=t.nodeType)o.appendChild(t),this.infoDestroy=null;else{let{dom:e,destroy:n}=t;o.appendChild(e),this.infoDestroy=n||null}this.dom.appendChild(o),this.view.requestMeasure(this.placeInfoReq)}updateSelectedOption(t){let e=null;for(let o=this.list.firstChild,n=this.range.from;o;o=o.nextSibling,n++)"LI"==o.nodeName&&o.id?n==t?o.hasAttribute("aria-selected")||(o.setAttribute("aria-selected","true"),e=o):o.hasAttribute("aria-selected")&&o.removeAttribute("aria-selected"):n--;return e&&function(t,e){let o=t.getBoundingClientRect(),n=e.getBoundingClientRect(),i=o.height/t.offsetHeight;n.top<o.top?t.scrollTop-=(o.top-n.top)/i:n.bottom>o.bottom&&(t.scrollTop+=(n.bottom-o.bottom)/i)}(this.list,e),e}measureInfo(){let t=this.dom.querySelector("[aria-selected]");if(!t||!this.info)return null;let e=this.dom.getBoundingClientRect(),o=this.info.getBoundingClientRect(),n=t.getBoundingClientRect(),i=this.space;if(!i){let t=this.dom.ownerDocument.defaultView||window;i={left:0,top:0,right:t.innerWidth,bottom:t.innerHeight}}return n.top>Math.min(i.bottom,e.bottom)-10||n.bottom<Math.max(i.top,e.top)+10?null:this.view.state.facet(W).positionInfo(this.view,e,n,o,i,this.dom)}placeInfo(t){this.info&&(t?(t.style&&(this.info.style.cssText=t.style),this.info.className="cm-tooltip cm-completionInfo "+(t.class||"")):this.info.style.cssText="top: -1e6px")}createListBox(t,e,o){const n=document.createElement("ul");n.id=e,n.setAttribute("role","listbox"),n.setAttribute("aria-expanded","true"),n.setAttribute("aria-label",this.view.state.phrase("Completions"));let i=null;for(let s=o.from;s<o.to;s++){let{completion:l,match:r}=t[s],{section:a}=l;if(a){let t="string"==typeof a?a:a.name;if(t!=i&&(s>o.from||0==o.from))if(i=t,"string"!=typeof a&&a.header)n.appendChild(a.header(a));else{n.appendChild(document.createElement("completion-section")).textContent=t}}const c=n.appendChild(document.createElement("li"));c.id=e+"-"+s,c.setAttribute("role","option");let h=this.optionClass(l);h&&(c.className=h);for(let t of this.optionContent){let e=t(l,this.view.state,this.view,r);e&&c.appendChild(e)}}return o.from&&n.classList.add("cm-completionListIncompleteTop"),o.to<t.length&&n.classList.add("cm-completionListIncompleteBottom"),n}destroyInfo(){this.info&&(this.infoDestroy&&this.infoDestroy(),this.info.remove(),this.info=null)}destroy(){this.destroyInfo()}}function K(t,e){return o=>new z(o,t,e)}function Q(t){return 100*(t.boost||0)+(t.apply?10:0)+(t.info?5:0)+(t.type?1:0)}class _{constructor(t,e,o,n,i,s){this.options=t,this.attrs=e,this.tooltip=o,this.timestamp=n,this.selected=i,this.disabled=s}setSelected(t,e){return t==this.selected||t>=this.options.length?this:new _(this.options,J(e,t),this.tooltip,this.timestamp,t,this.disabled)}static build(t,e,o,n,i){let s=function(t,e){let o=[],n=null,i=t=>{o.push(t);let{section:e}=t.completion;if(e){n||(n=[]);let t="string"==typeof e?e:e.name;n.some((e=>e.name==t))||n.push("string"==typeof e?{name:t}:e)}},s=e.facet(W);for(let n of t)if(n.hasResult()){let t=n.result.getMatch;if(!1===n.result.filter)for(let e of n.result.options)i(new R(e,n.source,t?t(e):[],1e9-o.length));else{let o,l=e.sliceDoc(n.from,n.to),r=s.filterStrict?new U(l):new N(l);for(let e of n.result.options)if(o=r.match(e.label)){let s=e.displayLabel?t?t(e,o.matched):[]:o.matched;i(new R(e,n.source,s,o.score+(e.boost||0)))}}}if(n){let t=Object.create(null),e=0,i=(t,e)=>{var o,n;return(null!==(o=t.rank)&&void 0!==o?o:1e9)-(null!==(n=e.rank)&&void 0!==n?n:1e9)||(t.name<e.name?-1:1)};for(let o of n.sort(i))e-=1e5,t[o.name]=e;for(let e of o){let{section:o}=e.completion;o&&(e.score+=t["string"==typeof o?o:o.name])}}let l=[],r=null,a=s.compareCompletions;for(let t of o.sort(((t,e)=>e.score-t.score||a(t.completion,e.completion)))){let e=t.completion;!r||r.label!=e.label||r.detail!=e.detail||null!=r.type&&null!=e.type&&r.type!=e.type||r.apply!=e.apply||r.boost!=e.boost?l.push(t):Q(t.completion)>Q(r)&&(l[l.length-1]=t),r=t.completion}return l}(t,e);if(!s.length)return n&&t.some((t=>1==t.state))?new _(n.options,n.attrs,n.tooltip,n.timestamp,n.selected,!0):null;let l=e.facet(W).selectOnOpen?0:-1;if(n&&n.selected!=l&&-1!=n.selected){let t=n.options[n.selected].completion;for(let e=0;e<s.length;e++)if(s[e].completion==t){l=e;break}}return new _(s,J(o,l),{pos:t.reduce(((t,e)=>e.hasResult()?Math.min(t,e.from):t),1e8),create:rt,above:i.aboveCursor},n?n.timestamp:Date.now(),l,!1)}map(t){return new _(this.options,this.attrs,Object.assign(Object.assign({},this.tooltip),{pos:t.mapPos(this.tooltip.pos)}),this.timestamp,this.selected,this.disabled)}}class X{constructor(t,e,o){this.active=t,this.id=e,this.open=o}static start(){return new X(Z,"cm-ac-"+Math.floor(2e6*Math.random()).toString(36),null)}update(t){let{state:e}=t,o=e.facet(W),n=(o.override||e.languageDataAt("autocomplete",E(e)).map(F)).map((e=>(this.active.find((t=>t.source==e))||new et(e,this.active.some((t=>0!=t.state))?1:0)).update(t,o)));n.length==this.active.length&&n.every(((t,e)=>t==this.active[e]))&&(n=this.active);let i=this.open;i&&t.docChanged&&(i=i.map(t.changes)),t.selection||n.some((e=>e.hasResult()&&t.changes.touchesRange(e.from,e.to)))||!function(t,e){if(t==e)return!0;for(let o=0,n=0;;){for(;o<t.length&&!t[o].hasResult;)o++;for(;n<e.length&&!e[n].hasResult;)n++;let i=o==t.length,s=n==e.length;if(i||s)return i==s;if(t[o++].result!=e[n++].result)return!1}}(n,this.active)?i=_.build(n,e,this.id,i,o):i&&i.disabled&&!n.some((t=>1==t.state))&&(i=null),!i&&n.every((t=>1!=t.state))&&n.some((t=>t.hasResult()))&&(n=n.map((t=>t.hasResult()?new et(t.source,0):t)));for(let e of t.effects)e.is(it)&&(i=i&&i.setSelected(e.value,this.id));return n==this.active&&i==this.open?this:new X(n,this.id,i)}get tooltip(){return this.open?this.open.tooltip:null}get attrs(){return this.open?this.open.attrs:this.active.length?Y:G}}const Y={"aria-autocomplete":"list"},G={};function J(t,e){let o={"aria-autocomplete":"list","aria-haspopup":"listbox","aria-controls":t};return e>-1&&(o["aria-activedescendant"]=t+"-"+e),o}const Z=[];function tt(t,e){if(t.isUserEvent("input.complete")){let o=t.annotation(M);if(o&&e.activateOnCompletion(o))return 12}let o=t.isUserEvent("input.type");return o&&e.activateOnTyping?5:o?1:t.isUserEvent("delete.backward")?2:t.selection?8:t.docChanged?16:0}class et{constructor(t,e,o=-1){this.source=t,this.state=e,this.explicitPos=o}hasResult(){return!1}update(t,e){let o=tt(t,e),n=this;(8&o||16&o&&this.touches(t))&&(n=new et(n.source,0)),4&o&&0==n.state&&(n=new et(this.source,1)),n=n.updateFor(t,o);for(let e of t.effects)if(e.is(j))n=new et(n.source,1,e.value?E(t.state):-1);else if(e.is($))n=new et(n.source,0);else if(e.is(nt))for(let t of e.value)t.source==n.source&&(n=t);return n}updateFor(t,e){return this.map(t.changes)}map(t){return t.empty||this.explicitPos<0?this:new et(this.source,this.state,t.mapPos(this.explicitPos))}touches(t){return t.changes.touchesRange(E(t.state))}}class ot extends et{constructor(t,e,o,n,i){super(t,2,e),this.result=o,this.from=n,this.to=i}hasResult(){return!0}updateFor(t,e){var o;if(!(3&e))return this.map(t.changes);let n=this.result;n.map&&!t.changes.empty&&(n=n.map(n,t.changes));let i=t.changes.mapPos(this.from),s=t.changes.mapPos(this.to,1),l=E(t.state);if((this.explicitPos<0?l<=i:l<this.from)||l>s||!n||2&e&&E(t.startState)==this.from)return new et(this.source,4&e?1:0);let r=this.explicitPos<0?-1:t.changes.mapPos(this.explicitPos);return function(t,e,o,n){if(!t)return!1;let i=e.sliceDoc(o,n);return"function"==typeof t?t(i,o,n,e):P(t,!0).test(i)}(n.validFor,t.state,i,s)?new ot(this.source,r,n,i,s):n.update&&(n=n.update(n,i,s,new T(t.state,l,r>=0)))?new ot(this.source,r,n,n.from,null!==(o=n.to)&&void 0!==o?o:E(t.state)):new et(this.source,1,r)}map(t){if(t.empty)return this;return(this.result.map?this.result.map(this.result,t):this.result)?new ot(this.source,this.explicitPos<0?-1:t.mapPos(this.explicitPos),this.result,t.mapPos(this.from),t.mapPos(this.to,1)):new et(this.source,0)}touches(t){return t.changes.touchesRange(this.from,this.to)}}const nt=a.define({map:(t,e)=>t.map((t=>t.map(e)))}),it=a.define(),st=r.define({create:()=>X.start(),update:(t,e)=>t.update(e),provide:t=>[w.from(t,(t=>t.tooltip)),g.contentAttributes.from(t,(t=>t.attrs))]});function lt(t,e){const n=e.completion.apply||e.completion.label;let i=t.state.field(st).active.find((t=>t.source==e.source));return i instanceof ot&&("string"==typeof n?t.dispatch(Object.assign(Object.assign({},function(t,e,n,i){let{main:s}=t.selection,l=n-s.from,r=i-s.from;return Object.assign(Object.assign({},t.changeByRange((a=>{if(a!=s&&n!=i&&t.sliceDoc(a.from+l,a.from+r)!=t.sliceDoc(n,i))return{range:a};let c=t.toText(e);return{changes:{from:a.from+l,to:i==s.from?a.to:a.from+r,insert:c},range:o.cursor(a.from+l+c.length)}}))),{scrollIntoView:!0,userEvent:"input.complete"})}(t.state,n,i.from,i.to)),{annotations:M.of(e.completion)})):n(t,e.completion,i.from,i.to),!0)}const rt=K(st,lt);function at(t,e="option"){return o=>{let n=o.state.field(st,!1);if(!n||!n.open||n.open.disabled||Date.now()-n.open.timestamp<o.state.facet(W).interactionDelay)return!1;let i,s=1;"page"==e&&(i=y(o,n.open.tooltip))&&(s=Math.max(2,Math.floor(i.dom.offsetHeight/i.dom.querySelector("li").offsetHeight)-1));let{length:l}=n.open.options,r=n.open.selected>-1?n.open.selected+s*(t?1:-1):t?0:l-1;return r<0?r="page"==e?0:l-1:r>=l&&(r="page"==e?l-1:0),o.dispatch({effects:it.of(r)}),!0}}const ct=t=>!!t.state.field(st,!1)&&(t.dispatch({effects:j.of(!0)}),!0);class ht{constructor(t,e){this.active=t,this.context=e,this.time=Date.now(),this.updates=[],this.done=void 0}}const pt=x.fromClass(class{constructor(t){this.view=t,this.debounceUpdate=-1,this.running=[],this.debounceAccept=-1,this.pendingStart=!1,this.composing=0;for(let e of t.state.field(st).active)1==e.state&&this.startQuery(e)}update(t){let e=t.state.field(st),o=t.state.facet(W);if(!t.selectionSet&&!t.docChanged&&t.startState.field(st)==e)return;let n=t.transactions.some((t=>{let e=tt(t,o);return 8&e||(t.selection||t.docChanged)&&!(3&e)}));for(let e=0;e<this.running.length;e++){let o=this.running[e];if(n||o.context.abortOnDocChange&&t.docChanged||o.updates.length+t.transactions.length>50&&Date.now()-o.time>1e3){for(let t of o.context.abortListeners)try{t()}catch(t){C(this.view.state,t)}o.context.abortListeners=null,this.running.splice(e--,1)}else o.updates.push(...t.transactions)}this.debounceUpdate>-1&&clearTimeout(this.debounceUpdate),t.transactions.some((t=>t.effects.some((t=>t.is(j)))))&&(this.pendingStart=!0);let i=this.pendingStart?50:o.activateOnTypingDelay;if(this.debounceUpdate=e.active.some((t=>1==t.state&&!this.running.some((e=>e.active.source==t.source))))?setTimeout((()=>this.startUpdate()),i):-1,0!=this.composing)for(let e of t.transactions)e.isUserEvent("input.type")?this.composing=2:2==this.composing&&e.selection&&(this.composing=3)}startUpdate(){this.debounceUpdate=-1,this.pendingStart=!1;let{state:t}=this.view,e=t.field(st);for(let t of e.active)1!=t.state||this.running.some((e=>e.active.source==t.source))||this.startQuery(t)}startQuery(t){let{state:e}=this.view,o=E(e),n=new T(e,o,t.explicitPos==o,this.view),i=new ht(t,n);this.running.push(i),Promise.resolve(t.source(n)).then((t=>{i.context.aborted||(i.done=t||null,this.scheduleAccept())}),(t=>{this.view.dispatch({effects:$.of(null)}),C(this.view.state,t)}))}scheduleAccept(){this.running.every((t=>void 0!==t.done))?this.accept():this.debounceAccept<0&&(this.debounceAccept=setTimeout((()=>this.accept()),this.view.state.facet(W).updateSyncTime))}accept(){var t;this.debounceAccept>-1&&clearTimeout(this.debounceAccept),this.debounceAccept=-1;let e=[],o=this.view.state.facet(W);for(let n=0;n<this.running.length;n++){let i=this.running[n];if(void 0===i.done)continue;if(this.running.splice(n--,1),i.done){let n=new ot(i.active.source,i.active.explicitPos,i.done,i.done.from,null!==(t=i.done.to)&&void 0!==t?t:E(i.updates.length?i.updates[0].startState:this.view.state));for(let t of i.updates)n=n.update(t,o);if(n.hasResult()){e.push(n);continue}}let s=this.view.state.field(st).active.find((t=>t.source==i.active.source));if(s&&1==s.state)if(null==i.done){let t=new et(i.active.source,0);for(let e of i.updates)t=t.update(e,o);1!=t.state&&e.push(t)}else this.startQuery(s)}e.length&&this.view.dispatch({effects:nt.of(e)})}},{eventHandlers:{blur(t){let e=this.view.state.field(st,!1);if(e&&e.tooltip&&this.view.state.facet(W).closeOnBlur){let o=e.open&&y(this.view,e.open.tooltip);o&&o.dom.contains(t.relatedTarget)||setTimeout((()=>this.view.dispatch({effects:$.of(null)})),10)}},compositionstart(){this.composing=1},compositionend(){3==this.composing&&setTimeout((()=>this.view.dispatch({effects:j.of(!1)})),20),this.composing=0}}}),ft="object"==typeof navigator&&/Win/.test(navigator.platform),ut=i.highest(g.domEventHandlers({keydown(t,e){let o=e.state.field(st,!1);if(!o||!o.open||o.open.disabled||o.open.selected<0||t.key.length>1||t.ctrlKey&&(!ft||!t.altKey)||t.metaKey)return!1;let n=o.open.options[o.open.selected],i=o.active.find((t=>t.source==n.source)),s=n.completion.commitCharacters||i.result.commitCharacters;return s&&s.indexOf(t.key)>-1&&lt(e,n),!1}})),dt=g.baseTheme({".cm-tooltip.cm-tooltip-autocomplete":{"& > ul":{fontFamily:"monospace",whiteSpace:"nowrap",overflow:"hidden auto",maxWidth_fallback:"700px",maxWidth:"min(700px, 95vw)",minWidth:"250px",maxHeight:"10em",height:"100%",listStyle:"none",margin:0,padding:0,"& > li, & > completion-section":{padding:"1px 3px",lineHeight:1.2},"& > li":{overflowX:"hidden",textOverflow:"ellipsis",cursor:"pointer"},"& > completion-section":{display:"list-item",borderBottom:"1px solid silver",paddingLeft:"0.5em",opacity:.7}}},"&light .cm-tooltip-autocomplete ul li[aria-selected]":{background:"#17c",color:"white"},"&light .cm-tooltip-autocomplete-disabled ul li[aria-selected]":{background:"#777"},"&dark .cm-tooltip-autocomplete ul li[aria-selected]":{background:"#347",color:"white"},"&dark .cm-tooltip-autocomplete-disabled ul li[aria-selected]":{background:"#444"},".cm-completionListIncompleteTop:before, .cm-completionListIncompleteBottom:after":{content:'"···"',opacity:.5,display:"block",textAlign:"center"},".cm-tooltip.cm-completionInfo":{position:"absolute",padding:"3px 9px",width:"max-content",maxWidth:"400px",boxSizing:"border-box",whiteSpace:"pre-line"},".cm-completionInfo.cm-completionInfo-left":{right:"100%"},".cm-completionInfo.cm-completionInfo-right":{left:"100%"},".cm-completionInfo.cm-completionInfo-left-narrow":{right:"30px"},".cm-completionInfo.cm-completionInfo-right-narrow":{left:"30px"},"&light .cm-snippetField":{backgroundColor:"#00000022"},"&dark .cm-snippetField":{backgroundColor:"#ffffff22"},".cm-snippetFieldPosition":{verticalAlign:"text-top",width:0,height:"1.15em",display:"inline-block",margin:"0 -0.7px -.7em",borderLeft:"1.4px dotted #888"},".cm-completionMatchedText":{textDecoration:"underline"},".cm-completionDetail":{marginLeft:"0.5em",fontStyle:"italic"},".cm-completionIcon":{fontSize:"90%",width:".8em",display:"inline-block",textAlign:"center",paddingRight:".6em",opacity:"0.6",boxSizing:"content-box"},".cm-completionIcon-function, .cm-completionIcon-method":{"&:after":{content:"'ƒ'"}},".cm-completionIcon-class":{"&:after":{content:"'○'"}},".cm-completionIcon-interface":{"&:after":{content:"'◌'"}},".cm-completionIcon-variable":{"&:after":{content:"'𝑥'"}},".cm-completionIcon-constant":{"&:after":{content:"'𝐶'"}},".cm-completionIcon-type":{"&:after":{content:"'𝑡'"}},".cm-completionIcon-enum":{"&:after":{content:"'∪'"}},".cm-completionIcon-property":{"&:after":{content:"'□'"}},".cm-completionIcon-keyword":{"&:after":{content:"'🔑︎'"}},".cm-completionIcon-namespace":{"&:after":{content:"'▢'"}},".cm-completionIcon-text":{"&:after":{content:"'abc'",fontSize:"50%",verticalAlign:"middle"}}});class mt{constructor(t,e,o,n){this.field=t,this.line=e,this.from=o,this.to=n}}class gt{constructor(t,e,o){this.field=t,this.from=e,this.to=o}map(t){let e=t.mapPos(this.from,-1,c.TrackDel),o=t.mapPos(this.to,1,c.TrackDel);return null==e||null==o?null:new gt(this.field,e,o)}}class vt{constructor(t,e){this.lines=t,this.fieldPositions=e}instantiate(t,e){let o=[],n=[e],i=t.doc.lineAt(e),s=/^\s*/.exec(i.text)[0];for(let i of this.lines){if(o.length){let o=s,l=/^\t*/.exec(i)[0].length;for(let e=0;e<l;e++)o+=t.facet(D);n.push(e+o.length-l),i=o+i.slice(l)}o.push(i),e+=i.length+1}let l=this.fieldPositions.map((t=>new gt(t.field,n[t.line]+t.from,n[t.line]+t.to)));return{text:o,ranges:l}}static parse(t){let e,o=[],n=[],i=[];for(let s of t.split(/\r\n?|\n/)){for(;e=/[#$]\{(?:(\d+)(?::([^}]*))?|((?:\\[{}]|[^}])*))\}/.exec(s);){let t=e[1]?+e[1]:null,l=e[2]||e[3]||"",r=-1,a=l.replace(/\\[{}]/g,(t=>t[1]));for(let e=0;e<o.length;e++)(null!=t?o[e].seq==t:a&&o[e].name==a)&&(r=e);if(r<0){let e=0;for(;e<o.length&&(null==t||null!=o[e].seq&&o[e].seq<t);)e++;o.splice(e,0,{seq:t,name:a}),r=e;for(let t of i)t.field>=r&&t.field++}i.push(new mt(r,n.length,e.index,e.index+a.length)),s=s.slice(0,e.index)+l+s.slice(e.index+e[0].length)}s=s.replace(/\\([{}])/g,((t,e,o)=>{for(let t of i)t.line==n.length&&t.from>o&&(t.from--,t.to--);return e})),n.push(s)}return new vt(n,i)}}let bt=I.widget({widget:new class extends O{toDOM(){let t=document.createElement("span");return t.className="cm-snippetFieldPosition",t}ignoreEvent(){return!1}}}),wt=I.mark({class:"cm-snippetField"});class yt{constructor(t,e){this.ranges=t,this.active=e,this.deco=I.set(t.map((t=>(t.from==t.to?bt:wt).range(t.from,t.to))))}map(t){let e=[];for(let o of this.ranges){let n=o.map(t);if(!n)return null;e.push(n)}return new yt(e,this.active)}selectionInsideField(t){return t.ranges.every((t=>this.ranges.some((e=>e.field==this.active&&e.from<=t.from&&e.to>=t.to))))}}const xt=a.define({map:(t,e)=>t&&t.map(e)}),Ct=a.define(),It=r.define({create:()=>null,update(t,e){for(let o of e.effects){if(o.is(xt))return o.value;if(o.is(Ct)&&t)return new yt(t.ranges,o.value)}return t&&e.docChanged&&(t=t.map(e.changes)),t&&e.selection&&!t.selectionInsideField(e.selection)&&(t=null),t},provide:t=>g.decorations.from(t,(t=>t?t.deco:I.none))});function Ot(t,e){return o.create(t.filter((t=>t.field==e)).map((t=>o.range(t.from,t.to))))}function kt(t){let e=vt.parse(t);return(t,o,n,i)=>{let{text:s,ranges:l}=e.instantiate(t.state,n),r={changes:{from:n,to:i,insert:d.of(s)},scrollIntoView:!0,annotations:o?[M.of(o),m.userEvent.of("input.complete")]:void 0};if(l.length&&(r.selection=Ot(l,0)),l.some((t=>t.field>0))){let e=new yt(l,0),o=r.effects=[xt.of(e)];void 0===t.state.field(It,!1)&&o.push(a.appendConfig.of([It,At,Rt,dt]))}t.dispatch(t.state.update(r))}}function Dt(t){return({state:e,dispatch:o})=>{let n=e.field(It,!1);if(!n||t<0&&0==n.active)return!1;let i=n.active+t,s=t>0&&!n.ranges.some((e=>e.field==i+t));return o(e.update({selection:Ot(n.ranges,i),effects:xt.of(s?null:new yt(n.ranges,i)),scrollIntoView:!0})),!0}}const Tt=[{key:"Tab",run:Dt(1),shift:Dt(-1)},{key:"Escape",run:({state:t,dispatch:e})=>!!t.field(It,!1)&&(e(t.update({effects:xt.of(null)})),!0)}],St=s.define({combine:t=>t.length?t[0]:Tt}),At=i.highest(v.compute([St],(t=>t.facet(St))));function Lt(t,e){return Object.assign(Object.assign({},e),{apply:kt(t)})}const Rt=g.domEventHandlers({mousedown(t,e){let o,n=e.state.field(It,!1);if(!n||null==(o=e.posAtCoords({x:t.clientX,y:t.clientY})))return!1;let i=n.ranges.find((t=>t.from<=o&&t.to>=o));return!(!i||i.field==n.active)&&(e.dispatch({selection:Ot(n.ranges,i.field),effects:xt.of(n.ranges.some((t=>t.field>i.field))?new yt(n.ranges,i.field):null),scrollIntoView:!0}),!0)}}),Et={brackets:["(","[","{","'",'"'],before:")]}:;>",stringPrefixes:[]},Pt=a.define({map(t,e){let o=e.mapPos(t,-1,c.TrackAfter);return null==o?void 0:o}}),Mt=new class extends h{};Mt.startSide=1,Mt.endSide=-1;const Bt=r.define({create:()=>p.empty,update(t,e){if(t=t.map(e.changes),e.selection){let o=e.state.doc.lineAt(e.selection.main.head);t=t.update({filter:t=>t>=o.from&&t<=o.to})}for(let o of e.effects)o.is(Pt)&&(t=t.update({add:[Mt.range(o.value,o.value+1)]}));return t}});function Ft(){return[Wt,Bt]}const jt="()[]{}<>";function $t(t){for(let e=0;e<8;e+=2)if(jt.charCodeAt(e)==t)return jt.charAt(e+1);return f(t<128?t:t+1)}function Nt(t,e){return t.languageDataAt("closeBrackets",e)[0]||Et}const Ut="object"==typeof navigator&&/Android\b/.test(navigator.userAgent),Wt=g.inputHandler.of(((o,n,i,s)=>{if((Ut?o.composing:o.compositionStarted)||o.state.readOnly)return!1;let l=o.state.selection.main;if(s.length>2||2==s.length&&1==t(e(s,0))||n!=l.from||i!=l.to)return!1;let r=function(t,o){let n=Nt(t,t.selection.main.head),i=n.brackets||Et.brackets;for(let s of i){let l=$t(e(s,0));if(o==s)return l==s?Qt(t,s,i.indexOf(s+s+s)>-1,n):zt(t,s,l,n.before||Et.before);if(o==l&&Ht(t,t.selection.main.from))return Kt(t,s,l)}return null}(o.state,s);return!!r&&(o.dispatch(r),!0)})),qt=[{key:"Backspace",run:({state:n,dispatch:i})=>{if(n.readOnly)return!1;let s=Nt(n,n.selection.main.head).brackets||Et.brackets,l=null,r=n.changeByRange((i=>{if(i.empty){let l=function(o,n){let i=o.sliceString(n-2,n);return t(e(i,0))==i.length?i:i.slice(1)}(n.doc,i.head);for(let t of s)if(t==l&&Vt(n.doc,i.head)==$t(e(t,0)))return{changes:{from:i.head-t.length,to:i.head+t.length},range:o.cursor(i.head-t.length)}}return{range:l=i}}));return l||i(n.update(r,{scrollIntoView:!0,userEvent:"delete.backward"})),!l}}];function Ht(t,e){let o=!1;return t.field(Bt).between(0,t.doc.length,(t=>{t==e&&(o=!0)})),o}function Vt(o,n){let i=o.sliceString(n,n+2);return i.slice(0,t(e(i,0)))}function zt(t,e,n,i){let s=null,l=t.changeByRange((l=>{if(!l.empty)return{changes:[{insert:e,from:l.from},{insert:n,from:l.to}],effects:Pt.of(l.to+e.length),range:o.range(l.anchor+e.length,l.head+e.length)};let r=Vt(t.doc,l.head);return!r||/\s/.test(r)||i.indexOf(r)>-1?{changes:{insert:e+n,from:l.head},effects:Pt.of(l.head+e.length),range:o.cursor(l.head+e.length)}:{range:s=l}}));return s?null:t.update(l,{scrollIntoView:!0,userEvent:"input.type"})}function Kt(t,e,n){let i=null,s=t.changeByRange((e=>e.empty&&Vt(t.doc,e.head)==n?{changes:{from:e.head,to:e.head+n.length,insert:n},range:o.cursor(e.head+n.length)}:i={range:e}));return i?null:t.update(s,{scrollIntoView:!0,userEvent:"input.type"})}function Qt(t,e,i,s){let l=s.stringPrefixes||Et.stringPrefixes,r=null,a=t.changeByRange((s=>{if(!s.empty)return{changes:[{insert:e,from:s.from},{insert:e,from:s.to}],effects:Pt.of(s.to+e.length),range:o.range(s.anchor+e.length,s.head+e.length)};let a,c=s.head,h=Vt(t.doc,c);if(h==e){if(_t(t,c))return{changes:{insert:e+e,from:c},effects:Pt.of(c+e.length),range:o.cursor(c+e.length)};if(Ht(t,c)){let n=i&&t.sliceDoc(c,c+3*e.length)==e+e+e?e+e+e:e;return{changes:{from:c,to:c+n.length,insert:n},range:o.cursor(c+n.length)}}}else{if(i&&t.sliceDoc(c-2*e.length,c)==e+e&&(a=Xt(t,c-2*e.length,l))>-1&&_t(t,a))return{changes:{insert:e+e+e+e,from:c},effects:Pt.of(c+e.length),range:o.cursor(c+e.length)};if(t.charCategorizer(c)(h)!=n.Word&&Xt(t,c,l)>-1&&!function(t,e,o,n){let i=k(t).resolveInner(e,-1),s=n.reduce(((t,e)=>Math.max(t,e.length)),0);for(let l=0;l<5;l++){let l=t.sliceDoc(i.from,Math.min(i.to,i.from+o.length+s)),r=l.indexOf(o);if(!r||r>-1&&n.indexOf(l.slice(0,r))>-1){let e=i.firstChild;for(;e&&e.from==i.from&&e.to-e.from>o.length+r;){if(t.sliceDoc(e.to-o.length,e.to)==o)return!1;e=e.firstChild}return!0}let a=i.to==e&&i.parent;if(!a)break;i=a}return!1}(t,c,e,l))return{changes:{insert:e+e,from:c},effects:Pt.of(c+e.length),range:o.cursor(c+e.length)}}return{range:r=s}}));return r?null:t.update(a,{scrollIntoView:!0,userEvent:"input.type"})}function _t(t,e){let o=k(t).resolveInner(e+1);return o.parent&&o.from==e}function Xt(t,e,o){let i=t.charCategorizer(e);if(i(t.sliceDoc(e-1,e))!=n.Word)return e;for(let s of o){let o=e-s.length;if(t.sliceDoc(o,e)==s&&i(t.sliceDoc(o-1,o))!=n.Word)return o}return-1}function Yt(t={}){return[ut,st,W.of(t),pt,Jt,dt]}const Gt=[{key:"Ctrl-Space",run:ct},{mac:"Alt-`",run:ct},{key:"Escape",run:t=>{let e=t.state.field(st,!1);return!(!e||!e.active.some((t=>0!=t.state)))&&(t.dispatch({effects:$.of(null)}),!0)}},{key:"ArrowDown",run:at(!0)},{key:"ArrowUp",run:at(!1)},{key:"PageDown",run:at(!0,"page")},{key:"PageUp",run:at(!1,"page")},{key:"Enter",run:t=>{let e=t.state.field(st,!1);return!(t.state.readOnly||!e||!e.open||e.open.selected<0||e.open.disabled||Date.now()-e.open.timestamp<t.state.facet(W).interactionDelay)&&lt(t,e.open.options[e.open.selected])}}],Jt=i.highest(v.computeN([W],(t=>t.facet(W).defaultKeymap?[Gt]:[])));export{Ft as a,Yt as b,A as c,qt as d,Gt as e,L as i,Lt as s};
//# sourceMappingURL=index-qze_Ijc7.js.map