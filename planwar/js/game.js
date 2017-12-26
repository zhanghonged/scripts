window.onload=function(){

	//发射子弹函数
	function doFire(x,y){
		for(var i=0;i<10;i++){
			var eshot = document.getElementById("eshot"+i);
			if(eshot.style.display == "none"){
				eshot.style.left = x + "px";
				eshot.style.top = y + "px";
				eshot.style.display = "block";
				return;
			}
		}
	}

	//敌机出现函数
	function doShow(){
		//随机出现0-5间的数字，获取img上面的敌机标签
		var i = Math.ceil(Math.random()*10000)%6;
		var ee = document.getElementById("e" + i);
		if(ee.style.display == "none"){
			ee.style.top = 0 + "px";
			//随机出现0-1100之间的数字，使敌机在地图顶端随机出现
			ee.style.left = Math.ceil(Math.random()*10000)%1100 + "px";
			ee.style.display = "block";
		}
		setTimeout(doShow,2000);
	}

	//敌机移动函数
	function ee_move(){
		for(var i=0;i<6;i++){
			var ee = document.getElementById("e"+i);
			if(ee.style.display == "block"){
				ee.style.top = ee.offsetTop + 5 + "px";
			}
			//offsetTop大于835像素，将飞出地图下面，将敌机回收
			if(ee.offsetTop > 835){
				ee.style.display = "none";
			}
		}
		setTimeout(ee_move,30);
	}

	//碰撞检测函数
	function doCheck(eshot){
		//循环遍历所有敌机
		for(var i=0;i<6;i++){
			var ee = document.getElementById("e"+i);
			if(ee.style.display == "block"){
				//敌机的坐标
				ex = ee.offsetLeft;
				ey = ee.offsetTop;
				//子弹当前坐标
				sx = eshot.offsetLeft;
				sy = eshot.offsetTop;

				//判断敌机与子弹是否坐标位置相交
				//1.子弹的sy小于敌机的ey
				//2.子弹的sx大于敌机的ex
				//3.子弹的sx小于敌机的ex+115，115是敌机的宽度
				if(sy < ey &&  sx > ex && sx < (ex+115)){
					//位置相交后把敌机和子弹都回收
					eshot.style.display = "none";
					ee.style.display = "none";
					//在位置相交处显示爆炸效果
					var pp = document.createElement("img");
					pp.src = "./images/boom.gif";
					pp.style.position="absolute";
					//130、190是爆炸效果图的宽高各一半，为使爆炸效果显示在中央
					pp.style.top = (sy - 130) + "px";
					pp.style.left = (sx - 190) + "px";
					//给爆炸效果添加num属性，设置值为0,为后面回收时使用
					pp.num = 0;
					//把这次爆炸添加到pplist
					pplist.push(pp);
					//显示爆炸效果
					gamebg.appendChild(pp);

				}
			}
		}
	}

	//子弹移动函数
	function eshot_move(){
		for(var i=0;i<10;i++){
			var eshot = document.getElementById("eshot"+i);
			//若子弹已经发射出，向上移动5个像素
			if(eshot.style.display == "block"){
				eshot.style.top = (eshot.offsetTop - 5) + "px";
				//检查碰撞
				doCheck(eshot);
			}

			//子弹飞出屏幕区域，回收子弹
			if(eshot.offsetTop < -20){
				eshot.style.display = "none";
			}
		}
		setTimeout(eshot_move,10);
	}


	//爆炸效果回收函数
	function pp_remove(){
		for(var i=0;i<pplist.length;i++){
			pplist[i].num ++;
			if(pplist[i].num > 5){
				pplist[i].style.display = "none";
				pplist.splice(i,1);
			}
		}
		setTimeout(pp_remove,30);
	}


	//飞机移动及发射子弹函数
	var myplan = document.getElementById("myplan")
	window.document.onkeydown = function(evt){
		//兼容w3c和IE
		var event = evt || window.event;
		// alert(event.keyCode);
		//获取键盘值
		switch(event.keyCode){
			// w和方向上
			case 87:
			case 38:
				myplan.style.top = Math.max(0,myplan.offsetTop - 10) + "px";
			break;
			// s和方向下
			case 83:
			case 40:
				myplan.style.top = Math.min(830,myplan.offsetTop + 10) + "px";
			break;
			// a和方向左
			case 65:
			case 37:
				myplan.style.left = Math.max(0,myplan.offsetLeft - 10) + "px";
			break;
			// d和方向右
			case 68:
			case 39:
				myplan.style.left = Math.min(1092,myplan.offsetLeft + 10) + "px";
			break;
			//空格发送子弹
			case 32:
				var x = myplan.offsetLeft + 52;
				var y = myplan.offsetTop;
				doFire(x,y);
		}
	}


	//背景图滚动
	var gamebg = document.getElementById("gamebg");
	var bg_m = -2344;
	setInterval(function(){
		bg_m += 2;
		if(bg_m > -1){
			bg_m = -2344;
		}
		gamebg.style.backgroundPosition = "0px " + bg_m + "px";
	},50)
	
	//初始化爆炸效果存放数组
	var pplist=[];

	doShow();
	ee_move();
	eshot_move();
	pp_remove();

}
