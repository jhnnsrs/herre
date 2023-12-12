"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2935],{3905:function(e,t,r){r.d(t,{Zo:function(){return s},kt:function(){return p}});var n=r(7294);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function c(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var u=n.createContext({}),l=function(e){var t=n.useContext(u),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},s=function(e){var t=l(e.components);return n.createElement(u.Provider,{value:t},e.children)},d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},h=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,u=e.parentName,s=c(e,["components","mdxType","originalType","parentName"]),h=l(r),p=a,f=h["".concat(u,".").concat(p)]||h[p]||d[p]||o;return r?n.createElement(f,i(i({ref:t},s),{},{components:r})):n.createElement(f,i({ref:t},s))}));function p(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=h;var c={};for(var u in t)hasOwnProperty.call(t,u)&&(c[u]=t[u]);c.originalType=e,c.mdxType="string"==typeof e?e:a,i[1]=c;for(var l=2;l<o;l++)i[l]=r[l];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}h.displayName="MDXCreateElement"},9361:function(e,t,r){r.r(t),r.d(t,{assets:function(){return s},contentTitle:function(){return u},default:function(){return p},frontMatter:function(){return c},metadata:function(){return l},toc:function(){return d}});var n=r(7462),a=r(3366),o=(r(7294),r(3905)),i=["components"],c={sidebar_label:"authorization_code",title:"grants.oauth2.authorization_code"},u=void 0,l={unversionedId:"reference/grants/oauth2/authorization_code",id:"reference/grants/oauth2/authorization_code",title:"grants.oauth2.authorization_code",description:"Redirecter Objects",source:"@site/docs/reference/grants/oauth2/authorization_code.md",sourceDirName:"reference/grants/oauth2",slug:"/reference/grants/oauth2/authorization_code",permalink:"/herre/docs/reference/grants/oauth2/authorization_code",editUrl:"https://github.com/jhnnsrs/turms/edit/master/website/docs/reference/grants/oauth2/authorization_code.md",tags:[],version:"current",frontMatter:{sidebar_label:"authorization_code",title:"grants.oauth2.authorization_code"},sidebar:"tutorialSidebar",previous:{title:"cache",permalink:"/herre/docs/reference/grants/meta/cache"},next:{title:"base",permalink:"/herre/docs/reference/grants/oauth2/base"}},s={},d=[{value:"Redirecter Objects",id:"redirecter-objects",level:2},{value:"aget_redirect_uri",id:"aget_redirect_uri",level:4},{value:"astart",id:"astart",level:4},{value:"Parameters",id:"parameters",level:2},{value:"Returns",id:"returns",level:2},{value:"AuthorizationCodeGrant Objects",id:"authorizationcodegrant-objects",level:2},{value:"redirecter",id:"redirecter",level:4},{value:"afetch_token",id:"afetch_token",level:4},{value:"Parameters",id:"parameters-1",level:2},{value:"Returns",id:"returns-1",level:2}],h={toc:d};function p(e){var t=e.components,r=(0,a.Z)(e,i);return(0,o.kt)("wrapper",(0,n.Z)({},h,r,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h2",{id:"redirecter-objects"},"Redirecter Objects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"@runtime_checkable\nclass Redirecter(Protocol)\n")),(0,o.kt)("p",null,"A protocol for a from oauthlib.common import generate_tokenedirect waiter"),(0,o.kt)("h4",{id:"aget_redirect_uri"},"aget","_","redirect","_","uri"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"async def aget_redirect_uri(token_request: TokenRequest) -> str\n")),(0,o.kt)("p",null,"Retrieves the redirect uri"),(0,o.kt)("p",null,"This function will retrieve the redirect uri from the RedirectWaiter.\nThis function has to be implemented by the user."),(0,o.kt)("h4",{id:"astart"},"astart"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"def astart(starturl: str) -> Awaitable[str]\n")),(0,o.kt)("p",null,"Awaits a redirect"),(0,o.kt)("p",null,"This has to be implemented by a user, and should\nreturn the path of the redirect (with the code)"),(0,o.kt)("h2",{id:"parameters"},"Parameters"),(0,o.kt)("p",null,"starturl : str\nThe url to start the redirect from"),(0,o.kt)("h2",{id:"returns"},"Returns"),(0,o.kt)("p",null,"Awaitable","[str]","\nThe path of the redirect (with the code)"),(0,o.kt)("h2",{id:"authorizationcodegrant-objects"},"AuthorizationCodeGrant Objects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"class AuthorizationCodeGrant(BaseOauth2Grant)\n")),(0,o.kt)("p",null,"A grant that uses the authorization code flow"),(0,o.kt)("p",null,"This grant will create an AuthorizationCodeGrant, and use it to fetch a token."),(0,o.kt)("h4",{id:"redirecter"},"redirecter"),(0,o.kt)("p",null,"A simple webserver that will listen for a redirect from the OSF and return the path"),(0,o.kt)("h4",{id:"afetch_token"},"afetch","_","token"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"async def afetch_token(request: TokenRequest) -> Token\n")),(0,o.kt)("p",null,"Fetch Token"),(0,o.kt)("p",null,"This function will fetch a token from the oauth2 provider,\nusing the authorization code flow. It will retrieve the redirect_uri from the redirecter,\nand use that as the redirect_uri, it will then build an authorization url, and delegate the\nredirect to the RedirectWaiter. When the redirecter has received the redirect, it will\nreturn the code to this function, which will then use the code to fetch a token."),(0,o.kt)("h2",{id:"parameters-1"},"Parameters"),(0,o.kt)("p",null,"request : TokenRequest\nThe token request to use"),(0,o.kt)("h2",{id:"returns-1"},"Returns"),(0,o.kt)("p",null,"Token\nThe token"))}p.isMDXComponent=!0}}]);