(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[4482],{73728:function(e,t,r){"use strict";r.d(t,{pV:function(){return a},P3:function(){return c},Ky:function(){return s},D4:function(){return l},XO:function(){return u},zO:function(){return d},oi:function(){return f},d4:function(){return p},ZJ:function(){return v},V3:function(){return y},WW:function(){return b}});var n=r(95282),i=r(38346),o=r(5986),a=["unignore","homekit","ssdp","zeroconf","discovery","mqtt"],c=["reauth"],s=function(e,t){var r;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(r=e.userData)||void 0===r?void 0:r.showAdvanced)})},l=function(e,t){return e.callApi("GET","config/config_entries/flow/".concat(t))},u=function(e,t,r){return e.callApi("POST","config/config_entries/flow/".concat(t),r)},d=function(e,t){return e.callWS({type:"config_entries/ignore_flow",flow_id:t})},f=function(e,t){return e.callApi("DELETE","config/config_entries/flow/".concat(t))},p=function(e){return e.callApi("GET","config/config_entries/flow_handlers")},h=function(e){return e.sendMessagePromise({type:"config_entries/flow/progress"})},m=function(e,t){return e.subscribeEvents((0,i.D)((function(){return h(e).then((function(e){return t.setState(e,!0)}))}),500,!0),"config_entry_discovered")},v=function(e){return(0,n._)(e,"_configFlowProgress",h,m)},y=function(e,t){return v(e.connection).subscribe(t)},b=function(e,t){var r=t.context.title_placeholders||{},n=Object.keys(r);if(0===n.length)return(0,o.Lh)(e,t.handler);var i=[];return n.forEach((function(e){i.push(e),i.push(r[e])})),e.apply(void 0,["component.".concat(t.handler,".config.flow_title")].concat(i))}},2852:function(e,t,r){"use strict";r.d(t,{t:function(){return k}});var n=r(15652),i=r(85415),o=r(91177),a=r(73728),c=r(5986),s=r(52871);function l(){var e=v(["\n            <ha-markdown allowsvg breaks .content=","></ha-markdown>\n          "]);return l=function(){return e},e}function u(){var e=v(["\n              <ha-markdown\n                allowsvg\n                breaks\n                .content=","\n              ></ha-markdown>\n            "]);return u=function(){return e},e}function d(){var e=v(["\n        ","\n        <p>\n          ","\n        </p>\n      "]);return d=function(){return e},e}function f(){var e=v(["\n              <ha-markdown\n                allowsvg\n                breaks\n                .content=","\n              ></ha-markdown>\n            "]);return f=function(){return e},e}function p(){var e=v(["\n        <p>\n          ","\n        </p>\n        ","\n      "]);return p=function(){return e},e}function h(){var e=v(["\n            <ha-markdown allowsvg breaks .content=","></ha-markdown>\n          "]);return h=function(){return e},e}function m(){var e=v(["\n            <ha-markdown allowsvg breaks .content=","></ha-markdown>\n          "]);return m=function(){return e},e}function v(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function y(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if("undefined"==typeof Symbol||!(Symbol.iterator in Object(e)))return;var r=[],n=!0,i=!1,o=void 0;try{for(var a,c=e[Symbol.iterator]();!(n=(a=c.next()).done)&&(r.push(a.value),!t||r.length!==t);n=!0);}catch(s){i=!0,o=s}finally{try{n||null==c.return||c.return()}finally{if(i)throw o}}return r}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return b(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function w(e,t,r,n,i,o,a){try{var c=e[o](a),s=c.value}catch(l){return void r(l)}c.done?t(s):Promise.resolve(s).then(n,i)}function g(e){return function(){var t=this,r=arguments;return new Promise((function(n,i){var o=e.apply(t,r);function a(e){w(o,n,i,a,c,"next",e)}function c(e){w(o,n,i,a,c,"throw",e)}a(void 0)}))}}var k=function(e,t){return(0,s.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:(b=g(regeneratorRuntime.mark((function e(t){var r,n,o;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.all([(0,a.d4)(t),t.loadBackendTranslation("title",void 0,!0)]);case 2:return r=e.sent,n=y(r,1),o=n[0],e.abrupt("return",o.sort((function(e,r){return(0,i.w)((0,c.Lh)(t.localize,e),(0,c.Lh)(t.localize,r))})));case 6:case"end":return e.stop()}}),e)}))),function(e){return b.apply(this,arguments)}),createFlow:(v=g(regeneratorRuntime.mark((function e(t,r){var n,i,o;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.all([(0,a.Ky)(t,r),t.loadBackendTranslation("config",r)]);case 2:return n=e.sent,i=y(n,1),o=i[0],e.abrupt("return",o);case 6:case"end":return e.stop()}}),e)}))),function(e,t){return v.apply(this,arguments)}),fetchFlow:(r=g(regeneratorRuntime.mark((function e(t,r){var n;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,a.D4)(t,r);case 2:return n=e.sent,e.next=5,t.loadBackendTranslation("config",n.handler);case 5:return e.abrupt("return",n);case 6:case"end":return e.stop()}}),e)}))),function(e,t){return r.apply(this,arguments)}),handleFlowStep:a.XO,deleteFlow:a.oi,renderAbortDescription:function(e,t){var r=(0,o.I)(e.localize,"component.".concat(t.handler,".config.abort.").concat(t.reason),t.description_placeholders);return r?(0,n.dy)(m(),r):""},renderShowFormStepHeader:function(e,t){return e.localize("component.".concat(t.handler,".config.step.").concat(t.step_id,".title"))||e.localize("component.".concat(t.handler,".title"))},renderShowFormStepDescription:function(e,t){var r=(0,o.I)(e.localize,"component.".concat(t.handler,".config.step.").concat(t.step_id,".description"),t.description_placeholders);return r?(0,n.dy)(h(),r):""},renderShowFormStepFieldLabel:function(e,t,r){return e.localize("component.".concat(t.handler,".config.step.").concat(t.step_id,".data.").concat(r.name))},renderShowFormStepFieldError:function(e,t,r){return e.localize("component.".concat(t.handler,".config.error.").concat(r))},renderExternalStepHeader:function(e,t){return e.localize("component.".concat(t.handler,".config.step.").concat(t.step_id,".title"))||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site")},renderExternalStepDescription:function(e,t){var r=(0,o.I)(e.localize,"component.".concat(t.handler,".config.").concat(t.step_id,".description"),t.description_placeholders);return(0,n.dy)(p(),e.localize("ui.panel.config.integrations.config_flow.external_step.description"),r?(0,n.dy)(f(),r):"")},renderCreateEntryDescription:function(e,t){var r=(0,o.I)(e.localize,"component.".concat(t.handler,".config.create_entry.").concat(t.description||"default"),t.description_placeholders);return(0,n.dy)(d(),r?(0,n.dy)(u(),r):"",e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title))},renderShowFormProgressHeader:function(e,t){return e.localize("component.".concat(t.handler,".title"))},renderShowFormProgressDescription:function(e,t){var r=(0,o.I)(e.localize,"component.".concat(t.handler,".config.progress.").concat(t.progress_action),t.description_placeholders);return r?(0,n.dy)(l(),r):""}});var r,v,b}},52871:function(e,t,r){"use strict";r.d(t,{w:function(){return o}});var n=r(47181),i=function(){return Promise.all([r.e(5009),r.e(8161),r.e(2955),r.e(8200),r.e(879),r.e(1041),r.e(8374),r.e(4444),r.e(1458),r.e(2296),r.e(486),r.e(6863),r.e(3648),r.e(4930),r.e(1480),r.e(1092),r.e(6509),r.e(4821),r.e(7164),r.e(4940),r.e(1206),r.e(8331),r.e(8101),r.e(7791)]).then(r.bind(r,49877))},o=function(e,t,r){(0,n.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:i,dialogParams:Object.assign({},t,{flowConfig:r})})}},78793:function(e,t,r){"use strict";r.r(t);var n=r(15652),i=r(57066),o=r(81582),a=r(57292),c=r(74186),s=r(18199),l=(r(78731),r(14516)),u=r(83849),d=(r(57793),r(5986)),f=(r(96551),r(29311)),p=r(2852),h=r(55317);r(59947);function m(e){return(m="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function v(){var e=g(["\n      <hass-tabs-subpage-data-table\n        .hass=","\n        .narrow=","\n        .backPath=","\n        .tabs=","\n        .route=","\n        .columns=","\n        .data=","\n        .activeFilters=","\n        @row-click=","\n      >\n      </hass-tabs-subpage-data-table>\n      <mwc-fab\n        ?is-wide=",'\n        icon="hass:plus"\n        title="Dodaj urządzenie"\n        @click=','\n        class=""\n      >\n        <ha-svg-icon slot="icon" path=',"></ha-svg-icon>\n      </mwc-fab>\n    "]);return v=function(){return e},e}function y(){var e=g(["\n                  ",'\n                  <div class="secondary">\n                    '," | ","\n                  </div>\n                "]);return y=function(){return e},e}function b(e,t){var r;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(r=T(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var n=0,i=function(){};return{s:i,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(e){throw e},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,c=!1;return{s:function(){r=e[Symbol.iterator]()},n:function(){var e=r.next();return a=e.done,e},e:function(e){c=!0,o=e},f:function(){try{a||null==r.return||r.return()}finally{if(c)throw o}}}}function w(){var e=g(["\n      .content {\n        padding: 4px;\n      }\n      mwc-fab {\n        position: fixed;\n        bottom: 16px;\n        right: 16px;\n        z-index: 1;\n      }\n    "]);return w=function(){return e},e}function g(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function k(e,t){return(k=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function _(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=S(e);if(t){var i=S(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return E(this,r)}}function E(e,t){return!t||"object"!==m(t)&&"function"!=typeof t?P(e):t}function P(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function S(e){return(S=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function D(){D=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!A(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[o])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&n.push(s.finisher);var l=s.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||T(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=x(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:j(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=j(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function z(e){var t,r=x(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function O(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function A(e){return e.decorators&&e.decorators.length}function C(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function j(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function x(e){var t=function(e,t){if("object"!==m(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==m(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===m(t)?t:String(t)}function T(e,t){if(e){if("string"==typeof e)return F(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?F(e,t):void 0}}function F(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}!function(e,t,r,n){var i=D();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,c.elements)}),r),c=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(C(o.descriptor)||C(i.descriptor)){if(A(o)||A(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(A(o)){if(A(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}O(o,i)}else t.push(o)}return t}(a.d.map(z)),e);i.initializeClassElements(a.F,c.elements),i.runClassFinishers(a.F,c.finishers)}([(0,n.Mo)("ha-config-ais-dom-devices-dashboard")],(function(e,t){return{F:function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&k(e,t)}(n,t);var r=_(n);function n(){var t;return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,n),t=r.call(this),e(P(t)),window.addEventListener("location-changed",(function(){t._searchParms=new URLSearchParams(window.location.search)})),window.addEventListener("popstate",(function(){t._searchParms=new URLSearchParams(window.location.search)})),t}return n}(t),d:[{kind:"get",static:!0,key:"styles",value:function(){return(0,n.iv)(w())}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:function(){return!1}},{kind:"field",decorators:[(0,n.Cb)()],key:"isWide",value:function(){return!1}},{kind:"field",decorators:[(0,n.Cb)()],key:"devices",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"entries",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"entities",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"areas",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_searchParms",value:function(){return new URLSearchParams(window.location.search)}},{kind:"field",key:"_activeFilters",value:function(){var e=this;return(0,l.Z)((function(t,r,n){var i=[];return r.forEach((function(r,o){switch(o){case"config_entry":var a=t.find((function(e){return e.entry_id===r}));if(!a)break;var c=(0,d.Lh)(n,a.domain);i.push("".concat(e.hass.localize("ui.panel.config.integrations.integration")," ").concat(c).concat(c!==a.title?": ".concat(a.title):""))}})),i.length?i:void 0}))}},{kind:"field",key:"_devices",value:function(){var e=this;return(0,l.Z)((function(t,r,n,i,o,c){var s,l=t,u={},d=b(t);try{for(d.s();!(s=d.n()).done;){var f=s.value;u[f.id]=f}}catch(D){d.e(D)}finally{d.f()}var p,h={},m=b(n);try{for(m.s();!(p=m.n()).done;){var v=p.value;v.device_id&&(v.device_id in h||(h[v.device_id]=[]),h[v.device_id].push(v))}}catch(D){m.e(D)}finally{m.f()}var y,w={},g=b(r);try{for(g.s();!(y=g.n()).done;){var k=y.value;w[k.entry_id]=k}}catch(D){g.e(D)}finally{g.f()}var _,E={},P=b(i);try{for(P.s();!(_=P.n()).done;){var S=_.value;E[S.area_id]=S}}catch(D){P.e(D)}finally{P.f()}return o.forEach((function(e,t){switch(t){case"config_entry":l=l.filter((function(t){return t.config_entries.includes(e)}))}})),l=l.map((function(t){return Object.assign({},t,{name:(0,a.jL)(t,e.hass,h[t.id]),model:t.model||"<unknown>",manufacturer:t.manufacturer||"<unknown>",area:t.area_id?E[t.area_id].name:e.hass.localize("ui.panel.config.devices.data_table.no_area"),integration:t.config_entries.length?t.config_entries.filter((function(e){return e in w})).map((function(e){return c("component.".concat(w[e].domain,".title"))||w[e].domain})).join(", "):"No integration",sw_version:t.sw_version})}))}))}},{kind:"field",key:"_columns",value:function(){var e=this;return(0,l.Z)((function(t){var r=t?{name:{title:"Device",sortable:!0,filterable:!0,direction:"asc",grows:!0,template:function(e,t){return(0,n.dy)(y(),e,t.area,t.integration)}}}:{name:{title:e.hass.localize("ui.panel.config.devices.data_table.device"),sortable:!0,filterable:!0,grows:!0,direction:"asc"}};return r.manufacturer={title:e.hass.localize("ui.panel.config.devices.data_table.manufacturer"),sortable:!0,hidden:t,filterable:!0,width:"15%"},r.model={title:e.hass.localize("ui.panel.config.devices.data_table.model"),sortable:!0,hidden:t,filterable:!0,width:"15%"},r.area={title:e.hass.localize("ui.panel.config.devices.data_table.area"),sortable:!0,hidden:t,filterable:!0,width:"15%"},r.integration={title:e.hass.localize("ui.panel.config.devices.data_table.integration"),sortable:!0,hidden:t,filterable:!0,width:"15%"},r.sw_version={title:"Wersja",sortable:!0,width:t?"90px":"15%",maxWidth:"90px"},r}))}},{kind:"method",key:"render",value:function(){return(0,n.dy)(v(),this.hass,this.narrow,this._searchParms.has("historyBack")?void 0:"/config",f.configSections.integrations,this.route,this._columns(this.narrow),this._devices(this.devices,this.entries,this.entities,this.areas,this._searchParms,this.hass.localize),this._activeFilters(this.entries,this._searchParms,this.hass.localize),this._handleRowClicked,!0,this._addDevice,h.qX5)}},{kind:"method",key:"_batteryEntity",value:function(e,t){var r=(0,c.eD)(this.hass,t[e]||[]);return r?r.entity_id:void 0}},{kind:"method",key:"_batteryChargingEntity",value:function(e,t){var r=(0,c.Mw)(this.hass,t[e]||[]);return r?r.entity_id:void 0}},{kind:"method",key:"_handleRowClicked",value:function(e){var t=e.detail.id;(0,u.c)(this,"/config/devices/device/".concat(t))}},{kind:"method",key:"_continueFlow",value:function(e){(0,p.t)(this,{continueFlowId:e,dialogClosedCallback:function(){console.log("OK")}})}},{kind:"method",key:"_addDevice",value:function(){var e=this;this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_dom_device"}).then((function(t){console.log(t),e._continueFlow(t.flow_id)}))}}]}}),n.oi);function R(e){return(R="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function I(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function L(e,t){return(L=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function W(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=V(e);if(t){var i=V(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return M(this,r)}}function M(e,t){return!t||"object"!==R(t)&&"function"!=typeof t?U(e):t}function U(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function B(){B=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!q(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[o])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&n.push(s.finisher);var l=s.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return X(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?X(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=N(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:K(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=K(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function H(e){var t,r=N(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function Z(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function q(e){return e.decorators&&e.decorators.length}function G(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function K(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function N(e){var t=function(e,t){if("object"!==R(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==R(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===R(t)?t:String(t)}function X(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function $(e,t,r){return($="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=V(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}})(e,t,r||e)}function V(e){return(V=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,n){var i=B();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,c.elements)}),r),c=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(G(o.descriptor)||G(i.descriptor)){if(q(o)||q(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(q(o)){if(q(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}Z(o,i)}else t.push(o)}return t}(a.d.map(H)),e);i.initializeClassElements(a.F,c.elements),i.runClassFinishers(a.F,c.finishers)}([(0,n.Mo)("ha-config-ais-dom-devices")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&L(e,t)}(n,t);var r=W(n);function n(){var t;I(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(U(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"showAdvanced",value:void 0},{kind:"field",key:"routerOptions",value:function(){return{defaultPage:"dashboard",routes:{dashboard:{tag:"ha-config-ais-dom-devices-dashboard",cache:!0},device:{tag:"ha-config-device-page"}}}}},{kind:"field",decorators:[(0,n.sz)()],key:"_configEntries",value:function(){return[]}},{kind:"field",decorators:[(0,n.sz)()],key:"_entityRegistryEntries",value:function(){return[]}},{kind:"field",decorators:[(0,n.sz)()],key:"_deviceRegistryEntries",value:function(){return[]}},{kind:"field",decorators:[(0,n.sz)()],key:"_areas",value:function(){return[]}},{kind:"field",key:"_unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){$(V(r.prototype),"connectedCallback",this).call(this),this.hass&&this._loadData()}},{kind:"method",key:"disconnectedCallback",value:function(){if($(V(r.prototype),"disconnectedCallback",this).call(this),this._unsubs){for(;this._unsubs.length;)this._unsubs.pop()();this._unsubs=void 0}}},{kind:"method",key:"firstUpdated",value:function(e){var t=this;$(V(r.prototype),"firstUpdated",this).call(this,e),this.addEventListener("hass-reload-entries",(function(){t._loadData()}))}},{kind:"method",key:"updated",value:function(e){$(V(r.prototype),"updated",this).call(this,e),!this._unsubs&&e.has("hass")&&this._loadData()}},{kind:"method",key:"updatePageEl",value:function(e){e.hass=this.hass,"device"===this._currentPage&&(e.deviceId=this.routeTail.path.substr(1)),e.entities=this._entityRegistryEntries,e.entries=this._configEntries,e.devices=this._deviceRegistryEntries,e.areas=this._areas,e.narrow=this.narrow,e.isWide=this.isWide,e.showAdvanced=this.showAdvanced,e.route=this.routeTail}},{kind:"method",key:"_loadData",value:function(){var e=this;(0,o.pB)(this.hass).then((function(t){e._configEntries=t})),this._unsubs||(this._unsubs=[(0,i.sG)(this.hass.connection,(function(t){e._areas=t})),(0,c.LM)(this.hass.connection,(function(t){e._entityRegistryEntries=t})),(0,a.q4)(this.hass.connection,(function(t){e._deviceRegistryEntries=t.filter((function(e){return"AI-Speaker"===e.manufacturer}))}))])}}]}}),s.n)}}]);
//# sourceMappingURL=chunk.e441d86329fe1d545edb.js.map