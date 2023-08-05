/*! For license information please see chunk.bab7ec358159dc18d1e0.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1823],{63207:function(t,e,n){"use strict";n(65660),n(15112);var i=n(9672),r=n(87156),o=n(50856),s=n(43437);function a(){var t=function(t,e){e||(e=t.slice(0));return Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))}(["\n    <style>\n      :host {\n        @apply --layout-inline;\n        @apply --layout-center-center;\n        position: relative;\n\n        vertical-align: middle;\n\n        fill: var(--iron-icon-fill-color, currentcolor);\n        stroke: var(--iron-icon-stroke-color, none);\n\n        width: var(--iron-icon-width, 24px);\n        height: var(--iron-icon-height, 24px);\n        @apply --iron-icon;\n      }\n\n      :host([hidden]) {\n        display: none;\n      }\n    </style>\n"]);return a=function(){return t},t}(0,i.k)({_template:(0,o.d)(a()),is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,r.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,r.vz)(this.root).appendChild(this._img))}})},15112:function(t,e,n){"use strict";n.d(e,{P:function(){return o}});n(43437);var i=n(9672);function r(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}var o=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),t[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}var e,n,i;return e=t,(n=[{key:"byKey",value:function(t){return this.key=t,this.value}},{key:"value",get:function(){var e=this.type,n=this.key;if(e&&n)return t.types[e]&&t.types[e][n]},set:function(e){var n=this.type,i=this.key;n&&i&&(n=t.types[n]=t.types[n]||{},null==e?delete n[i]:n[i]=e)}},{key:"list",get:function(){if(this.type){var e=t.types[this.type];return e?Object.keys(e).map((function(t){return s[this.type][t]}),this):[]}}}])&&r(e.prototype,n),i&&r(e,i),t}();o[" "]=function(){},o.types={};var s=o.types;(0,i.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,n){var i=new o({type:t,key:e});return void 0!==n&&n!==i.value?i.value=n:this.value!==i.value&&(this.value=i.value),i},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new o({type:this.type,key:t}).value}})},58993:function(t,e,n){"use strict";function i(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function r(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}n.d(e,{yh:function(){return s},U2:function(){return c},t8:function(){return u},ZH:function(){return h}});var o,s=function(){function t(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"keyval-store",n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"keyval";i(this,t),this.storeName=n,this._dbp=new Promise((function(t,i){var r=indexedDB.open(e,1);r.onerror=function(){return i(r.error)},r.onsuccess=function(){return t(r.result)},r.onupgradeneeded=function(){r.result.createObjectStore(n)}}))}var e,n,o;return e=t,(n=[{key:"_withIDBStore",value:function(t,e){var n=this;return this._dbp.then((function(i){return new Promise((function(r,o){var s=i.transaction(n.storeName,t);s.oncomplete=function(){return r()},s.onabort=s.onerror=function(){return o(s.error)},e(s.objectStore(n.storeName))}))}))}}])&&r(e.prototype,n),o&&r(e,o),t}();function a(){return o||(o=new s),o}function c(t){var e,n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:a();return n._withIDBStore("readonly",(function(n){e=n.get(t)})).then((function(){return e.result}))}function u(t,e){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:a();return n._withIDBStore("readwrite",(function(n){n.put(e,t)}))}function h(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:a();return t._withIDBStore("readwrite",(function(t){t.clear()}))}}}]);
//# sourceMappingURL=chunk.bab7ec358159dc18d1e0.js.map