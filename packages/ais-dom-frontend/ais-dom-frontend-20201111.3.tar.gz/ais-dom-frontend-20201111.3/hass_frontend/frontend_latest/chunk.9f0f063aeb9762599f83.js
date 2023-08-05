/*! For license information please see chunk.9f0f063aeb9762599f83.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9290],{29290:(t,e,i)=>{"use strict";var n,o,s=i(87480),r=i(15652),a=(i(54567),{ANCHOR:"mdc-menu-surface--anchor",ANIMATING_CLOSED:"mdc-menu-surface--animating-closed",ANIMATING_OPEN:"mdc-menu-surface--animating-open",FIXED:"mdc-menu-surface--fixed",IS_OPEN_BELOW:"mdc-menu-surface--is-open-below",OPEN:"mdc-menu-surface--open",ROOT:"mdc-menu-surface"}),c={CLOSED_EVENT:"MDCMenuSurface:closed",OPENED_EVENT:"MDCMenuSurface:opened",FOCUSABLE_ELEMENTS:["button:not(:disabled)",'[href]:not([aria-disabled="true"])',"input:not(:disabled)","select:not(:disabled)","textarea:not(:disabled)",'[tabindex]:not([tabindex="-1"]):not([aria-disabled="true"])'].join(", ")},d={TRANSITION_OPEN_DURATION:120,TRANSITION_CLOSE_DURATION:75,MARGIN_TO_EDGE:32,ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO:.67};!function(t){t[t.BOTTOM=1]="BOTTOM",t[t.CENTER=2]="CENTER",t[t.RIGHT=4]="RIGHT",t[t.FLIP_RTL=8]="FLIP_RTL"}(n||(n={})),function(t){t[t.TOP_LEFT=0]="TOP_LEFT",t[t.TOP_RIGHT=4]="TOP_RIGHT",t[t.BOTTOM_LEFT=1]="BOTTOM_LEFT",t[t.BOTTOM_RIGHT=5]="BOTTOM_RIGHT",t[t.TOP_START=8]="TOP_START",t[t.TOP_END=12]="TOP_END",t[t.BOTTOM_START=9]="BOTTOM_START",t[t.BOTTOM_END=13]="BOTTOM_END"}(o||(o={}));var h=i(72774),u=function(t){function e(i){var n=t.call(this,(0,s.pi)((0,s.pi)({},e.defaultAdapter),i))||this;return n.isSurfaceOpen=!1,n.isQuickOpen=!1,n.isHoistedElement=!1,n.isFixedPosition=!1,n.openAnimationEndTimerId=0,n.closeAnimationEndTimerId=0,n.animationRequestId=0,n.anchorCorner=o.TOP_START,n.originCorner=o.TOP_START,n.anchorMargin={top:0,right:0,bottom:0,left:0},n.position={x:0,y:0},n}return(0,s.ZT)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return a},enumerable:!0,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return c},enumerable:!0,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return d},enumerable:!0,configurable:!0}),Object.defineProperty(e,"Corner",{get:function(){return o},enumerable:!0,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},hasClass:function(){return!1},hasAnchor:function(){return!1},isElementInContainer:function(){return!1},isFocused:function(){return!1},isRtl:function(){return!1},getInnerDimensions:function(){return{height:0,width:0}},getAnchorDimensions:function(){return null},getWindowDimensions:function(){return{height:0,width:0}},getBodyDimensions:function(){return{height:0,width:0}},getWindowScroll:function(){return{x:0,y:0}},setPosition:function(){},setMaxHeight:function(){},setTransformOrigin:function(){},saveFocus:function(){},restoreFocus:function(){},notifyClose:function(){},notifyOpen:function(){}}},enumerable:!0,configurable:!0}),e.prototype.init=function(){var t=e.cssClasses,i=t.ROOT,n=t.OPEN;if(!this.adapter.hasClass(i))throw new Error(i+" class required in root element.");this.adapter.hasClass(n)&&(this.isSurfaceOpen=!0)},e.prototype.destroy=function(){clearTimeout(this.openAnimationEndTimerId),clearTimeout(this.closeAnimationEndTimerId),cancelAnimationFrame(this.animationRequestId)},e.prototype.setAnchorCorner=function(t){this.anchorCorner=t},e.prototype.flipCornerHorizontally=function(){this.originCorner=this.originCorner^n.RIGHT},e.prototype.setAnchorMargin=function(t){this.anchorMargin.top=t.top||0,this.anchorMargin.right=t.right||0,this.anchorMargin.bottom=t.bottom||0,this.anchorMargin.left=t.left||0},e.prototype.setIsHoisted=function(t){this.isHoistedElement=t},e.prototype.setFixedPosition=function(t){this.isFixedPosition=t},e.prototype.setAbsolutePosition=function(t,e){this.position.x=this.isFinite(t)?t:0,this.position.y=this.isFinite(e)?e:0},e.prototype.setQuickOpen=function(t){this.isQuickOpen=t},e.prototype.isOpen=function(){return this.isSurfaceOpen},e.prototype.open=function(){var t=this;this.isSurfaceOpen||(this.adapter.saveFocus(),this.isQuickOpen?(this.isSurfaceOpen=!0,this.adapter.addClass(e.cssClasses.OPEN),this.dimensions=this.adapter.getInnerDimensions(),this.autoposition(),this.adapter.notifyOpen()):(this.adapter.addClass(e.cssClasses.ANIMATING_OPEN),this.animationRequestId=requestAnimationFrame((function(){t.adapter.addClass(e.cssClasses.OPEN),t.dimensions=t.adapter.getInnerDimensions(),t.autoposition(),t.openAnimationEndTimerId=setTimeout((function(){t.openAnimationEndTimerId=0,t.adapter.removeClass(e.cssClasses.ANIMATING_OPEN),t.adapter.notifyOpen()}),d.TRANSITION_OPEN_DURATION)})),this.isSurfaceOpen=!0))},e.prototype.close=function(t){var i=this;void 0===t&&(t=!1),this.isSurfaceOpen&&(this.isQuickOpen?(this.isSurfaceOpen=!1,t||this.maybeRestoreFocus(),this.adapter.removeClass(e.cssClasses.OPEN),this.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),this.adapter.notifyClose()):(this.adapter.addClass(e.cssClasses.ANIMATING_CLOSED),requestAnimationFrame((function(){i.adapter.removeClass(e.cssClasses.OPEN),i.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),i.closeAnimationEndTimerId=setTimeout((function(){i.closeAnimationEndTimerId=0,i.adapter.removeClass(e.cssClasses.ANIMATING_CLOSED),i.adapter.notifyClose()}),d.TRANSITION_CLOSE_DURATION)})),this.isSurfaceOpen=!1,t||this.maybeRestoreFocus()))},e.prototype.handleBodyClick=function(t){var e=t.target;this.adapter.isElementInContainer(e)||this.close()},e.prototype.handleKeydown=function(t){var e=t.keyCode;("Escape"===t.key||27===e)&&this.close()},e.prototype.autoposition=function(){var t;this.measurements=this.getAutoLayoutmeasurements();var i=this.getoriginCorner(),o=this.getMenuSurfaceMaxHeight(i),s=this.hasBit(i,n.BOTTOM)?"bottom":"top",r=this.hasBit(i,n.RIGHT)?"right":"left",a=this.getHorizontalOriginOffset(i),c=this.getVerticalOriginOffset(i),h=this.measurements,u=h.anchorSize,l=h.surfaceSize,m=((t={})[r]=a,t[s]=c,t);u.width/l.width>d.ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO&&(r="center"),(this.isHoistedElement||this.isFixedPosition)&&this.adjustPositionForHoistedElement(m),this.adapter.setTransformOrigin(r+" "+s),this.adapter.setPosition(m),this.adapter.setMaxHeight(o?o+"px":""),this.hasBit(i,n.BOTTOM)||this.adapter.addClass(e.cssClasses.IS_OPEN_BELOW)},e.prototype.getAutoLayoutmeasurements=function(){var t=this.adapter.getAnchorDimensions(),e=this.adapter.getBodyDimensions(),i=this.adapter.getWindowDimensions(),n=this.adapter.getWindowScroll();return t||(t={top:this.position.y,right:this.position.x,bottom:this.position.y,left:this.position.x,width:0,height:0}),{anchorSize:t,bodySize:e,surfaceSize:this.dimensions,viewportDistance:{top:t.top,right:i.width-t.right,bottom:i.height-t.bottom,left:t.left},viewportSize:i,windowScroll:n}},e.prototype.getoriginCorner=function(){var t,i,o=this.originCorner,s=this.measurements,r=s.viewportDistance,a=s.anchorSize,c=s.surfaceSize,d=e.numbers.MARGIN_TO_EDGE;this.hasBit(this.anchorCorner,n.BOTTOM)?(t=r.top-d+a.height+this.anchorMargin.bottom,i=r.bottom-d-this.anchorMargin.bottom):(t=r.top-d+this.anchorMargin.top,i=r.bottom-d+a.height-this.anchorMargin.top),!(i-c.height>0)&&t>=i&&(o=this.setBit(o,n.BOTTOM));var h,u,l=this.adapter.isRtl(),m=this.hasBit(this.anchorCorner,n.FLIP_RTL),p=this.hasBit(this.anchorCorner,n.RIGHT),f=!1;(f=l&&m?!p:p)?(h=r.left+a.width+this.anchorMargin.right,u=r.right-this.anchorMargin.right):(h=r.left+this.anchorMargin.left,u=r.right+a.width-this.anchorMargin.left);var T=h-c.width>0,g=u-c.width>0,y=this.hasBit(o,n.FLIP_RTL)&&this.hasBit(o,n.RIGHT);return g&&y&&l||!T&&y?o=this.unsetBit(o,n.RIGHT):(T&&f&&l||T&&!f&&p||!g&&h>=u)&&(o=this.setBit(o,n.RIGHT)),o},e.prototype.getMenuSurfaceMaxHeight=function(t){var i=this.measurements.viewportDistance,o=0,s=this.hasBit(t,n.BOTTOM),r=this.hasBit(this.anchorCorner,n.BOTTOM),a=e.numbers.MARGIN_TO_EDGE;return s?(o=i.top+this.anchorMargin.top-a,r||(o+=this.measurements.anchorSize.height)):(o=i.bottom-this.anchorMargin.bottom+this.measurements.anchorSize.height-a,r&&(o-=this.measurements.anchorSize.height)),o},e.prototype.getHorizontalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,n.RIGHT),o=this.hasBit(this.anchorCorner,n.RIGHT);if(i){var s=o?e.width-this.anchorMargin.left:this.anchorMargin.right;return this.isHoistedElement||this.isFixedPosition?s-(this.measurements.viewportSize.width-this.measurements.bodySize.width):s}return o?e.width-this.anchorMargin.right:this.anchorMargin.left},e.prototype.getVerticalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,n.BOTTOM),o=this.hasBit(this.anchorCorner,n.BOTTOM);return i?o?e.height-this.anchorMargin.top:-this.anchorMargin.bottom:o?e.height+this.anchorMargin.bottom:this.anchorMargin.top},e.prototype.adjustPositionForHoistedElement=function(t){var e,i,n=this.measurements,o=n.windowScroll,r=n.viewportDistance,a=Object.keys(t);try{for(var c=(0,s.XA)(a),d=c.next();!d.done;d=c.next()){var h=d.value,u=t[h]||0;u+=r[h],this.isFixedPosition||("top"===h?u+=o.y:"bottom"===h?u-=o.y:"left"===h?u+=o.x:u-=o.x),t[h]=u}}catch(l){e={error:l}}finally{try{d&&!d.done&&(i=c.return)&&i.call(c)}finally{if(e)throw e.error}}},e.prototype.maybeRestoreFocus=function(){var t=this.adapter.isFocused(),e=document.activeElement&&this.adapter.isElementInContainer(document.activeElement);(t||e)&&this.adapter.restoreFocus()},e.prototype.hasBit=function(t,e){return Boolean(t&e)},e.prototype.setBit=function(t,e){return t|e},e.prototype.unsetBit=function(t,e){return t^e},e.prototype.isFinite=function(t){return"number"==typeof t&&isFinite(t)},e}(h.K);const l=u;var m=i(78220),p=i(14114),f=i(82612),T=i(81471),g=i(79865);const y={TOP_LEFT:o.TOP_LEFT,TOP_RIGHT:o.TOP_RIGHT,BOTTOM_LEFT:o.BOTTOM_LEFT,BOTTOM_RIGHT:o.BOTTOM_RIGHT,TOP_START:o.TOP_START,TOP_END:o.TOP_END,BOTTOM_START:o.BOTTOM_START,BOTTOM_END:o.BOTTOM_END};class O extends m.H{constructor(){super(...arguments),this.mdcFoundationClass=l,this.absolute=!1,this.fullwidth=!1,this.fixed=!1,this.x=null,this.y=null,this.quick=!1,this.open=!1,this.bitwiseCorner=o.TOP_START,this.previousMenuCorner=null,this.menuCorner="START",this.corner="TOP_START",this.styleTop="",this.styleLeft="",this.styleRight="",this.styleBottom="",this.styleMaxHeight="",this.styleTransformOrigin="",this.anchor=null,this.previouslyFocused=null,this.previousAnchor=null,this.onBodyClickBound=()=>{}}render(){const t={"mdc-menu-surface--fixed":this.fixed,"mdc-menu-surface--fullwidth":this.fullwidth},e={top:this.styleTop,left:this.styleLeft,right:this.styleRight,bottom:this.styleBottom,"max-height":this.styleMaxHeight,"transform-origin":this.styleTransformOrigin};return r.dy`
      <div
          class="mdc-menu-surface ${(0,T.$)(t)}"
          style="${(0,g.V)(e)}"
          @keydown=${this.onKeydown}
          @opened=${this.registerBodyClick}
          @closed=${this.deregisterBodyClick}>
        <slot></slot>
      </div>`}createAdapter(){return Object.assign(Object.assign({},(0,m.q)(this.mdcRoot)),{hasAnchor:()=>!!this.anchor,notifyClose:()=>{const t=new CustomEvent("closed",{bubbles:!0,composed:!0});this.open=!1,this.mdcRoot.dispatchEvent(t)},notifyOpen:()=>{const t=new CustomEvent("opened",{bubbles:!0,composed:!0});this.open=!0,this.mdcRoot.dispatchEvent(t)},isElementInContainer:()=>!1,isRtl:()=>!!this.mdcRoot&&"rtl"===getComputedStyle(this.mdcRoot).direction,setTransformOrigin:t=>{this.mdcRoot&&(this.styleTransformOrigin=t)},isFocused:()=>(0,f.WU)(this),saveFocus:()=>{const t=(0,f.Mh)(),e=t.length;e||(this.previouslyFocused=null),this.previouslyFocused=t[e-1]},restoreFocus:()=>{this.previouslyFocused&&"focus"in this.previouslyFocused&&this.previouslyFocused.focus()},getInnerDimensions:()=>{const t=this.mdcRoot;return t?{width:t.offsetWidth,height:t.offsetHeight}:{width:0,height:0}},getAnchorDimensions:()=>{const t=this.anchor;return t?t.getBoundingClientRect():null},getBodyDimensions:()=>({width:document.body.clientWidth,height:document.body.clientHeight}),getWindowDimensions:()=>({width:window.innerWidth,height:window.innerHeight}),getWindowScroll:()=>({x:window.pageXOffset,y:window.pageYOffset}),setPosition:t=>{this.mdcRoot&&(this.styleLeft="left"in t?t.left+"px":"",this.styleRight="right"in t?t.right+"px":"",this.styleTop="top"in t?t.top+"px":"",this.styleBottom="bottom"in t?t.bottom+"px":"")},setMaxHeight:async t=>{this.mdcRoot&&(this.styleMaxHeight=t,await this.updateComplete,this.styleMaxHeight=`var(--mdc-menu-max-height, ${t})`)}})}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onBodyClick(t){-1===t.composedPath().indexOf(this)&&this.close()}registerBodyClick(){this.onBodyClickBound=this.onBodyClick.bind(this),document.body.addEventListener("click",this.onBodyClickBound,{passive:!0,capture:!0})}deregisterBodyClick(){document.body.removeEventListener("click",this.onBodyClickBound)}close(){this.open=!1}show(){this.open=!0}}(0,s.gn)([(0,r.IO)(".mdc-menu-surface")],O.prototype,"mdcRoot",void 0),(0,s.gn)([(0,r.IO)("slot")],O.prototype,"slotElement",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean}),(0,p.P)((function(t){this.mdcFoundation&&!this.fixed&&this.mdcFoundation.setIsHoisted(t)}))],O.prototype,"absolute",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],O.prototype,"fullwidth",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean}),(0,p.P)((function(t){this.mdcFoundation&&!this.absolute&&this.mdcFoundation.setIsHoisted(t)}))],O.prototype,"fixed",void 0),(0,s.gn)([(0,r.Cb)({type:Number}),(0,p.P)((function(t){this.mdcFoundation&&null!==this.y&&null!==t&&(this.mdcFoundation.setAbsolutePosition(t,this.y),this.mdcFoundation.setAnchorMargin({left:t,top:this.y,right:-t,bottom:this.y}))}))],O.prototype,"x",void 0),(0,s.gn)([(0,r.Cb)({type:Number}),(0,p.P)((function(t){this.mdcFoundation&&null!==this.x&&null!==t&&(this.mdcFoundation.setAbsolutePosition(this.x,t),this.mdcFoundation.setAnchorMargin({left:this.x,top:t,right:-this.x,bottom:t}))}))],O.prototype,"y",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean}),(0,p.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setQuickOpen(t)}))],O.prototype,"quick",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean,reflect:!0}),(0,p.P)((function(t,e){this.mdcFoundation&&(t?this.mdcFoundation.open():void 0!==e&&this.mdcFoundation.close())}))],O.prototype,"open",void 0),(0,s.gn)([(0,r.sz)(),(0,p.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setAnchorCorner(t)}))],O.prototype,"bitwiseCorner",void 0),(0,s.gn)([(0,r.Cb)({type:String}),(0,p.P)((function(t){if(this.mdcFoundation){const e="START"===t||"END"===t,i=null===this.previousMenuCorner,o=!i&&t!==this.previousMenuCorner,s=i&&"END"===t;e&&(o||s)&&(this.bitwiseCorner=this.bitwiseCorner^n.RIGHT,this.mdcFoundation.flipCornerHorizontally(),this.previousMenuCorner=t)}}))],O.prototype,"menuCorner",void 0),(0,s.gn)([(0,r.Cb)({type:String}),(0,p.P)((function(t){if(this.mdcFoundation&&t){let e=y[t];"END"===this.menuCorner&&(e^=n.RIGHT),this.bitwiseCorner=e}}))],O.prototype,"corner",void 0),(0,s.gn)([(0,r.sz)()],O.prototype,"styleTop",void 0),(0,s.gn)([(0,r.sz)()],O.prototype,"styleLeft",void 0),(0,s.gn)([(0,r.sz)()],O.prototype,"styleRight",void 0),(0,s.gn)([(0,r.sz)()],O.prototype,"styleBottom",void 0),(0,s.gn)([(0,r.sz)()],O.prototype,"styleMaxHeight",void 0),(0,s.gn)([(0,r.sz)()],O.prototype,"styleTransformOrigin",void 0);const E=r.iv`.mdc-menu-surface{display:none;position:absolute;box-sizing:border-box;max-width:calc(100vw - 32px);max-height:calc(100vh - 32px);margin:0;padding:0;transform:scale(1);transform-origin:top left;opacity:0;overflow:auto;will-change:transform,opacity;z-index:8;transition:opacity .03s linear,transform .12s cubic-bezier(0, 0, 0.2, 1),height 250ms cubic-bezier(0, 0, 0.2, 1);box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12);background-color:#fff;background-color:var(--mdc-theme-surface, #fff);color:#000;color:var(--mdc-theme-on-surface, #000);border-radius:4px;border-radius:var(--mdc-shape-medium, 4px);transform-origin-left:top left;transform-origin-right:top right}.mdc-menu-surface:focus{outline:none}.mdc-menu-surface--open{display:inline-block;transform:scale(1);opacity:1}.mdc-menu-surface--animating-open{display:inline-block;transform:scale(0.8);opacity:0}.mdc-menu-surface--animating-closed{display:inline-block;opacity:0;transition:opacity .075s linear}[dir=rtl] .mdc-menu-surface,.mdc-menu-surface[dir=rtl]{transform-origin-left:top right;transform-origin-right:top left}.mdc-menu-surface--anchor{position:relative;overflow:visible}.mdc-menu-surface--fixed{position:fixed}.mdc-menu-surface--fullwidth{width:100%}:host(:not([open])){display:none}.mdc-menu-surface{z-index:8;z-index:var(--mdc-menu-z-index, 8);max-height:calc(100vh - 32px);max-height:var(--mdc-menu-max-height, calc(100vh - 32px))}`;let I=class extends O{};I.styles=E,I=(0,s.gn)([(0,r.Mo)("mwc-menu-surface")],I);var C,b={MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"},A={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list",SELECTED_EVENT:"MDCMenu:selected"},_={FOCUS_ROOT_INDEX:-1};!function(t){t[t.NONE=0]="NONE",t[t.LIST_ROOT=1]="LIST_ROOT",t[t.FIRST_ITEM=2]="FIRST_ITEM",t[t.LAST_ITEM=3]="LAST_ITEM"}(C||(C={}));var v=i(74015);const x=function(t){function e(i){var n=t.call(this,(0,s.pi)((0,s.pi)({},e.defaultAdapter),i))||this;return n.closeAnimationEndTimerId_=0,n.defaultFocusState_=C.LIST_ROOT,n}return(0,s.ZT)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return b},enumerable:!0,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return A},enumerable:!0,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return _},enumerable:!0,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!0,configurable:!0}),e.prototype.destroy=function(){this.closeAnimationEndTimerId_&&clearTimeout(this.closeAnimationEndTimerId_),this.adapter.closeSurface()},e.prototype.handleKeydown=function(t){var e=t.key,i=t.keyCode;("Tab"===e||9===i)&&this.adapter.closeSurface(!0)},e.prototype.handleItemAction=function(t){var e=this,i=this.adapter.getElementIndex(t);i<0||(this.adapter.notifySelected({index:i}),this.adapter.closeSurface(),this.closeAnimationEndTimerId_=setTimeout((function(){var i=e.adapter.getElementIndex(t);i>=0&&e.adapter.isSelectableItemAtIndex(i)&&e.setSelectedIndex(i)}),u.numbers.TRANSITION_CLOSE_DURATION))},e.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState_){case C.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case C.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case C.NONE:break;default:this.adapter.focusListRoot()}},e.prototype.setDefaultFocusState=function(t){this.defaultFocusState_=t},e.prototype.setSelectedIndex=function(t){if(this.validatedIndex_(t),!this.adapter.isSelectableItemAtIndex(t))throw new Error("MDCMenuFoundation: No selection group at specified index.");var e=this.adapter.getSelectedSiblingOfItemAtIndex(t);e>=0&&(this.adapter.removeAttributeFromElementAtIndex(e,A.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(e,b.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(t,b.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(t,A.ARIA_CHECKED_ATTR,"true")},e.prototype.setEnabled=function(t,e){this.validatedIndex_(t),e?(this.adapter.removeClassFromElementAtIndex(t,v.UX.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(t,A.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(t,v.UX.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(t,A.ARIA_DISABLED_ATTR,"true"))},e.prototype.validatedIndex_=function(t){var e=this.adapter.getMenuItemCount();if(!(t>=0&&t<e))throw new Error("MDCMenuFoundation: No list item at specified index.")},e}(h.K);i(10333);class S extends m.H{constructor(){super(...arguments),this.mdcFoundationClass=x,this.listElement_=null,this.anchor=null,this.open=!1,this.quick=!1,this.wrapFocus=!1,this.innerRole="menu",this.corner="TOP_START",this.x=null,this.y=null,this.absolute=!1,this.multi=!1,this.activatable=!1,this.fixed=!1,this.forceGroupSelection=!1,this.fullwidth=!1,this.menuCorner="START",this.defaultFocus="LIST_ROOT",this._listUpdateComplete=null}get listElement(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}get items(){const t=this.listElement;return t?t.items:[]}get index(){const t=this.listElement;return t?t.index:-1}get selected(){const t=this.listElement;return t?t.selected:null}render(){const t="menu"===this.innerRole?"menuitem":"option";return r.dy`
      <mwc-menu-surface
          ?hidden=${!this.open}
          .anchor=${this.anchor}
          .open=${this.open}
          .quick=${this.quick}
          .corner=${this.corner}
          .x=${this.x}
          .y=${this.y}
          .absolute=${this.absolute}
          .fixed=${this.fixed}
          .fullwidth=${this.fullwidth}
          .menuCorner=${this.menuCorner}
          class="mdc-menu mdc-menu-surface"
          @closed=${this.onClosed}
          @opened=${this.onOpened}
          @keydown=${this.onKeydown}>
        <mwc-list
          rootTabbable
          .innerRole=${this.innerRole}
          .multi=${this.multi}
          class="mdc-list"
          .itemRoles=${t}
          .wrapFocus=${this.wrapFocus}
          .activatable=${this.activatable}
          @action=${this.onAction}>
        <slot></slot>
      </mwc-list>
    </mwc-menu-surface>`}createAdapter(){return{addClassToElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&("mdc-menu-item--selected"===e?this.forceGroupSelection&&!n.selected&&i.toggle(t,!0):n.classList.add(e))},removeClassFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&("mdc-menu-item--selected"===e?n.selected&&i.toggle(t,!1):n.classList.remove(e))},addAttributeToElementAtIndex:(t,e,i)=>{const n=this.listElement;if(!n)return;const o=n.items[t];o&&o.setAttribute(e,i)},removeAttributeFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&n.removeAttribute(e)},elementContainsClass:(t,e)=>t.classList.contains(e),closeSurface:()=>{this.open=!1},getElementIndex:t=>{const e=this.listElement;return e?e.items.indexOf(t):-1},notifySelected:()=>{},getMenuItemCount:()=>{const t=this.listElement;return t?t.items.length:0},focusItemAtIndex:t=>{const e=this.listElement;if(!e)return;const i=e.items[t];i&&i.focus()},focusListRoot:()=>{this.listElement&&this.listElement.focus()},getSelectedSiblingOfItemAtIndex:t=>{const e=this.listElement;if(!e)return-1;const i=e.items[t];if(!i||!i.group)return-1;for(let n=0;n<e.items.length;n++){if(n===t)continue;const o=e.items[n];if(o.selected&&o.group===i.group)return n}return-1},isSelectableItemAtIndex:t=>{const e=this.listElement;if(!e)return!1;const i=e.items[t];return!!i&&i.hasAttribute("group")}}}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onAction(t){const e=this.listElement;if(this.mdcFoundation&&e){const i=t.detail.index,n=e.items[i];n&&this.mdcFoundation.handleItemAction(n)}}onOpened(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}onClosed(){this.open=!1}async _getUpdateComplete(){await this._listUpdateComplete,await super._getUpdateComplete()}async firstUpdated(){super.firstUpdated();const t=this.listElement;t&&(this._listUpdateComplete=t.updateComplete,await this._listUpdateComplete)}select(t){const e=this.listElement;e&&e.select(t)}close(){this.open=!1}show(){this.open=!0}getFocusedItemIndex(){const t=this.listElement;return t?t.getFocusedItemIndex():-1}focusItemAtIndex(t){const e=this.listElement;e&&e.focusItemAtIndex(t)}layout(t=!0){const e=this.listElement;e&&e.layout(t)}}(0,s.gn)([(0,r.IO)(".mdc-menu")],S.prototype,"mdcRoot",void 0),(0,s.gn)([(0,r.IO)("slot")],S.prototype,"slotElement",void 0),(0,s.gn)([(0,r.Cb)({type:Object})],S.prototype,"anchor",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean,reflect:!0})],S.prototype,"open",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],S.prototype,"quick",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],S.prototype,"wrapFocus",void 0),(0,s.gn)([(0,r.Cb)({type:String})],S.prototype,"innerRole",void 0),(0,s.gn)([(0,r.Cb)({type:String})],S.prototype,"corner",void 0),(0,s.gn)([(0,r.Cb)({type:Number})],S.prototype,"x",void 0),(0,s.gn)([(0,r.Cb)({type:Number})],S.prototype,"y",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],S.prototype,"absolute",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],S.prototype,"multi",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],S.prototype,"activatable",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],S.prototype,"fixed",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],S.prototype,"forceGroupSelection",void 0),(0,s.gn)([(0,r.Cb)({type:Boolean})],S.prototype,"fullwidth",void 0),(0,s.gn)([(0,r.Cb)({type:String})],S.prototype,"menuCorner",void 0),(0,s.gn)([(0,r.Cb)({type:String}),(0,p.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(C[t])}))],S.prototype,"defaultFocus",void 0);const R=r.iv`mwc-list ::slotted([mwc-list-item]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}mwc-list{max-width:var(--mdc-menu-max-width, auto);min-width:var(--mdc-menu-min-width, auto)}`;let M=class extends S{};M.styles=R,M=(0,s.gn)([(0,r.Mo)("mwc-menu")],M)}}]);
//# sourceMappingURL=chunk.9f0f063aeb9762599f83.js.map