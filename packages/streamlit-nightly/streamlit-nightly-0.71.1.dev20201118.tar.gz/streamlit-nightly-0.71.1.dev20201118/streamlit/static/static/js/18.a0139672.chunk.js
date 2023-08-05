(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[18],{1186:function(e,t,n){"use strict";var r=n(5),o=n.n(r),i=o()("label",{target:"effi0qh0"})((function(e){var t=e.theme;return{fontSize:t.fontSizes.smDefault,color:t.colors.bodyText,marginBottom:t.fontSizes.halfSmDefault}}),""),a=o()("div",{target:"effi0qh1"})((function(e){var t=e.theme;return{fontSize:t.fontSizes.smDefault,color:t.colors.gray,margin:t.spacing.none,textAlign:"right",position:"absolute",bottom:0,right:t.fontSizes.halfSmDefault}}),"");n.d(t,"a",(function(){return a})),n.d(t,"b",(function(){return i}))},1231:function(e,t,n){"use strict";n.d(t,"b",(function(){return r})),n.d(t,"a",(function(){return o})),n.d(t,"d",(function(){return i})),n.d(t,"c",(function(){return a}));var r={textarea:"textarea"},o={none:"none",left:"left",right:"right",both:"both"},i={mini:"mini",default:"default",compact:"compact",large:"large"},a={start:"start",end:"end"}},1295:function(e,t,n){var r;!function(){"use strict";var o={not_string:/[^s]/,not_bool:/[^t]/,not_type:/[^T]/,not_primitive:/[^v]/,number:/[diefg]/,numeric_arg:/[bcdiefguxX]/,json:/[j]/,not_json:/[^j]/,text:/^[^\x25]+/,modulo:/^\x25{2}/,placeholder:/^\x25(?:([1-9]\d*)\$|\(([^)]+)\))?(\+)?(0|'[^$])?(-)?(\d+)?(?:\.(\d+))?([b-gijostTuvxX])/,key:/^([a-z_][a-z_\d]*)/i,key_access:/^\.([a-z_][a-z_\d]*)/i,index_access:/^\[(\d+)\]/,sign:/^[+-]/};function i(e){return c(u(e),arguments)}function a(e,t){return i.apply(null,[e].concat(t||[]))}function c(e,t){var n,r,a,c,s,u,l,p,f,d=1,y=e.length,b="";for(r=0;r<y;r++)if("string"===typeof e[r])b+=e[r];else if("object"===typeof e[r]){if((c=e[r]).keys)for(n=t[d],a=0;a<c.keys.length;a++){if(void 0==n)throw new Error(i('[sprintf] Cannot access property "%s" of undefined value "%s"',c.keys[a],c.keys[a-1]));n=n[c.keys[a]]}else n=c.param_no?t[c.param_no]:t[d++];if(o.not_type.test(c.type)&&o.not_primitive.test(c.type)&&n instanceof Function&&(n=n()),o.numeric_arg.test(c.type)&&"number"!==typeof n&&isNaN(n))throw new TypeError(i("[sprintf] expecting number but found %T",n));switch(o.number.test(c.type)&&(p=n>=0),c.type){case"b":n=parseInt(n,10).toString(2);break;case"c":n=String.fromCharCode(parseInt(n,10));break;case"d":case"i":n=parseInt(n,10);break;case"j":n=JSON.stringify(n,null,c.width?parseInt(c.width):0);break;case"e":n=c.precision?parseFloat(n).toExponential(c.precision):parseFloat(n).toExponential();break;case"f":n=c.precision?parseFloat(n).toFixed(c.precision):parseFloat(n);break;case"g":n=c.precision?String(Number(n.toPrecision(c.precision))):parseFloat(n);break;case"o":n=(parseInt(n,10)>>>0).toString(8);break;case"s":n=String(n),n=c.precision?n.substring(0,c.precision):n;break;case"t":n=String(!!n),n=c.precision?n.substring(0,c.precision):n;break;case"T":n=Object.prototype.toString.call(n).slice(8,-1).toLowerCase(),n=c.precision?n.substring(0,c.precision):n;break;case"u":n=parseInt(n,10)>>>0;break;case"v":n=n.valueOf(),n=c.precision?n.substring(0,c.precision):n;break;case"x":n=(parseInt(n,10)>>>0).toString(16);break;case"X":n=(parseInt(n,10)>>>0).toString(16).toUpperCase()}o.json.test(c.type)?b+=n:(!o.number.test(c.type)||p&&!c.sign?f="":(f=p?"+":"-",n=n.toString().replace(o.sign,"")),u=c.pad_char?"0"===c.pad_char?"0":c.pad_char.charAt(1):" ",l=c.width-(f+n).length,s=c.width&&l>0?u.repeat(l):"",b+=c.align?f+n+s:"0"===u?f+s+n:s+f+n)}return b}var s=Object.create(null);function u(e){if(s[e])return s[e];for(var t,n=e,r=[],i=0;n;){if(null!==(t=o.text.exec(n)))r.push(t[0]);else if(null!==(t=o.modulo.exec(n)))r.push("%");else{if(null===(t=o.placeholder.exec(n)))throw new SyntaxError("[sprintf] unexpected placeholder");if(t[2]){i|=1;var a=[],c=t[2],u=[];if(null===(u=o.key.exec(c)))throw new SyntaxError("[sprintf] failed to parse named argument key");for(a.push(u[1]);""!==(c=c.substring(u[0].length));)if(null!==(u=o.key_access.exec(c)))a.push(u[1]);else{if(null===(u=o.index_access.exec(c)))throw new SyntaxError("[sprintf] failed to parse named argument key");a.push(u[1])}t[2]=a}else i|=2;if(3===i)throw new Error("[sprintf] mixing positional and named placeholders is not (yet) supported");r.push({placeholder:t[0],param_no:t[1],keys:t[2],sign:t[3],pad_char:t[4],align:t[5],width:t[6],precision:t[7],type:t[8]})}n=n.substring(t[0].length)}return s[e]=r}t.sprintf=i,t.vsprintf=a,"undefined"!==typeof window&&(window.sprintf=i,window.vsprintf=a,void 0===(r=function(){return{sprintf:i,vsprintf:a}}.call(t,n,t,e))||(e.exports=r))}()},1326:function(e,t,n){"use strict";var r=n(0),o=n(23),i=n(14),a=n(104),c=n(105);function s(){return(s=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function u(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?u(Object(n),!0).forEach((function(t){p(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):u(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function p(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function f(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}function d(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if(!(Symbol.iterator in Object(e))&&"[object Arguments]"!==Object.prototype.toString.call(e))return;var n=[],r=!0,o=!1,i=void 0;try{for(var a,c=e[Symbol.iterator]();!(r=(a=c.next()).done)&&(n.push(a.value),!t||n.length!==t);r=!0);}catch(s){o=!0,i=s}finally{try{r||null==c.return||c.return()}finally{if(o)throw i}}return n}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()}t.a=r.forwardRef((function(e,t){var n=d(Object(o.b)(),2)[1],u=e.overrides,p=void 0===u?{}:u,y=f(e,["overrides"]),b=Object(i.d)({component:n.icons&&n.icons.DeleteAlt?n.icons.DeleteAlt:null,props:l({title:"Delete Alt",viewBox:"0 0 24 24"},Object(c.a)(y))},p&&p.Svg?Object(i.f)(p.Svg):{});return r.createElement(a.a,s({title:"Delete Alt",viewBox:"0 0 24 24",ref:t,overrides:{Svg:b}},y),r.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12 20C16.4183 20 20 16.4183 20 12C20 7.58173 16.4183 4 12 4C7.58173 4 4 7.58173 4 12C4 16.4183 7.58173 20 12 20ZM10.0303 8.96967C9.73743 8.67679 9.26257 8.67679 8.96967 8.96967C8.67676 9.26257 8.67676 9.73743 8.96967 10.0303L10.9393 12L8.96967 13.9697C8.67676 14.2626 8.67676 14.7374 8.96967 15.0303C9.26257 15.3232 9.73743 15.3232 10.0303 15.0303L12 13.0607L13.9697 15.0303C14.2626 15.3232 14.7374 15.3232 15.0303 15.0303C15.3232 14.7374 15.3232 14.2626 15.0303 13.9697L13.0607 12L15.0303 10.0303C15.3232 9.73743 15.3232 9.26257 15.0303 8.96967C14.7374 8.67679 14.2626 8.67679 13.9697 8.96967L12 10.9393L10.0303 8.96967Z"}))}))},1328:function(e,t,n){"use strict";var r=n(0),o=n.n(r),i=n(44),a=n(1186),c=n(6),s=n(143),u=n(5),l=n.n(u),p=n(106);function f(){var e=Object(s.a)(["\n  50% {\n    color: rgba(0, 0, 0, 0);\n  }\n"]);return f=function(){return e},e}var d=Object(p.keyframes)(f()),y=l()("span",{target:"e1m4n6jn0"})((function(e){var t=e.includeDot,n=e.shouldBlink,r=e.theme;return Object(c.a)(Object(c.a)({},t?{"&::before":{opacity:1,content:'"\u2022"',animation:"none",color:r.colors.gray,margin:"0 5px"}}:{}),n?{color:r.colors.red,animationName:"".concat(d),animationDuration:"0.5s",animationIterationCount:5}:{})}),"");t.a=function(e){var t=e.dirty,n=e.value,r=e.maxLength,c=e.className,s=e.type,u=[],l=function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];u.push(o.a.createElement(y,{key:u.length,includeDot:u.length>0,shouldBlink:t},e))};return t&&("multiline"===(void 0===s?"single":s)?Object(i.f)()?l("Press \u2318+Enter to apply"):l("Press Ctrl+Enter to apply"):l("Press Enter to apply")),r&&l("".concat(n.length,"/").concat(r),t&&n.length>=r),o.a.createElement(a.a,{className:c},u)}},1509:function(e,t,n){"use strict";var r=n(0),o=n(14),i=n(1386),a=n(1520),c=n(1285),s=n(1231);function u(e){return(u="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function l(){return(l=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function p(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if(!(Symbol.iterator in Object(e))&&"[object Arguments]"!==Object.prototype.toString.call(e))return;var n=[],r=!0,o=!1,i=void 0;try{for(var a,c=e[Symbol.iterator]();!(r=(a=c.next()).done)&&(n.push(a.value),!t||n.length!==t);r=!0);}catch(s){o=!0,i=s}finally{try{r||null==c.return||c.return()}finally{if(o)throw i}}return n}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()}function f(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}function d(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function y(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function b(e,t){return!t||"object"!==u(t)&&"function"!==typeof t?g(e):t}function m(e){return(m=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function g(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function h(e,t){return(h=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function v(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var w=function(e){function t(){var e,n;d(this,t);for(var r=arguments.length,o=new Array(r),i=0;i<r;i++)o[i]=arguments[i];return v(g(n=b(this,(e=m(t)).call.apply(e,[this].concat(o)))),"state",{isFocused:n.props.autoFocus||!1}),v(g(n),"onFocus",(function(e){n.setState({isFocused:!0}),n.props.onFocus(e)})),v(g(n),"onBlur",(function(e){n.setState({isFocused:!1}),n.props.onBlur(e)})),n}var n,u,w;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&h(e,t)}(t,e),n=t,(u=[{key:"render",value:function(){var e=this.props,t=e.startEnhancer,n=e.endEnhancer,u=e.overrides,d=u.Root,y=u.StartEnhancer,b=u.EndEnhancer,m=f(u,["Root","StartEnhancer","EndEnhancer"]),g=f(e,["startEnhancer","endEnhancer","overrides"]),h=p(Object(o.c)(d,c.d),2),v=h[0],w=h[1],j=p(Object(o.c)(y,c.c),2),x=j[0],S=j[1],E=p(Object(o.c)(b,c.c),2),k=E[0],C=E[1],_=Object(i.a)(this.props,this.state);return r.createElement(v,l({"data-baseweb":"input"},_,w),t&&r.createElement(x,l({},_,S,{$position:s.c.start}),"function"===typeof t?t(_):t),r.createElement(a.a,l({},g,{overrides:m,adjoined:O(t,n),onFocus:this.onFocus,onBlur:this.onBlur})),n&&r.createElement(k,l({},_,C,{$position:s.c.end}),"function"===typeof n?n(_):n))}}])&&y(n.prototype,u),w&&y(n,w),t}(r.Component);function O(e,t){return e&&t?s.a.both:e?s.a.left:t?s.a.right:s.a.none}v(w,"defaultProps",{autoComplete:"on",autoFocus:!1,disabled:!1,name:"",error:!1,onBlur:function(){},onFocus:function(){},overrides:{},required:!1,size:s.d.default,startEnhancer:null,endEnhancer:null}),t.a=w},3836:function(e,t,n){"use strict";n.r(t);var r=n(9),o=n(13),i=n(20),a=n(21),c=n(0),s=n.n(c),u=n(65),l=n(1295),p=n(10),f=n(11),d=n(74),y=n(1509),b=n(1328),m=n(1186),g=n(5),h=n.n(g);var v=h()("div",{target:"e1jwn65y0"})((function(e){return{display:"flex",flexDirection:"row",flexWrap:"nowrap",alignItems:"center",input:{MozAppearance:"textfield","&::-webkit-inner-spin-button, &::-webkit-outer-spin-button":{WebkitAppearance:"none",margin:e.theme.spacing.none}}}}),""),w=h()("div",{target:"e1jwn65y1"})({name:"fjj0yo",styles:"height:49px;display:flex;flex-direction:row;"}),O=h()("button",{target:"e1jwn65y2"})((function(e){var t=e.theme;return{margin:t.spacing.none,border:"none",height:t.sizes.full,display:"flex",cursor:"pointer",alignItems:"center",width:"".concat(45,"px"),justifyContent:"center",transition:"color 300ms, backgroundColor 300ms",backgroundColor:t.colors.lightGray,"&:hover, &:focus":{color:t.colors.white,backgroundColor:t.colors.primary,transition:"none",outline:"none"},"&:active":{outline:"none",border:"none"},"&:last-of-type":{borderTopRightRadius:t.radii.md,borderBottomRightRadius:t.radii.md}}}),""),j=h()("div",{target:"e1jwn65y3"})((function(e){return{marginRight:e.theme.spacing.xs,right:"".concat(90,"px")}}),"");var x=function(e){Object(i.a)(n,e);var t=Object(a.a)(n);function n(e){var o;return Object(r.a)(this,n),(o=t.call(this,e)).inputRef=s.a.createRef(),o.formatValue=function(e){var t=function(e){return null==e||""===e?void 0:e}(o.props.element.format);if(null==t)return e.toString();try{return Object(l.sprintf)(t,e)}catch(n){return Object(p.d)("Error in sprintf(".concat(t,", ").concat(e,"): ").concat(n)),String(e)}},o.isIntData=function(){return o.props.element.dataType===f.k.DataType.INT},o.getMin=function(){return o.props.element.hasMin?o.props.element.min:-1/0},o.getMax=function(){return o.props.element.hasMax?o.props.element.max:1/0},o.getStep=function(){var e=o.props.element.step;return e||(o.isIntData()?1:.01)},o.setWidgetValue=function(e){var t=o.state.value,n=o.props,r=n.element,i=n.widgetMgr,a=o.props.element,c=r.id,s=o.getMin(),u=o.getMax();if(s>t||t>u){var l=o.inputRef.current;l&&l.reportValidity()}else{var p=t||0===t?t:a.default;o.isIntData()?i.setIntValue(c,p,e):i.setFloatValue(c,p,e),o.setState({dirty:!1,value:p,formattedValue:o.formatValue(p)})}},o.onBlur=function(){o.state.dirty&&o.setWidgetValue({fromUi:!0})},o.onChange=function(e){var t=e.target.value,n=null;n=o.isIntData()?parseInt(t,10):parseFloat(t),o.setState({dirty:!0,value:n,formattedValue:t})},o.onKeyDown=function(e){switch(e.key){case"ArrowUp":e.preventDefault(),o.modifyValueUsingStep("increment")();break;case"ArrowDown":e.preventDefault(),o.modifyValueUsingStep("decrement")()}},o.onKeyPress=function(e){"Enter"===e.key&&o.state.dirty&&o.setWidgetValue({fromUi:!0})},o.modifyValueUsingStep=function(e){return function(){var t=o.state.value,n=o.getStep(),r=o.getMin(),i=o.getMax();switch(e){case"increment":t+n<=i&&o.setState({dirty:!0,value:t+n},(function(){o.setWidgetValue({fromUi:!0})}));break;case"decrement":t-n>=r&&o.setState({dirty:!0,value:t-n},(function(){o.setWidgetValue({fromUi:!0})}))}}},o.render=function(){var e=o.props,t=e.element,n=e.width,r=e.disabled,i=o.state,a=i.formattedValue,c=i.dirty,l={width:n};return s.a.createElement("div",{className:"stNumberInput",style:l},s.a.createElement(m.b,null,t.label),s.a.createElement(v,null,s.a.createElement(y.a,{type:"number",inputRef:o.inputRef,value:a,onBlur:o.onBlur,onChange:o.onChange,onKeyPress:o.onKeyPress,onKeyDown:o.onKeyDown,disabled:r,overrides:{Input:{props:{step:o.getStep(),min:o.getMin(),max:o.getMax()}},InputContainer:{style:function(){return{borderTopRightRadius:0,borderBottomRightRadius:0}}}}}),s.a.createElement(w,null,s.a.createElement(O,{className:"step-down",onClick:o.modifyValueUsingStep("decrement")},s.a.createElement(d.a,{content:u.Minus,size:"xs"})),s.a.createElement(O,{className:"step-up",onClick:o.modifyValueUsingStep("increment")},s.a.createElement(d.a,{content:u.Plus,size:"xs"})))),s.a.createElement(j,null,s.a.createElement(b.a,{dirty:c,value:a,className:"input-instructions"})))},o.state={dirty:!1,value:o.initialValue,formattedValue:o.formatValue(o.initialValue)},o}return Object(o.a)(n,[{key:"componentDidMount",value:function(){this.setWidgetValue({fromUi:!1})}},{key:"initialValue",get:function(){var e=this.props.element.id,t=this.props.widgetMgr.getIntValue(e);return void 0!==t?t:this.props.element.default}}]),n}(s.a.PureComponent);n.d(t,"default",(function(){return x}))}}]);
//# sourceMappingURL=18.a0139672.chunk.js.map