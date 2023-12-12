"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7737],{3905:function(e,t,r){r.d(t,{Zo:function(){return u},kt:function(){return f}});var n=r(7294);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function i(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function a(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?i(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function c(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},i=Object.keys(e);for(n=0;n<i.length;n++)r=i[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)r=i[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var l=n.createContext({}),s=function(e){var t=n.useContext(l),r=t;return e&&(r="function"==typeof e?e(t):a(a({},t),e)),r},u=function(e){var t=s(e.components);return n.createElement(l.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var r=e.components,o=e.mdxType,i=e.originalType,l=e.parentName,u=c(e,["components","mdxType","originalType","parentName"]),d=s(r),f=o,b=d["".concat(l,".").concat(f)]||d[f]||p[f]||i;return r?n.createElement(b,a(a({ref:t},u),{},{components:r})):n.createElement(b,a({ref:t},u))}));function f(e,t){var r=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=r.length,a=new Array(i);a[0]=d;var c={};for(var l in t)hasOwnProperty.call(t,l)&&(c[l]=t[l]);c.originalType=e,c.mdxType="string"==typeof e?e:o,a[1]=c;for(var s=2;s<i;s++)a[s]=r[s];return n.createElement.apply(null,a)}return n.createElement.apply(null,r)}d.displayName="MDXCreateElement"},726:function(e,t,r){r.r(t),r.d(t,{assets:function(){return u},contentTitle:function(){return l},default:function(){return f},frontMatter:function(){return c},metadata:function(){return s},toc:function(){return p}});var n=r(7462),o=r(3366),i=(r(7294),r(3905)),a=["components"],c={sidebar_label:"builders",title:"builders"},l=void 0,s={unversionedId:"reference/builders",id:"reference/builders",title:"builders",description:"github\\_desktop",source:"@site/docs/reference/builders.md",sourceDirName:"reference",slug:"/reference/builders",permalink:"/herre/docs/reference/builders",editUrl:"https://github.com/jhnnsrs/turms/edit/master/website/docs/reference/builders.md",tags:[],version:"current",frontMatter:{sidebar_label:"builders",title:"builders"},sidebar:"tutorialSidebar",previous:{title:"Introduction",permalink:"/herre/docs/intro"},next:{title:"errors",permalink:"/herre/docs/reference/errors"}},u={},p=[{value:"github_desktop",id:"github_desktop",level:4},{value:"Parameters",id:"parameters",level:2},{value:"Returns",id:"returns",level:2}],d={toc:p};function f(e){var t=e.components,r=(0,o.Z)(e,a);return(0,i.kt)("wrapper",(0,n.Z)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("h4",{id:"github_desktop"},"github","_","desktop"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def github_desktop(client_id: str,\n                   client_secret: str,\n                   scopes: Optional[List[str]] = None) -> Herre\n")),(0,i.kt)("p",null,"Creates a Herre instance that can be used to login locally to github"),(0,i.kt)("p",null,"This function will create a Herre instance that can be used to login locally to github.\nIt will use the authorization code grant, and a aiohttp server redirecter."),(0,i.kt)("h2",{id:"parameters"},"Parameters"),(0,i.kt)("p",null,"client_id : str\nThe client id to use\nclient_secret : str\nThe client secret to use\nscopes : Optional[List","[str]","], optional\nThe scopes to use, by default None"),(0,i.kt)("h2",{id:"returns"},"Returns"),(0,i.kt)("p",null,"Herre\nThe Herre instance"))}f.isMDXComponent=!0}}]);