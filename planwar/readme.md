## 系统包括以下模块

![image](https://github.com/zhanghonged/scripts/blob/master/planwar/images/modul.jpg)
1、<b>背景图移动</b><br>
2、<b>键盘操作响应</b>

- <b>上下左右位置移动</b>
- <b>空格键发送子弹</b>

3、<b>敌机出现</b><br>
4、<b>敌机移动</b><br>
5、<b>子弹移动</b>

- <b>碰撞检测</b>
- <b>爆炸效果产生</b>

6、<b>爆炸效果移除</b>

## 各模块具体实现方法

### 一、背景图移动步骤
![image](https://github.com/zhanghonged/scripts/blob/master/planwar/images/mapmove.jpg)

### 二、键盘操作步骤
`使用 window.document.onkeydown 监控键盘动作。`<br>
1、方向键控制飞机上、下、左、右移动。<br>
2、空格键发射子弹 (doFire方法)。

### 三、子弹发射步骤
1、在主 `div` 内添加 `img` 标签，数量若干个，个数就是可以发射的子弹数。并设置默认样式：`style="display:none;position:absolute"`，默认不可见，具有绝对定位属性。<br>
2、获取飞机的当前位置 `x = player.offsetLeft+52;  y = player.offsetTop;`, 其中52为飞机的宽度的一半。<br>
3、循环遍历所有子弹 `img` 标签，通过 `id`获取子弹对象，对 `display` 属性为 `none` 的子弹进行后续处理。<br>
4、子弹的 `left` 属性为第2步获取的当前飞机的的 `x`。<br>
4、子弹的 `top` 属性为第2步获取的当前飞机的 `y`。<br>
5、将此子弹对象的 `display` 属性设置为 `block`，变成可见显示。

### 四、敌机随机出现步骤
1、在主 `div` 内添加 `img` 标签，数量若干个，个数就是敌机的数量。并设置默认样式：`style="position:absolute;display:none`，默认不可见，具有绝对定位属性。<br>
2、我们这里6架敌机，使用随机0-5之间的数字，获得6架敌机中的某一架。通过 `Math.ceil(Math.random()*10000)%6;` 实现0-5间数字的循环。<br>
3、通过`document.getElementById`取出上一步骤随机出的敌机。<br>
4、判断敌机的`display`属性，如果是`none`属性，则继续往下走，如果是`block`则忽略。<br>
5、设置此敌机的`top`样式属性为地图顶端像素位置。<br>
6、设置此敌机的`left`样式属性为地图宽度范围内随机。例如通过`Math.ceil(Math.random()*10000)%396)+"px";`实现，在0-396像素内去随机数。<br>
7、设置此敌机的`display`属性为`block`，使敌机出现。


### 五、敌机移动步骤
1、通过循环遍历所有敌机，数量为`img`标签里定义的数量。<br>
2、通过`document.getElementById`获取到敌机。<br>
3、通过检测`display`属性是否为`block`获取可见敌机。<br>
4、将敌机的`top`样式属性增加5像素。`style.top=offsetTop +5;`<br>
5、将飞出地图的敌机回收，`display`属性修改为`block`。

### 六、子弹移动步骤
1、通过循环遍历所有子弹，使用`document.getElementById`获取到子弹元素，主`div`里定义了多少`img`子弹标签就循环多少次。<br>
2、通过检测`display`属性是否为`block`,判断子弹是否可见。<br>
3、将子弹的`top`样式属性减少`5px`像素，使子弹向上移动。<br>
4、检测是否子弹和敌机碰撞，通过`dochek()`方法实现。<br>
5、判断子弹的`offsetTop`属性是否小于`-20px`，如果小于`-20px`就是飞出地图了，将`display`属性设为`block`进行回收。

### 七、碰撞检测步骤
`碰撞检测是针对子弹操作的，对某一个子弹进行碰撞检测`。<br>
1、通过循环遍历所有敌机，使用`document.getElementById`获取敌机，主`div`里定义了多少敌机`img`标签就循环多少次。<br>
3、通过检测`display`属性是否为`block`检测敌机是否可见，对可见的敌机进行后续操作。<br>
4、获取敌机和子弹位置:<br>
  敌机的x位置:`ex = offsetLeft`<br>
  敌机的y位置:`ey = offsetTop`<br>
  子弹的x位置:`sx = offsetLeft`<br>
  子弹的y位置:`sy = offsetTop`<br>

5、判断子弹和敌机位置是否相交，需满足已下3个条件：<br>
   a. `ey > sy` 敌机的`ey`大于子弹`sy`,飞机比子弹位置低。<br>
   b. `sx > ex` 子弹的`sx`大于飞机的`ex`，子弹的横向位置大于飞机的最左边横向位置。<br>
   c. `sx < ex+115` 子弹的`sx`小于飞机的`ex+115`，子弹的横向位置小于飞机最右边的位置，`115`是飞机的宽度。<br>

6、如果敌机和子弹位置相交，将相交的飞机和子弹都回收，`diskply`属性设置为`none`。<br>
7、在发生碰撞的位置产生碰撞效果:<br>
   a. 定义爆炸在`html`中的`img`标签元素。`var pp = document.createElement("img");`<br> 
   b. 给此元素设置src属性。`pp.src="xxx";`<br>
   c. 为此`img`标签添加绝对定位属性。 `pp.style.position="absolute";`<br>
   d. 设置爆炸`img`的位置,就是敌机和子弹相交处的位置。为了爆炸显示在中间，分别减去爆炸效果图片的一半高度和宽度。<br>

8、定义此次爆炸效果的`num`属性为`0`。`pp.num = 0;`<br>
9、将这次爆炸添加到前面定义的爆炸数组里。`pplist.push(pp);`<br>
10、让爆炸效果在页面里显示出来。 `game.appendChild(pp);`


### 八、爆炸效果回收实路：
1、通过循环遍历爆炸效果数组`pplist`，遍历所有爆炸效果。<br>
2、将爆炸效果的`num`属性自加`1`。`pplist[i].num++;`<br>
3、进行判断，如果此爆炸效果的`num > 5`，则设置`display`属性设置为`none`将此效果回收。<br>
4、在`pplist`里删除此爆炸效果。`pplist.splice(i,1);`
