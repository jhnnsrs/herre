"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2747],{3905:function(e,t,n){n.d(t,{Zo:function(){return u},kt:function(){return d}});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var c=r.createContext({}),i=function(e){var t=r.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},u=function(e){var t=i(e.components);return r.createElement(c.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,c=e.parentName,u=l(e,["components","mdxType","originalType","parentName"]),f=i(n),d=a,b=f["".concat(c,".").concat(d)]||f[d]||p[d]||o;return n?r.createElement(b,s(s({ref:t},u),{},{components:n})):r.createElement(b,s({ref:t},u))}));function d(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,s=new Array(o);s[0]=f;var l={};for(var c in t)hasOwnProperty.call(t,c)&&(l[c]=t[c]);l.originalType=e,l.mdxType="string"==typeof e?e:a,s[1]=l;for(var i=2;i<o;i++)s[i]=n[i];return r.createElement.apply(null,s)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},8674:function(e,t,n){n.r(t),n.d(t,{assets:function(){return u},contentTitle:function(){return c},default:function(){return d},frontMatter:function(){return l},metadata:function(){return i},toc:function(){return p}});var r=n(7462),a=n(3366),o=(n(7294),n(3905)),s=["components"],l={sidebar_label:"base",title:"grants.base"},c=void 0,i={unversionedId:"reference/grants/base",id:"reference/grants/base",title:"grants.base",description:"BaseGrantProtocol Objects",source:"@site/docs/reference/grants/base.md",sourceDirName:"reference/grants",slug:"/reference/grants/base",permalink:"/herre/docs/reference/grants/base",editUrl:"https://github.com/jhnnsrs/turms/edit/master/website/docs/reference/grants/base.md",tags:[],version:"current",frontMatter:{sidebar_label:"base",title:"grants.base"},sidebar:"tutorialSidebar",previous:{title:"auto_login",permalink:"/herre/docs/reference/grants/auto_login"},next:{title:"errors",permalink:"/herre/docs/reference/grants/errors"}},u={},p=[{value:"BaseGrantProtocol Objects",id:"basegrantprotocol-objects",level:2},{value:"afetch_token",id:"afetch_token",level:4},{value:"Parameters",id:"parameters",level:2},{value:"Returns",id:"returns",level:2},{value:"BaseGrant Objects",id:"basegrant-objects",level:2},{value:"afetch_token",id:"afetch_token-1",level:4},{value:"Parameters",id:"parameters-1",level:2},{value:"Returns",id:"returns-1",level:2},{value:"Config Objects",id:"config-objects",level:2}],f={toc:p};function d(e){var t=e.components,n=(0,a.Z)(e,s);return(0,o.kt)("wrapper",(0,r.Z)({},f,n,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h2",{id:"basegrantprotocol-objects"},"BaseGrantProtocol Objects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"@runtime_checkable\nclass BaseGrantProtocol(Protocol)\n")),(0,o.kt)("p",null,"The base grant protocol"),(0,o.kt)("p",null,"This protocol is implemented by all grants.\nIt can be used to type hint a grant."),(0,o.kt)("h4",{id:"afetch_token"},"afetch","_","token"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"async def afetch_token(request: TokenRequest) -> Token\n")),(0,o.kt)("p",null,"Fetches a token"),(0,o.kt)("p",null,"This function will fetch a token from the grant.\nThis function is async, and should be awaited"),(0,o.kt)("h2",{id:"parameters"},"Parameters"),(0,o.kt)("p",null,"request : TokenRequest\nThe token request to use"),(0,o.kt)("h2",{id:"returns"},"Returns"),(0,o.kt)("p",null,"Token\nThe token"),(0,o.kt)("h2",{id:"basegrant-objects"},"BaseGrant Objects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"class BaseGrant(BaseModel)\n")),(0,o.kt)("p",null,"The base grant class"),(0,o.kt)("p",null,"This class is the base class for all grants.\nIt is a pydantic model, and can be used as such.\nIt also implements the BaseGrantProtocol, which can be used to type hint\na grant."),(0,o.kt)("h4",{id:"afetch_token-1"},"afetch","_","token"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"@abstractmethod\nasync def afetch_token(request: TokenRequest) -> Token\n")),(0,o.kt)("p",null,"Fetches a token"),(0,o.kt)("p",null,"This function will fetch a token from the grant.\nThis function is async, and should be awaited"),(0,o.kt)("h2",{id:"parameters-1"},"Parameters"),(0,o.kt)("p",null,"request : TokenRequest\nThe token request to use"),(0,o.kt)("h2",{id:"returns-1"},"Returns"),(0,o.kt)("p",null,"Token\nThe token"),(0,o.kt)("h2",{id:"config-objects"},"Config Objects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"class Config()\n")),(0,o.kt)("p",null,"Config for the base grant"))}d.isMDXComponent=!0}}]);