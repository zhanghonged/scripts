## 系统包括以下模块

![image](https://github.com/zhanghonged/scripts/blob/master/planwar/images/modul.jpg)
1、<b>背景图移动</b>
2、<b>键盘操作响应</b>

- <b>上下左右位置移动</b>
- <b>空格键发送子弹</b>

3、<b>敌机出现</b>
4、<b>敌机移动</b>
5、<b>子弹移动</b>

- <b>碰撞检测</b>
- <b>爆炸效果产生</b>

6、<b>爆炸效果移除</b>







### 背景图移动思路
![image](https://github.com/zhanghonged/scripts/blob/master/planwar/images/mapmove.jpg)

### 键盘操作思路
1、使用**window.document.onkeydown**监控键盘动作。
2、按键控制飞机上、下、左、右移动包括：

    - 上、下、左、右 移动控制
    - 按空格键发射子弹 (doFire方法)

### 子弹发射思路
1、在主 <div> 内添加 <img> 标签，数量若干个，个数就是可以发射的子弹数。并设置默认样式：style="display:none;position:absolute"，默认不可见，具有绝对定位属性。
2、获取飞机的当前位置 x = player.offsetLeft+52;  y = player.offsetTop; 其中52为飞机的宽度的一半。
3、js里面循环通过id获取子弹对象eshot，对样式为style.display == "none"的eshot进行处理。
4、子弹的left样式为第2步获取的当前飞机的的x。
4、子弹的top样式为第2步获取的当前飞机的y。
5、将此子弹对象的display属性设置为block，变成可见显示。

### 敌机循环随机出现实路
1、在主 <div> 内添加 <img> 标签，数量若干个，个数就是敌机的数量。并设置默认样式：style="position:absolute;display:none"，默认不可见，具有绝对定位属性。
2、如果添加6架敌机，就循环0-5之间的数字，每次出现0-5中的第几家敌机。通过 Math.ceil(Math.random()*10000)%6; 实现0-5间数字的循环。
3、通过document.getElementById取出上一步骤循环得到的敌机。
4、判断敌机的display属性，如果是"none"属性，则继续往下走，如果是"block"忽略。
5、设置此敌机的top样式为地图顶端像素位置。
6、设置此敌机的left属性为地图宽度范围内随机。例如通过Math.ceil(Math.random()*10000)%396)+"px";实现，在0-396像素内去随机数。
7、设置此敌机的display属性为"display"。使敌机出现。


### 敌机移动思路
1、循环所有敌机，数量为img标签里定义的数量。
2、通过document.getElementById获取到敌机。
3、判断敌机是否可见，获取可见敌机。通过检测display属性是否为“block”。
4、将敌机的top属性+5像素，style.top=offsetTop +5
5、将飞出地图的敌机回收，display属性设置为“block”。

### 子弹移动的实路
1、循环所有子弹，通过document.getElementById获取到子弹元素，主<div>里定义了多少<img>子弹标签就循环多少次。
2、判断子弹是否可见，通过检测display属性是否为“block”。
3、将子弹的offsetTop样式减少5px像素。实现向上移动。
4、检测是否子弹和敌机碰撞，通过dochek()方法实现。
5、判断子弹的offsetTop属性是否 小于 -20，如果小于-20就是飞出地图了，将display属性设为“block”进行回收。

### 碰撞检测思路
1、碰撞检测是针对子弹操作的，对某一个子弹进行碰撞检测。
2、循环遍历所有敌机，通过document.getElementById获取到敌机元素，主<div>里定义了多少<img>敌机标签就循环多少次。
3、判断敌机是否可见，通过检测display属性是否为“block”。对可见的敌机进行后续操作。
4、获取子弹和敌机位置。

   - 飞机的x位置，ex = offsetLeft
   - 飞机的y位置，ey = offsetTop
   - 子弹的x位置，px = offsetLeft
   - 子弹的y位置，py = offsetTop

5、判断子弹和敌机位置是否相交。

   - py < ey 飞机的ey大于子弹py,飞机比子弹位置低。
   - px > ex 子弹的px大于飞机的ex，子弹的横向位置大于飞机的横向位置。
   - px < ex+115 子弹的px小于飞机的ex+115，子弹的横向位置小于飞机最右边的位置。飞机的宽度为115。

6、如果位置相交，则将相交的飞机和子弹都回收，diskply属性设置为“none”。
7、在发生碰撞的位置产生碰撞效果。

   - 定义爆炸在html中的<img>标签元素。var pp = document.createElement("img"); pp.src="xxx";
   - 为此<img>标签添加绝对定位属性。 pp.style.position="absolute";
   - 设置爆炸<img>的位置：为了爆炸显示在中间，分别减去爆炸效果图片的一半高度和宽度。

8、定义此次爆炸效果的num属性为0，pp.num = 0;
9、将这次爆炸添加到前面定义的爆炸数组里。
10、让爆炸效果在页面里显示出来。 game.appendChild(pp);


### 爆炸效果回收实路：
1、循环爆炸效果数组，遍历所有爆炸效果。
2、将爆炸效果的num属性自加1，pplist[i].num++
3、进行if判断，如果此爆炸效果的num属性大于5，则将此效果回收，display属性设置为“none”
4、在pplist里删除此爆炸效果pplist.splice(i,1).


游戏流程
1、按键控制飞机上、下、左、右移动 (window.document.onkeydown)，包括：
    a、上、下、左、右 移动控制
    b、按空格键发射子弹 (doFire方法)
2、实现敌机的循环出现，随机位置出现。定义（doShow方法），并通过setTimeout方法循环执行。

3、开始游戏主线程。通过setTimeout方法进行循环执行。
   a、循环获取所有可见子弹，使移动子弹向上移动，并检测是否碰撞到敌机，碰撞后产生效果图，并使飞出屏幕的子弹变为不可见，实现回收。
   b、循环所有可见敌机进行移动，并将飞出屏幕的飞机进行回收。
   c、循环所有可见的碰撞效果图，将碰撞产生的爆炸效果进行回收。