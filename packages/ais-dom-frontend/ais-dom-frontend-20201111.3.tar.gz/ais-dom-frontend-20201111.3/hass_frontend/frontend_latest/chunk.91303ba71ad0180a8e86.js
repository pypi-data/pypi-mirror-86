(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2390],{92390:(t,e,i)=>{"use strict";i(31206);var a=i(50856),s=i(28426),n=i(1265),r=i(78956),o=i(44583),l=i(72986),h=i(33367),d=i(21683),c=i(49684);i(10983);let p=null;class u extends((0,h.P)([l.z],s.H3)){static get template(){return a.d`
      <style>
        :host {
          display: block;
        }
        .chartHeader {
          padding: 6px 0 0 0;
          width: 100%;
          display: flex;
          flex-direction: row;
        }
        .chartHeader > div {
          vertical-align: top;
          padding: 0 8px;
        }
        .chartHeader > div.chartTitle {
          padding-top: 8px;
          flex: 0 0 0;
          max-width: 30%;
        }
        .chartHeader > div.chartLegend {
          flex: 1 1;
          min-width: 70%;
        }
        :root {
          user-select: none;
          -moz-user-select: none;
          -webkit-user-select: none;
          -ms-user-select: none;
        }
        .chartTooltip {
          font-size: 90%;
          opacity: 1;
          position: absolute;
          background: rgba(80, 80, 80, 0.9);
          color: white;
          border-radius: 3px;
          pointer-events: none;
          transform: translate(-50%, 12px);
          z-index: 1000;
          width: 200px;
          transition: opacity 0.15s ease-in-out;
        }
        :host([rtl]) .chartTooltip {
          direction: rtl;
        }
        .chartLegend ul,
        .chartTooltip ul {
          display: inline-block;
          padding: 0 0px;
          margin: 5px 0 0 0;
          width: 100%;
        }
        .chartTooltip ul {
          margin: 0 3px;
        }
        .chartTooltip li {
          display: block;
          white-space: pre-line;
        }
        .chartTooltip li::first-line {
          line-height: 0;
        }
        .chartTooltip .title {
          text-align: center;
          font-weight: 500;
        }
        .chartTooltip .beforeBody {
          text-align: center;
          font-weight: 300;
          word-break: break-all;
        }
        .chartLegend li {
          display: inline-block;
          padding: 0 6px;
          max-width: 49%;
          text-overflow: ellipsis;
          white-space: nowrap;
          overflow: hidden;
          box-sizing: border-box;
        }
        .chartLegend li:nth-child(odd):last-of-type {
          /* Make last item take full width if it is odd-numbered. */
          max-width: 100%;
        }
        .chartLegend li[data-hidden] {
          text-decoration: line-through;
        }
        .chartLegend em,
        .chartTooltip em {
          border-radius: 5px;
          display: inline-block;
          height: 10px;
          margin-right: 4px;
          width: 10px;
        }
        :host([rtl]) .chartTooltip em {
          margin-right: inherit;
          margin-left: 4px;
        }
        ha-icon-button {
          color: var(--secondary-text-color);
        }
      </style>
      <template is="dom-if" if="[[unit]]">
        <div class="chartHeader">
          <div class="chartTitle">[[unit]]</div>
          <div class="chartLegend">
            <ul>
              <template is="dom-repeat" items="[[metas]]">
                <li on-click="_legendClick" data-hidden$="[[item.hidden]]">
                  <em style$="background-color:[[item.bgColor]]"></em>
                  [[item.label]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
      <div id="chartTarget" style="height:40px; width:100%">
        <canvas id="chartCanvas"></canvas>
        <div
          class$="chartTooltip [[tooltip.yAlign]]"
          style$="opacity:[[tooltip.opacity]]; top:[[tooltip.top]]; left:[[tooltip.left]]; padding:[[tooltip.yPadding]]px [[tooltip.xPadding]]px"
        >
          <div class="title">[[tooltip.title]]</div>
          <template is="dom-if" if="[[tooltip.beforeBody]]">
            <div class="beforeBody">[[tooltip.beforeBody]]</div>
          </template>
          <div>
            <ul>
              <template is="dom-repeat" items="[[tooltip.lines]]">
                <li>
                  <em style$="background-color:[[item.bgColor]]"></em
                  >[[item.text]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    `}get chart(){return this._chart}static get properties(){return{data:Object,identifier:String,rendered:{type:Boolean,notify:!0,value:!1,readOnly:!0},metas:{type:Array,value:()=>[]},tooltip:{type:Object,value:()=>({opacity:"0",left:"0",top:"0",xPadding:"5",yPadding:"3"})},unit:Object,rtl:{type:Boolean,reflectToAttribute:!0}}}static get observers(){return["onPropsChange(data)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.onPropsChange(),this._resizeListener=()=>{this._debouncer=r.d.debounce(this._debouncer,d.Wc.after(10),(()=>{this._isAttached&&this.resizeChart()}))},"function"==typeof ResizeObserver?(this.resizeObserver=new ResizeObserver((t=>{t.forEach((()=>{this._resizeListener()}))})),this.resizeObserver.observe(this.$.chartTarget)):this.addEventListener("iron-resize",this._resizeListener),null===p&&(p=Promise.all([i.e(9680),i.e(7770)]).then(i.bind(i,79109))),p.then((t=>{this.ChartClass=t.default,this.onPropsChange()}))}disconnectedCallback(){super.disconnectedCallback(),this._isAttached=!1,this.resizeObserver&&this.resizeObserver.unobserve(this.$.chartTarget),this.removeEventListener("iron-resize",this._resizeListener),void 0!==this._resizeTimer&&(clearInterval(this._resizeTimer),this._resizeTimer=void 0)}onPropsChange(){this._isAttached&&this.ChartClass&&this.data&&this.drawChart()}_customTooltips(t){if(0===t.opacity)return void this.set(["tooltip","opacity"],0);t.yAlign?this.set(["tooltip","yAlign"],t.yAlign):this.set(["tooltip","yAlign"],"no-transform");const e=t.title&&t.title[0]||"";this.set(["tooltip","title"],e),t.beforeBody&&this.set(["tooltip","beforeBody"],t.beforeBody.join("\n"));const i=t.body.map((t=>t.lines));t.body&&this.set(["tooltip","lines"],i.map(((e,i)=>{const a=t.labelColors[i];return{color:a.borderColor,bgColor:a.backgroundColor,text:e.join("\n")}})));const a=this.$.chartTarget.clientWidth;let s=t.caretX;const n=this._chart.canvas.offsetTop+t.caretY;t.caretX+100>a?s=a-100:t.caretX<100&&(s=100),s+=this._chart.canvas.offsetLeft,this.tooltip={...this.tooltip,opacity:1,left:s+"px",top:n+"px"}}_legendClick(t){(t=t||window.event).stopPropagation();let e=t.target||t.srcElement;for(;"LI"!==e.nodeName;)e=e.parentElement;const i=t.model.itemsIndex,a=this._chart.getDatasetMeta(i);a.hidden=null===a.hidden?!this._chart.data.datasets[i].hidden:null,this.set(["metas",i,"hidden"],this._chart.isDatasetVisible(i)?null:"hidden"),this._chart.update()}_drawLegend(){const t=this._chart,e=this._oldIdentifier&&this.identifier===this._oldIdentifier;this._oldIdentifier=this.identifier,this.set("metas",this._chart.data.datasets.map(((i,a)=>({label:i.label,color:i.color,bgColor:i.backgroundColor,hidden:e&&a<this.metas.length?this.metas[a].hidden:!t.isDatasetVisible(a)}))));let i=!1;if(e)for(let a=0;a<this.metas.length;a++){const e=t.getDatasetMeta(a);!!e.hidden!=!!this.metas[a].hidden&&(i=!0),e.hidden=!!this.metas[a].hidden||null}i&&t.update(),this.unit=this.data.unit}_formatTickValue(t,e,i){if(0===i.length)return t;const a=new Date(i[e].value);return(0,c.m)(a,this.hass.language)}drawChart(){const t=this.data.data,e=this.$.chartCanvas;if(t.datasets&&t.datasets.length||this._chart){if("timeline"!==this.data.type&&t.datasets.length>0){const e=t.datasets.length,i=this.constructor.getColorList(e);for(let a=0;a<e;a++)t.datasets[a].borderColor=i[a].rgbString(),t.datasets[a].backgroundColor=i[a].alpha(.6).rgbaString()}if(this._chart)this._customTooltips({opacity:0}),this._chart.data=t,this._chart.update({duration:0}),this.isTimeline?this._chart.options.scales.yAxes[0].gridLines.display=t.length>1:!0===this.data.legend&&this._drawLegend(),this.resizeChart();else{if(!t.datasets)return;this._customTooltips({opacity:0});const i=[{afterRender:()=>this._setRendered(!0)}];let a={responsive:!0,maintainAspectRatio:!1,animation:{duration:0},hover:{animationDuration:0},responsiveAnimationDuration:0,tooltips:{enabled:!1,custom:this._customTooltips.bind(this)},legend:{display:!1},line:{spanGaps:!0},elements:{font:"12px 'Roboto', 'sans-serif'"},ticks:{fontFamily:"'Roboto', 'sans-serif'"}};a=Chart.helpers.merge(a,this.data.options),a.scales.xAxes[0].ticks.callback=this._formatTickValue.bind(this),"timeline"===this.data.type?(this.set("isTimeline",!0),void 0!==this.data.colors&&(this._colorFunc=this.constructor.getColorGenerator(this.data.colors.staticColors,this.data.colors.staticColorIndex)),void 0!==this._colorFunc&&(a.elements.colorFunction=this._colorFunc),1===t.datasets.length&&(a.scales.yAxes[0].ticks?a.scales.yAxes[0].ticks.display=!1:a.scales.yAxes[0].ticks={display:!1},a.scales.yAxes[0].gridLines?a.scales.yAxes[0].gridLines.display=!1:a.scales.yAxes[0].gridLines={display:!1}),this.$.chartTarget.style.height="50px"):this.$.chartTarget.style.height="160px";const s={type:this.data.type,data:this.data.data,options:a,plugins:i};this._chart=new this.ChartClass(e,s),!0!==this.isTimeline&&!0===this.data.legend&&this._drawLegend(),this.resizeChart()}}}resizeChart(){this._chart&&(void 0!==this._resizeTimer?(clearInterval(this._resizeTimer),this._resizeTimer=void 0,this._resizeChart()):this._resizeTimer=setInterval(this.resizeChart.bind(this),10))}_resizeChart(){const t=this.$.chartTarget,e=this.data.data;if(0===e.datasets.length)return;if(!this.isTimeline)return void this._chart.resize();const i=this._chart.chartArea.top,a=this._chart.chartArea.bottom,s=this._chart.canvas.clientHeight;if(a>0&&(this._axisHeight=s-a+i),!this._axisHeight)return t.style.height="50px",this._chart.resize(),void this.resizeChart();if(this._axisHeight){const i=30*e.datasets.length+this._axisHeight+"px";t.style.height!==i&&(t.style.height=i),this._chart.resize()}}static getColorList(t){let e=!1;t>10&&(e=!0,t=Math.ceil(t/2));const i=360/t,a=[];for(let s=0;s<t;s++)a[s]=Color().hsl(i*s,80,38),e&&(a[s+t]=Color().hsl(i*s,80,62));return a}static getColorGenerator(t,e){const i=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"];function a(t){return Color("#"+i[t%i.length])}const s={};let n=0;return e>0&&(n=e),t&&Object.keys(t).forEach((e=>{const i=t[e];isFinite(i)?s[e.toLowerCase()]=a(i):s[e.toLowerCase()]=Color(t[e])})),function(t,e){let i;const r=e[3];if(null===r)return Color().hsl(0,40,38);if(void 0===r)return Color().hsl(120,40,38);const o=r.toLowerCase();return void 0===i&&(i=s[o]),void 0===i&&(i=a(n),n++,s[o]=i),i}}}customElements.define("ha-chart-base",u);class m extends((0,n.Z)(s.H3)){static get template(){return a.d`
      <style>
        :host {
          display: block;
          overflow: hidden;
          height: 0;
          transition: height 0.3s ease-in-out;
        }
      </style>
      <ha-chart-base
        id="chart"
        hass="[[hass]]"
        data="[[chartData]]"
        identifier="[[identifier]]"
        rendered="{{rendered}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:Object,names:Object,unit:String,identifier:String,isSingleDevice:{type:Boolean,value:!1},endTime:Object,rendered:{type:Boolean,value:!1,observer:"_onRenderedChanged"}}}static get observers(){return["dataChanged(data, endTime, isSingleDevice)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}ready(){super.ready(),this.addEventListener("transitionend",(()=>{this.style.overflow="auto"}))}dataChanged(){this.drawChart()}_onRenderedChanged(t){t&&this.animateHeight()}animateHeight(){requestAnimationFrame((()=>requestAnimationFrame((()=>{this.style.height=this.$.chart.scrollHeight+"px"}))))}drawChart(){if(!this._isAttached)return;const t=this.unit,e=this.data,i=[];let a;if(0===e.length)return;function s(t){const e=parseFloat(t);return isFinite(e)?e:null}a=this.endTime||new Date(Math.max.apply(null,e.map((t=>new Date(t.states[t.states.length-1].last_changed))))),a>new Date&&(a=new Date);const n=this.names||{};e.forEach((e=>{const r=e.domain,o=n[e.entity_id]||e.name;let l;const h=[];function d(t,e){e&&(t>a||(h.forEach(((i,a)=>{i.data.push({x:t,y:e[a]})})),l=e))}function c(e,i,a){let s=!1,n=!1;a&&(s="origin"),i&&(n="before"),h.push({label:e,fill:s,steppedLine:n,pointRadius:0,data:[],unitText:t})}if("thermostat"===r||"climate"===r||"water_heater"===r){const t=e.states.some((t=>t.attributes&&t.attributes.hvac_action)),i="climate"===r&&t?t=>"heating"===t.attributes.hvac_action:t=>"heat"===t.state,a="climate"===r&&t?t=>"cooling"===t.attributes.hvac_action:t=>"cool"===t.state,n=e.states.some(i),l=e.states.some(a),h=e.states.some((t=>t.attributes&&t.attributes.target_temp_high!==t.attributes.target_temp_low));c(""+this.hass.localize("ui.card.climate.current_temperature","name",o),!0),n&&c(""+this.hass.localize("ui.card.climate.heating","name",o),!0,!0),l&&c(""+this.hass.localize("ui.card.climate.cooling","name",o),!0,!0),h?(c(""+this.hass.localize("ui.card.climate.target_temperature_mode","name",o,"mode",this.hass.localize("ui.card.climate.high")),!0),c(""+this.hass.localize("ui.card.climate.target_temperature_mode","name",o,"mode",this.hass.localize("ui.card.climate.low")),!0)):c(""+this.hass.localize("ui.card.climate.target_temperature_entity","name",o),!0),e.states.forEach((t=>{if(!t.attributes)return;const e=s(t.attributes.current_temperature),r=[e];if(n&&r.push(i(t)?e:null),l&&r.push(a(t)?e:null),h){const e=s(t.attributes.target_temp_high),i=s(t.attributes.target_temp_low);r.push(e,i),d(new Date(t.last_changed),r)}else{const e=s(t.attributes.temperature);r.push(e),d(new Date(t.last_changed),r)}}))}else if("humidifier"===r)c(""+this.hass.localize("ui.card.humidifier.target_humidity_entity","name",o),!0),c(""+this.hass.localize("ui.card.humidifier.on_entity","name",o),!0,!0),e.states.forEach((t=>{if(!t.attributes)return;const e=s(t.attributes.humidity),i=[e];i.push("on"===t.state?e:null),d(new Date(t.last_changed),i)}));else{c(o,"sensor"===r);let t=null,i=null,a=null;e.states.forEach((e=>{const n=s(e.state),r=new Date(e.last_changed);if(null!==n&&null!==a){const e=r.getTime(),s=a.getTime(),o=i.getTime();d(a,[(s-o)/(e-o)*(n-t)+t]),d(new Date(s+1),[null]),d(r,[n]),i=r,t=n,a=null}else null!==n&&null===a?(d(r,[n]),i=r,t=n):null===n&&null===a&&null!==t&&(a=r)}))}d(a,l),Array.prototype.push.apply(i,h)}));const r={type:"line",unit:t,legend:!this.isSingleDevice,options:{scales:{xAxes:[{type:"time",ticks:{major:{fontStyle:"bold"}}}],yAxes:[{ticks:{maxTicksLimit:7}}]},tooltips:{mode:"neareach",callbacks:{title:(t,e)=>{const i=t[0],a=e.datasets[i.datasetIndex].data[i.index].x;return(0,o.E)(a,this.hass.language)}}},hover:{mode:"neareach"},layout:{padding:{top:5}},elements:{line:{tension:.1,pointRadius:0,borderWidth:1.5},point:{hitRadius:5}},plugins:{filler:{propagate:!0}}},data:{labels:[],datasets:i}};this.chartData=r}}customElements.define("state-history-chart-line",m);var g=i(87744);class f extends((0,n.Z)(s.H3)){static get template(){return a.d`
      <style>
        :host {
          display: block;
          opacity: 0;
          transition: opacity 0.3s ease-in-out;
        }
        :host([rendered]) {
          opacity: 1;
        }

        ha-chart-base {
          direction: ltr;
        }
      </style>
      <ha-chart-base
        hass="[[hass]]"
        data="[[chartData]]"
        rendered="{{rendered}}"
        rtl="{{rtl}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:{type:Object,observer:"dataChanged"},names:Object,noSingle:Boolean,endTime:Date,rendered:{type:Boolean,value:!1,reflectToAttribute:!0},rtl:{reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}static get observers(){return["dataChanged(data, endTime, localize, language)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}drawChart(){let t=this.data;if(!this._isAttached)return;t||(t=[]);const e=new Date(t.reduce(((t,e)=>Math.min(t,new Date(e.data[0].last_changed))),new Date));let i=this.endTime||new Date(t.reduce(((t,e)=>Math.max(t,new Date(e.data[e.data.length-1].last_changed))),e));i>new Date&&(i=new Date);const a=[],s=[],n=this.names||{};t.forEach((t=>{let r,o=null,l=null,h=e;const d=n[t.entity_id]||t.name,c=[];t.data.forEach((t=>{let e=t.state;void 0!==e&&""!==e||(e=null),new Date(t.last_changed)>i||(null!==o&&e!==o?(r=new Date(t.last_changed),c.push([h,r,l,o]),o=e,l=t.state_localize,h=r):null===o&&(o=e,l=t.state_localize,h=new Date(t.last_changed)))})),null!==o&&c.push([h,i,l,o]),s.push({data:c,entity_id:t.entity_id}),a.push(d)}));const r={type:"timeline",options:{tooltips:{callbacks:{label:(t,e)=>{const i=e.datasets[t.datasetIndex].data[t.index],a=(0,o.E)(i[0],this.hass.language),s=(0,o.E)(i[1],this.hass.language);return[i[2],a,s]},beforeBody:(t,e)=>{if(!this.hass.userData||!this.hass.userData.showAdvanced||!t[0])return"";return e.datasets[t[0].datasetIndex].entity_id||""}}},scales:{xAxes:[{ticks:{major:{fontStyle:"bold"}}}],yAxes:[{afterSetDimensions:t=>{t.maxWidth=.18*t.chart.width},position:this._computeRTL?"right":"left"}]}},data:{labels:a,datasets:s},colors:{staticColors:{on:1,off:0,home:1,not_home:0,unavailable:"#a0a0a0",unknown:"#606060",idle:2},staticColorIndex:3}};this.chartData=r}_computeRTL(t){return(0,g.HE)(t)}}customElements.define("state-history-chart-timeline",f);class b extends((0,n.Z)(s.H3)){static get template(){return a.d`
      <style>
        :host {
          display: block;
          /* height of single timeline chart = 58px */
          min-height: 58px;
        }
        .info {
          text-align: center;
          line-height: 58px;
          color: var(--secondary-text-color);
        }
      </style>
      <template
        is="dom-if"
        class="info"
        if="[[_computeIsLoading(isLoadingData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.loading_history')]]
        </div>
      </template>

      <template
        is="dom-if"
        class="info"
        if="[[_computeIsEmpty(isLoadingData, historyData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.no_history_found')]]
        </div>
      </template>

      <template is="dom-if" if="[[historyData.timeline.length]]">
        <state-history-chart-timeline
          hass="[[hass]]"
          data="[[historyData.timeline]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          no-single="[[noSingle]]"
          names="[[names]]"
        ></state-history-chart-timeline>
      </template>

      <template is="dom-repeat" items="[[historyData.line]]">
        <state-history-chart-line
          hass="[[hass]]"
          unit="[[item.unit]]"
          data="[[item.data]]"
          identifier="[[item.identifier]]"
          is-single-device="[[_computeIsSingleLineChart(item.data, noSingle)]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          names="[[names]]"
        ></state-history-chart-line>
      </template>
    `}static get properties(){return{hass:Object,historyData:{type:Object,value:null},names:Object,isLoadingData:Boolean,endTime:{type:Object},upToNow:Boolean,noSingle:Boolean}}_computeIsSingleLineChart(t,e){return!e&&t&&1===t.length}_computeIsEmpty(t,e){const i=!e||!e.timeline||!e.line||0===e.timeline.length&&0===e.line.length;return!t&&i}_computeIsLoading(t){return t&&!this.historyData}_computeEndTime(t,e){return e?new Date:t}}customElements.define("state-history-charts",b)}}]);
//# sourceMappingURL=chunk.91303ba71ad0180a8e86.js.map