(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[22],{1186:function(e,t,n){"use strict";var r=n(5),o=n.n(r),i=o()("label",{target:"effi0qh0"})((function(e){var t=e.theme;return{fontSize:t.fontSizes.smDefault,color:t.colors.bodyText,marginBottom:t.fontSizes.halfSmDefault}}),""),a=o()("div",{target:"effi0qh1"})((function(e){var t=e.theme;return{fontSize:t.fontSizes.smDefault,color:t.colors.gray,margin:t.spacing.none,textAlign:"right",position:"absolute",bottom:0,right:t.fontSizes.halfSmDefault}}),"");n.d(t,"a",(function(){return a})),n.d(t,"b",(function(){return i}))},1231:function(e,t,n){"use strict";n.d(t,"b",(function(){return r})),n.d(t,"a",(function(){return o})),n.d(t,"d",(function(){return i})),n.d(t,"c",(function(){return a}));var r={textarea:"textarea"},o={none:"none",left:"left",right:"right",both:"both"},i={mini:"mini",default:"default",compact:"compact",large:"large"},a={start:"start",end:"end"}},1326:function(e,t,n){"use strict";var r=n(0),o=n(23),i=n(14),a=n(104),c=n(105);function u(){return(u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function l(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?l(Object(n),!0).forEach((function(t){f(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function f(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function p(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}function b(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if(!(Symbol.iterator in Object(e))&&"[object Arguments]"!==Object.prototype.toString.call(e))return;var n=[],r=!0,o=!1,i=void 0;try{for(var a,c=e[Symbol.iterator]();!(r=(a=c.next()).done)&&(n.push(a.value),!t||n.length!==t);r=!0);}catch(u){o=!0,i=u}finally{try{r||null==c.return||c.return()}finally{if(o)throw i}}return n}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()}t.a=r.forwardRef((function(e,t){var n=b(Object(o.b)(),2)[1],l=e.overrides,f=void 0===l?{}:l,y=p(e,["overrides"]),d=Object(i.d)({component:n.icons&&n.icons.DeleteAlt?n.icons.DeleteAlt:null,props:s({title:"Delete Alt",viewBox:"0 0 24 24"},Object(c.a)(y))},f&&f.Svg?Object(i.f)(f.Svg):{});return r.createElement(a.a,u({title:"Delete Alt",viewBox:"0 0 24 24",ref:t,overrides:{Svg:d}},y),r.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12 20C16.4183 20 20 16.4183 20 12C20 7.58173 16.4183 4 12 4C7.58173 4 4 7.58173 4 12C4 16.4183 7.58173 20 12 20ZM10.0303 8.96967C9.73743 8.67679 9.26257 8.67679 8.96967 8.96967C8.67676 9.26257 8.67676 9.73743 8.96967 10.0303L10.9393 12L8.96967 13.9697C8.67676 14.2626 8.67676 14.7374 8.96967 15.0303C9.26257 15.3232 9.73743 15.3232 10.0303 15.0303L12 13.0607L13.9697 15.0303C14.2626 15.3232 14.7374 15.3232 15.0303 15.0303C15.3232 14.7374 15.3232 14.2626 15.0303 13.9697L13.0607 12L15.0303 10.0303C15.3232 9.73743 15.3232 9.26257 15.0303 8.96967C14.7374 8.67679 14.2626 8.67679 13.9697 8.96967L12 10.9393L10.0303 8.96967Z"}))}))},1328:function(e,t,n){"use strict";var r=n(0),o=n.n(r),i=n(44),a=n(1186),c=n(6),u=n(143),l=n(5),s=n.n(l),f=n(106);function p(){var e=Object(u.a)(["\n  50% {\n    color: rgba(0, 0, 0, 0);\n  }\n"]);return p=function(){return e},e}var b=Object(f.keyframes)(p()),y=s()("span",{target:"e1m4n6jn0"})((function(e){var t=e.includeDot,n=e.shouldBlink,r=e.theme;return Object(c.a)(Object(c.a)({},t?{"&::before":{opacity:1,content:'"\u2022"',animation:"none",color:r.colors.gray,margin:"0 5px"}}:{}),n?{color:r.colors.red,animationName:"".concat(b),animationDuration:"0.5s",animationIterationCount:5}:{})}),"");t.a=function(e){var t=e.dirty,n=e.value,r=e.maxLength,c=e.className,u=e.type,l=[],s=function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];l.push(o.a.createElement(y,{key:l.length,includeDot:l.length>0,shouldBlink:t},e))};return t&&("multiline"===(void 0===u?"single":u)?Object(i.f)()?s("Press \u2318+Enter to apply"):s("Press Ctrl+Enter to apply"):s("Press Enter to apply")),r&&s("".concat(n.length,"/").concat(r),t&&n.length>=r),o.a.createElement(a.a,{className:c},l)}},3831:function(e,t,n){"use strict";n.r(t);var r=n(9),o=n(13),i=n(20),a=n(21),c=n(0),u=n.n(c),l=n(14),s=n(1520),f=n(1231),p=n(23),b=n(1285);function y(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function d(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?y(Object(n),!0).forEach((function(t){v(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):y(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function v(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var m=Object(p.a)("div",(function(e){return d({},Object(b.h)(e))}));m.displayName="StyledTextareaContainer";var h=Object(p.a)("textarea",(function(e){return d({},Object(b.i)(e),{resize:"none"})}));function g(e){return(g="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function O(){return(O=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function j(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function w(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function P(e,t){return!t||"object"!==g(t)&&"function"!==typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function S(e){return(S=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function C(e,t){return(C=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}h.displayName="StyledTextarea";var D,E,x,k=function(e){function t(){return j(this,t),P(this,S(t).apply(this,arguments))}var n,r,o;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&C(e,t)}(t,e),n=t,(r=[{key:"render",value:function(){var e=Object(l.e)({Input:{component:h},InputContainer:{component:m}},this.props.overrides);return c.createElement(s.a,O({"data-baseweb":"textarea"},this.props,{type:f.b.textarea,overrides:e}))}}])&&w(n.prototype,r),o&&w(n,o),t}(c.Component);D=k,E="defaultProps",x={autoFocus:!1,disabled:!1,error:!1,name:"",onBlur:function(){},onChange:function(){},onKeyDown:function(){},onKeyPress:function(){},onKeyUp:function(){},onFocus:function(){},overrides:{},placeholder:"",required:!1,rows:3,size:f.d.default,value:""},E in D?Object.defineProperty(D,E,{value:x,enumerable:!0,configurable:!0,writable:!0}):D[E]=x;var A=k,K=n(1328),L=n(1186),z=function(e){Object(i.a)(n,e);var t=Object(a.a)(n);function n(){var e;Object(r.a)(this,n);for(var o=arguments.length,i=new Array(o),a=0;a<o;a++)i[a]=arguments[a];return(e=t.call.apply(t,[this].concat(i))).state={dirty:!1,value:e.initialValue},e.setWidgetValue=function(t){var n=e.props.element.id;e.props.widgetMgr.setStringValue(n,e.state.value,t),e.setState({dirty:!1})},e.onBlur=function(){e.state.dirty&&e.setWidgetValue({fromUi:!0})},e.onChange=function(t){var n=t.target.value,r=e.props.element.maxChars;(!r||n.length<=r)&&e.setState({dirty:!0,value:n})},e.isEnterKeyPressed=function(e){var t=e.keyCode;return"Enter"===e.key||13===t||10===t},e.onKeyDown=function(t){var n=t.metaKey,r=t.ctrlKey,o=e.state.dirty;e.isEnterKeyPressed(t)&&(r||n)&&o&&(t.preventDefault(),e.setWidgetValue({fromUi:!0}))},e.render=function(){var t=e.props,n=t.element,r=t.disabled,o=t.width,i=e.state,a=i.value,c=i.dirty,l={width:o},s=n.height;return u.a.createElement("div",{className:"stTextArea",style:l},u.a.createElement(L.b,null,n.label),u.a.createElement(A,{value:a,onBlur:e.onBlur,onChange:e.onChange,onKeyDown:e.onKeyDown,disabled:r,overrides:{Input:{style:{height:s?"".concat(s,"px"):"",minHeight:"95px",resize:s?"vertical":"none"}}}}),u.a.createElement(K.a,{dirty:c,value:a,maxLength:n.maxChars,type:"multiline"}))},e}return Object(o.a)(n,[{key:"componentDidMount",value:function(){this.setWidgetValue({fromUi:!1})}},{key:"initialValue",get:function(){var e=this.props.element.id,t=this.props.widgetMgr.getStringValue(e);return void 0!==t?t:this.props.element.default}}]),n}(u.a.PureComponent);n.d(t,"default",(function(){return z}))}}]);
//# sourceMappingURL=22.1021b00e.chunk.js.map