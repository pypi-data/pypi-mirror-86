(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[851],{7323:(e,t,i)=>{"use strict";i.d(t,{p:()=>r});const r=(e,t)=>e&&-1!==e.config.components.indexOf(t)},25516:(e,t,i)=>{"use strict";i.d(t,{i:()=>r});const r=e=>t=>({kind:"method",placement:"prototype",key:t.key,descriptor:{set(e){this["__"+String(t.key)]=e},get(){return this["__"+String(t.key)]},enumerable:!0,configurable:!0},finisher(i){const r=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){if(r.call(this),this[t.key]){const i=this.renderRoot.querySelector(e);if(!i)return;i.scrollTop=this[t.key]}}}})},8436:(e,t,i)=>{"use strict";i.r(t),i.d(t,{HuiLogbookCard:()=>w});var r=i(15652),o=i(81471),n=i(7323),s=i(43260),a=i(22311),l=i(8330),c=(i(22098),i(31206),i(55422)),d=(i(97740),i(64588)),h=i(90271);i(75502);function f(){f=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!m(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return k(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?k(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=v(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function u(e){var t,i=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function k(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function b(e,t,i){return(b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=_(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function _(e){return(_=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let w=function(e,t,i,r){var o=f();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(y(n.descriptor)||y(o.descriptor)){if(m(n)||m(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(m(n)){if(m(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}p(n,o)}else t.push(n)}return t}(s.d.map(u)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("hui-logbook-card")],(function(e,t){class f extends t{constructor(...t){super(...t),e(this)}}return{F:f,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([i.e(5009),i.e(8161),i.e(2955),i.e(1041),i.e(8374),i.e(3098),i.e(6087),i.e(1002),i.e(4535),i.e(6902),i.e(2725)]).then(i.bind(i,74237)),document.createElement("hui-logbook-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,i){return{entities:(0,d.j)(e,3,t,i,["light","switch"])}}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_logbookEntries",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_persons",value:()=>({})},{kind:"field",decorators:[(0,r.sz)()],key:"_configEntities",value:void 0},{kind:"field",key:"_lastLogbookDate",value:void 0},{kind:"field",key:"_throttleGetLogbookEntries",value(){return(0,l.P)((()=>{this._getLogBookData()}),1e4)}},{kind:"method",key:"getCardSize",value:function(){var e;return 9+((null===(e=this._config)||void 0===e?void 0:e.title)?1:0)}},{kind:"method",key:"setConfig",value:function(e){this._configEntities=(0,h.A)(e.entities),this._config={hours_to_show:24,...e}}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.has("_config")||e.has("_persons")||e.has("_logbookEntries"))return!0;const t=e.get("hass");if(!this._configEntities||!t||t.themes!==this.hass.themes||t.language!==this.hass.language)return!0;for(const i of this._configEntities)if(t.states[i.entity]!==this.hass.states[i.entity])return!0;return!1}},{kind:"method",key:"firstUpdated",value:function(){this._fetchPersonNames()}},{kind:"method",key:"updated",value:function(e){if(b(_(f.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const t=e.has("_config"),i=e.has("hass"),r=e.get("hass"),o=e.get("_config");if((i&&(null==r?void 0:r.themes)!==this.hass.themes||t&&(null==o?void 0:o.theme)!==this._config.theme)&&(0,s.R)(this,this.hass.themes,this._config.theme),!t||(null==o?void 0:o.entities)===this._config.entities&&(null==o?void 0:o.hours_to_show)===this._config.hours_to_show)r&&this._configEntities.some((e=>r.states[e.entity]!==this.hass.states[e.entity]))&&setTimeout(this._throttleGetLogbookEntries,1e3);else{if(this._logbookEntries=void 0,this._lastLogbookDate=void 0,!this._configEntities)return;this._throttleGetLogbookEntries()}}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?(0,n.p)(this.hass,"logbook")?r.dy`
      <ha-card
        .header=${this._config.title}
        class=${(0,o.$)({"no-header":!this._config.title})}
      >
        <div class="content">
          ${this._logbookEntries?this._logbookEntries.length?r.dy`
                <ha-logbook
                  narrow
                  relative-time
                  virtualize
                  .hass=${this.hass}
                  .entries=${this._logbookEntries}
                  .userIdToName=${this._persons}
                ></ha-logbook>
              `:r.dy`
                <div class="no-entries">
                  ${this.hass.localize("ui.components.logbook.entries_not_found")}
                </div>
              `:r.dy`
                <ha-circular-progress
                  active
                  alt=${this.hass.localize("ui.common.loading")}
                ></ha-circular-progress>
              `}
        </div>
      </ha-card>
    `:r.dy`
        <hui-warning>
          ${this.hass.localize("ui.components.logbook.component_not_loaded")}</hui-warning
        >
      `:r.dy``}},{kind:"method",key:"_getLogBookData",value:async function(){if(!this.hass||!this._config||!(0,n.p)(this.hass,"logbook"))return;const e=new Date((new Date).getTime()-60*this._config.hours_to_show*60*1e3),t=this._lastLogbookDate||e,i=new Date,r=await(0,c.rM)(this.hass,t.toISOString(),i.toISOString(),this._configEntities.map((e=>e.entity)).toString(),!0),o=this._logbookEntries?[...r,...this._logbookEntries]:r;this._logbookEntries=o.filter((t=>new Date(t.when)>e)),this._lastLogbookDate=i}},{kind:"method",key:"_fetchPersonNames",value:function(){this.hass&&Object.values(this.hass.states).forEach((e=>{e.attributes.user_id&&"person"===(0,a.N)(e)&&(this._persons[e.attributes.user_id]=e.attributes.friendly_name)}))}},{kind:"get",static:!0,key:"styles",value:function(){return[r.iv`
        ha-card {
          height: 100%;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }

        .content {
          padding: 0 16px 16px;
        }

        .no-header .content {
          padding-top: 16px;
        }

        .no-entries {
          text-align: center;
          padding: 16px;
          color: var(--secondary-text-color);
        }

        ha-logbook {
          height: 385px;
          overflow: auto;
          display: block;
        }

        ha-circular-progress {
          display: flex;
          justify-content: center;
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=chunk.e1687516d2c6be4bc427.js.map