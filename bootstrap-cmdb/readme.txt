响应式布局之媒体查询@media

CSS媒体查询允许我们根据设备的特性来应用不同的样式申明。如，我们可以让 768px 宽度的设备(ipad) 及以上屏幕内容显示4列，768px 以下的显示 1列。

语法：
以@media开头来表示这是一条媒体查询语句。@media后面的是一个或者多个表达式，如果表达式为真，则应用样式。如
@media (max-width: 600px) {
  .facet_sidebar {
    display: none;
  }
}
上面的代码在屏幕宽度小于 600px 的时候，会作用大括号里的内容。

媒体查询可以在 link标签上加media属性或css文件中使用。

<!-- link元素中的CSS媒体查询 屏幕宽度小于800px时应用example.css样式表-->
<link rel="stylesheet" media="(max-width: 800px)" href="example.css" />

<!-- 样式表中的CSS媒体查询 -->
<style>
@media (max-width: 600px) {
  .facet_sidebar {
    display: none;
  }
}
</style>

max与min
他们是要配合支持它们的属性使用的,如：
max-width:600px  表示最大600px，就是应用于小于600px的情况。
min-width:1204px 表示最小1024px，就是应用于大于1024px的情况。

一般情况下手机和平板的大小设置。
@media(max-width:768px){/*平板小于768px*/
	.lengc-text{
	font-size:20px;  
	}
}
@media(max-width:400px){/*手机小于400px*/
	.lengc-text{
	font-size:15px;  
	}
}
