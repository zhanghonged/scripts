window.onload=function(){
	var bg = document.getElementById("home");
	var start = document.getElementById("buttonstart");
	//页面透明渐变实现调转
	var homeopacity = 1.0;
	function fadeOut(){
		homeopacity -= 0.02
		if(homeopacity >= 0){
			bg.style.opacity = homeopacity;
		}else{
			//透明后调转到游戏页面
			document.location = "./game.html";
		}
	}
	start.onmouseover = function(){
		start.style.width="340px";
		start.style.cursor="pointer";
	}
	start.onmouseout = function(){
		start.style.width="240px";
	}
	var handle;
	start.onclick = function(){
		
		handle = setInterval(fadeOut,20);
		clearInterval(handle);
	}
}