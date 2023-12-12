"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2268],{3905:function(e,t,r){r.d(t,{Zo:function(){return c},kt:function(){return d}});var n=r(7294);function s(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function o(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){s(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function u(e,t){if(null==e)return{};var r,n,s=function(e,t){if(null==e)return{};var r,n,s={},a=Object.keys(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||(s[r]=e[r]);return s}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(s[r]=e[r])}return s}var i=n.createContext({}),l=function(e){var t=n.useContext(i),r=t;return e&&(r="function"==typeof e?e(t):o(o({},t),e)),r},c=function(e){var t=l(e.components);return n.createElement(i.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},f=n.forwardRef((function(e,t){var r=e.components,s=e.mdxType,a=e.originalType,i=e.parentName,c=u(e,["components","mdxType","originalType","parentName"]),f=l(r),d=s,g=f["".concat(i,".").concat(d)]||f[d]||p[d]||a;return r?n.createElement(g,o(o({ref:t},c),{},{components:r})):n.createElement(g,o({ref:t},c))}));function d(e,t){var r=arguments,s=t&&t.mdxType;if("string"==typeof e||s){var a=r.length,o=new Array(a);o[0]=f;var u={};for(var i in t)hasOwnProperty.call(t,i)&&(u[i]=t[i]);u.originalType=e,u.mdxType="string"==typeof e?e:s,o[1]=u;for(var l=2;l<a;l++)o[l]=r[l];return n.createElement.apply(null,o)}return n.createElement.apply(null,r)}f.displayName="MDXCreateElement"},5899:function(e,t,r){r.r(t),r.d(t,{assets:function(){return c},contentTitle:function(){return i},default:function(){return d},frontMatter:function(){return u},metadata:function(){return l},toc:function(){return p}});var n=r(7462),s=r(3366),a=(r(7294),r(3905)),o=["components"],u={sidebar_label:"settings_store",title:"grants.qt.settings_store"},i=void 0,l={unversionedId:"reference/grants/qt/settings_store",id:"reference/grants/qt/settings_store",title:"grants.qt.settings_store",description:"QtSettingsUserStore Objects",source:"@site/docs/reference/grants/qt/settings_store.md",sourceDirName:"reference/grants/qt",slug:"/reference/grants/qt/settings_store",permalink:"/herre/docs/reference/grants/qt/settings_store",editUrl:"https://github.com/jhnnsrs/turms/edit/master/website/docs/reference/grants/qt/settings_store.md",tags:[],version:"current",frontMatter:{sidebar_label:"settings_store",title:"grants.qt.settings_store"},sidebar:"tutorialSidebar",previous:{title:"errors",permalink:"/herre/docs/reference/grants/qt/errors"},next:{title:"static",permalink:"/herre/docs/reference/grants/static"}},c={},p=[{value:"QtSettingsUserStore Objects",id:"qtsettingsuserstore-objects",level:2},{value:"aput_default_user",id:"aput_default_user",level:4},{value:"Parameters",id:"parameters",level:2},{value:"aget_default_user",id:"aget_default_user",level:4},{value:"Returns",id:"returns",level:2}],f={toc:p};function d(e){var t=e.components,r=(0,s.Z)(e,o);return(0,a.kt)("wrapper",(0,n.Z)({},f,r,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h2",{id:"qtsettingsuserstore-objects"},"QtSettingsUserStore Objects"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"class QtSettingsUserStore(BaseModel)\n")),(0,a.kt)("p",null,"A user store that uses Qt settings to store the use"),(0,a.kt)("h4",{id:"aput_default_user"},"aput","_","default","_","user"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"async def aput_default_user(user: Optional[StoredUser]) -> None\n")),(0,a.kt)("p",null,"Puts the default user"),(0,a.kt)("h2",{id:"parameters"},"Parameters"),(0,a.kt)("p",null,"user : StoredUser | None\nA stored user, with the token and the user, if None is provided\nthe user is deleted"),(0,a.kt)("h4",{id:"aget_default_user"},"aget","_","default","_","user"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"async def aget_default_user() -> Optional[StoredUser]\n")),(0,a.kt)("p",null,"Gets the default user"),(0,a.kt)("h2",{id:"returns"},"Returns"),(0,a.kt)("p",null,"Optional","[StoredUser]","\nA stored user, with the token and the user"))}d.isMDXComponent=!0}}]);