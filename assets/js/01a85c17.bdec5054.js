"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[13],{8665:function(e,t,a){a.d(t,{Z:function(){return p}});var r=a(3366),l=a(7294),n=a(6010),c=a(2600),s=a(9960),i="sidebar_a9qW",m="sidebarItemTitle_uKok",o="sidebarItemList_Kvuv",u="sidebarItem_CF0Q",d="sidebarItemLink_miNk",b="sidebarItemLinkActive_RRTD",g=a(5999);function E(e){var t=e.sidebar;return 0===t.items.length?null:l.createElement("nav",{className:(0,n.Z)(i,"thin-scrollbar"),"aria-label":(0,g.I)({id:"theme.blog.sidebar.navAriaLabel",message:"Blog recent posts navigation",description:"The ARIA label for recent posts in the blog sidebar"})},l.createElement("div",{className:(0,n.Z)(m,"margin-bottom--md")},t.title),l.createElement("ul",{className:o},t.items.map((function(e){return l.createElement("li",{key:e.permalink,className:u},l.createElement(s.Z,{isNavLink:!0,to:e.permalink,className:d,activeClassName:b},e.title))}))))}var v=["sidebar","toc","children"];function p(e){var t=e.sidebar,a=e.toc,s=e.children,i=(0,r.Z)(e,v),m=t&&t.items.length>0;return l.createElement(c.Z,i,l.createElement("div",{className:"container margin-vert--lg"},l.createElement("div",{className:"row"},m&&l.createElement("aside",{className:"col col--3"},l.createElement(E,{sidebar:t})),l.createElement("main",{className:(0,n.Z)("col",{"col--7":m,"col--9 col--offset-1":!m}),itemScope:!0,itemType:"http://schema.org/Blog"},s),a&&l.createElement("div",{className:"col col--2"},a))))}},497:function(e,t,a){a.r(t),a.d(t,{default:function(){return d}});var r=a(7294),l=a(8665),n=a(7774),c=a(5979),s="tag_Shcx";function i(e){var t=e.letterEntry;return r.createElement("article",null,r.createElement("h2",null,t.letter),r.createElement("ul",{className:"padding--none"},t.tags.map((function(e){return r.createElement("li",{key:e.permalink,className:s},r.createElement(n.Z,e))}))),r.createElement("hr",null))}function m(e){var t=e.tags,a=(0,c.PZ)(t);return r.createElement("section",{className:"margin-vert--lg"},a.map((function(e){return r.createElement(i,{key:e.letter,letterEntry:e})})))}var o=a(4739),u=a(6010);function d(e){var t=e.tags,a=e.sidebar,n=(0,c.MA)();return r.createElement(c.FG,{className:(0,u.Z)(c.kM.wrapper.blogPages,c.kM.page.blogTagsListPage)},r.createElement(c.d,{title:n}),r.createElement(o.Z,{tag:"blog_tags_list"}),r.createElement(l.Z,{sidebar:a},r.createElement("h1",null,n),r.createElement(m,{tags:Object.values(t)})))}}}]);