(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[664],{30664:(e,t,i)=>{"use strict";var r=i(55317),n=(i(30879),i(53973),i(68374),i(15652)),o=i(47181),a=(i(52039),i(3143),i(49599));i(25230);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!d(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=h(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function l(e){var t,i=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}const m=(e,t,i)=>{e.firstElementChild||(e.innerHTML="\n      <style>\n        paper-item {\n          margin: -10px;\n          padding: 0;\n        }\n      </style>\n      <paper-item></paper-item>\n    "),e.querySelector("paper-item").textContent=(0,a.b)(i.item)};!function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,p.elements)}),i),p=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(u(o.descriptor)||u(n.descriptor)){if(d(o)||d(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(d(o)){if(d(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(a.d.map(l)),e);n.initializeClassElements(a.F,p.elements),n.runClassFinishers(a.F,p.finishers)}([(0,n.Mo)("ha-entity-attribute-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"entityId",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"allow-custom-value"})],key:"allowCustomValue",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"_opened",value:()=>!1},{kind:"field",decorators:[(0,n.IO)("vaadin-combo-box-light",!0)],key:"_comboBox",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return!(!e.has("_opened")&&this._opened)}},{kind:"method",key:"updated",value:function(e){if(e.has("_opened")&&this._opened){const e=this.entityId?this.hass.states[this.entityId]:void 0;this._comboBox.items=e?Object.keys(e.attributes):[]}}},{kind:"method",key:"render",value:function(){var e;return this.hass?n.dy`
      <vaadin-combo-box-light
        .value=${this._value}
        .allowCustomValue=${this.allowCustomValue}
        .renderer=${m}
        attr-for-value="bind-value"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
        <paper-input
          .autofocus=${this.autofocus}
          .label=${null!==(e=this.label)&&void 0!==e?e:this.hass.localize("ui.components.entity.entity-attribute-picker.attribute")}
          .value=${this._value?(0,a.b)(this._value):""}
          .disabled=${this.disabled||!this.entityId}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          spellcheck="false"
        >
          <div class="suffix" slot="suffix">
            ${this.value?n.dy`
                  <mwc-icon-button
                    .label=${this.hass.localize("ui.components.entity.entity-picker.clear")}
                    class="clear-button"
                    tabindex="-1"
                    @click=${this._clearValue}
                    no-ripple
                  >
                    <ha-svg-icon .path=${r.r5M}></ha-svg-icon>
                  </mwc-icon-button>
                `:""}

            <mwc-icon-button
              .label=${this.hass.localize("ui.components.entity.entity-attribute-picker.show_attributes")}
              class="toggle-button"
              tabindex="-1"
            >
              <ha-svg-icon
                .path=${this._opened?r.MzE:r.iW9}
              ></ha-svg-icon>
            </mwc-icon-button>
          </div>
        </paper-input>
      </vaadin-combo-box-light>
    `:n.dy``}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),this._setValue("")}},{kind:"get",key:"_value",value:function(){return this.value}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.detail.value;t!==this._value&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,o.B)(this,"value-changed",{value:e}),(0,o.B)(this,"change")}),0)}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      .suffix {
        display: flex;
      }
      mwc-icon-button {
        --mdc-icon-button-size: 24px;
        padding: 0px 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}]}}),n.oi)},49599:(e,t,i)=>{"use strict";i.d(t,{Z:()=>n,b:()=>o});const r={DOMAIN_DEVICE_CLASS:{binary_sensor:["battery","cold","connectivity","door","garage_door","gas","heat","light","lock","moisture","motion","moving","occupancy","opening","plug","power","presence","problem","safety","smoke","sound","vibration","window"],cover:["awning","blind","curtain","damper","door","garage","shade","shutter","window"],humidifier:["dehumidifier","humidifier"],sensor:["battery","humidity","illuminance","temperature","pressure","power","signal_strength","timestamp"],switch:["switch","outlet"]},UNKNOWN_TYPE:"json",ADD_TYPE:"key-value",TYPE_TO_TAG:{string:"ha-customize-string",json:"ha-customize-string",icon:"ha-customize-icon",boolean:"ha-customize-boolean",array:"ha-customize-array","key-value":"ha-customize-key-value"},LOGIC_STATE_ATTRIBUTES:{}};r.LOGIC_STATE_ATTRIBUTES={entity_picture:void 0,friendly_name:{type:"string",description:"Name"},icon:{type:"icon"},emulated_hue:{type:"boolean",domains:["emulated_hue"]},emulated_hue_name:{type:"string",domains:["emulated_hue"]},haaska_hidden:void 0,haaska_name:void 0,supported_features:void 0,attribution:void 0,restored:void 0,custom_ui_more_info:{type:"string"},custom_ui_state_card:{type:"string"},device_class:{type:"array",options:r.DOMAIN_DEVICE_CLASS,description:"Device class",domains:["binary_sensor","cover","humidifier","sensor","switch"]},assumed_state:{type:"boolean",domains:["switch","light","cover","climate","fan","humidifier","group","water_heater"]},initial_state:{type:"string",domains:["automation"]},unit_of_measurement:{type:"string"}};const n=r;function o(e){return(e=e.replace(/_/g," ").replace(/\bid\b/g,"ID")).charAt(0).toUpperCase()+e.slice(1)}}}]);
//# sourceMappingURL=chunk.6df6afb98603abed1443.js.map