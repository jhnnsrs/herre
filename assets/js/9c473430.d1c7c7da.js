"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5427],{3905:function(e,r,t){t.d(r,{Zo:function(){return c},kt:function(){return f}});var n=t(7294);function a(e,r,t){return r in e?Object.defineProperty(e,r,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[r]=t,e}function u(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function l(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?u(Object(t),!0).forEach((function(r){a(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):u(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}function i(e,r){if(null==e)return{};var t,n,a=function(e,r){if(null==e)return{};var t,n,a={},u=Object.keys(e);for(n=0;n<u.length;n++)t=u[n],r.indexOf(t)>=0||(a[t]=e[t]);return a}(e,r);if(Object.getOwnPropertySymbols){var u=Object.getOwnPropertySymbols(e);for(n=0;n<u.length;n++)t=u[n],r.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var o=n.createContext({}),s=function(e){var r=n.useContext(o),t=r;return e&&(t="function"==typeof e?e(r):l(l({},r),e)),t},c=function(e){var r=s(e.components);return n.createElement(o.Provider,{value:r},e.children)},p={inlineCode:"code",wrapper:function(e){var r=e.children;return n.createElement(n.Fragment,{},r)}},d=n.forwardRef((function(e,r){var t=e.components,a=e.mdxType,u=e.originalType,o=e.parentName,c=i(e,["components","mdxType","originalType","parentName"]),d=s(t),f=a,h=d["".concat(o,".").concat(f)]||d[f]||p[f]||u;return t?n.createElement(h,l(l({ref:r},c),{},{components:t})):n.createElement(h,l({ref:r},c))}));function f(e,r){var t=arguments,a=r&&r.mdxType;if("string"==typeof e||a){var u=t.length,l=new Array(u);l[0]=d;var i={};for(var o in r)hasOwnProperty.call(r,o)&&(i[o]=r[o]);i.originalType=e,i.mdxType="string"==typeof e?e:a,l[1]=i;for(var s=2;s<u;s++)l[s]=t[s];return n.createElement.apply(null,l)}return n.createElement.apply(null,t)}d.displayName="MDXCreateElement"},9075:function(e,r,t){t.r(r),t.d(r,{assets:function(){return c},contentTitle:function(){return o},default:function(){return f},frontMatter:function(){return i},metadata:function(){return s},toc:function(){return p}});var n=t(7462),a=t(3366),u=(t(7294),t(3905)),l=["components"],i={sidebar_label:"utils",title:"grants.oauth2.utils"},o=void 0,s={unversionedId:"reference/grants/oauth2/utils",id:"reference/grants/oauth2/utils",title:"grants.oauth2.utils",description:"build\\authorize\\url",source:"@site/docs/reference/grants/oauth2/utils.md",sourceDirName:"reference/grants/oauth2",slug:"/reference/grants/oauth2/utils",permalink:"/herre/docs/reference/grants/oauth2/utils",editUrl:"https://github.com/jhnnsrs/turms/edit/master/website/docs/reference/grants/oauth2/utils.md",tags:[],version:"current",frontMatter:{sidebar_label:"utils",title:"grants.oauth2.utils"},sidebar:"tutorialSidebar",previous:{title:"refresh",permalink:"/herre/docs/reference/grants/oauth2/refresh"},next:{title:"auto_login",permalink:"/herre/docs/reference/grants/qt/auto_login"}},c={},p=[{value:"build_authorize_url",id:"build_authorize_url",level:4},{value:"Parameters",id:"parameters",level:2},{value:"Returns",id:"returns",level:2},{value:"build_token_url",id:"build_token_url",level:4},{value:"Parameters",id:"parameters-1",level:2},{value:"Returns",id:"returns-1",level:2},{value:"build_refresh_url",id:"build_refresh_url",level:4},{value:"Parameters",id:"parameters-2",level:2},{value:"Returns",id:"returns-2",level:2}],d={toc:p};function f(e){var r=e.components,t=(0,a.Z)(e,l);return(0,u.kt)("wrapper",(0,n.Z)({},d,t,{components:r,mdxType:"MDXLayout"}),(0,u.kt)("h4",{id:"build_authorize_url"},"build","_","authorize","_","url"),(0,u.kt)("pre",null,(0,u.kt)("code",{parentName:"pre",className:"language-python"},"def build_authorize_url(grant: BaseOauth2Grant) -> str\n")),(0,u.kt)("p",null,"Builds the authorize url for the given grant."),(0,u.kt)("h2",{id:"parameters"},"Parameters"),(0,u.kt)("p",null,"grant : BaseOauth2Grant\nA BaseOauth2Grant"),(0,u.kt)("h2",{id:"returns"},"Returns"),(0,u.kt)("p",null,"str\nThe authorize url"),(0,u.kt)("h4",{id:"build_token_url"},"build","_","token","_","url"),(0,u.kt)("pre",null,(0,u.kt)("code",{parentName:"pre",className:"language-python"},"def build_token_url(grant: BaseOauth2Grant) -> str\n")),(0,u.kt)("p",null,"Builds the token url for the given grant."),(0,u.kt)("h2",{id:"parameters-1"},"Parameters"),(0,u.kt)("p",null,"grant : BaseOauth2Grant\nBaseOauth2Grant"),(0,u.kt)("h2",{id:"returns-1"},"Returns"),(0,u.kt)("p",null,"str\nThe token url"),(0,u.kt)("h4",{id:"build_refresh_url"},"build","_","refresh","_","url"),(0,u.kt)("pre",null,(0,u.kt)("code",{parentName:"pre",className:"language-python"},"def build_refresh_url(grant: BaseOauth2Grant) -> str\n")),(0,u.kt)("p",null,"Builds the token url for the given grant."),(0,u.kt)("h2",{id:"parameters-2"},"Parameters"),(0,u.kt)("p",null,"grant : BaseOauth2Grant\nBaseOauth2Grant"),(0,u.kt)("h2",{id:"returns-2"},"Returns"),(0,u.kt)("p",null,"str\nThe token url"))}f.isMDXComponent=!0}}]);