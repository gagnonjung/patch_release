/* Lazy, muted gameplay videos from the verified World of Longplays YouTube channel. */
(function(){
"use strict";
var videos={
 "seireki-1999":{id:"aWkCqSFbtTI",start:435,player:"MadMatty"},
 "taromaru":{id:"EH_Nb78Yvog",start:120,player:"SCHLAUCHI"},
 "zelda-oot":{id:"mF9CxAulk04",start:600,player:"RickyC"},
 "zelda-mm":{id:"_9Kw6AfaZ2s",start:420,player:"Spazbo4"},
 "zelda-ura":{id:"VHFvrKkX_E8",start:750,player:"Spazbo4"},
 "mgs-tts":{id:"d2vcI5m2nBI",start:420,player:"Spazbo4"}
};
function ready(){
 var body=document.body, slug=body&&body.getAttribute("data-game-theme"),video=videos[slug];
 if(!video)return;
 var hero=document.querySelector("main.shell .hero-banner");
 if(!hero||hero.querySelector(".game-video-layer"))return;
 var layer=document.createElement("div");layer.className="game-video-layer";layer.setAttribute("aria-hidden","true");
 var ui=document.createElement("div");ui.className="game-video-ui";
 var toggle=document.createElement("button");toggle.type="button";toggle.className="game-video-toggle";
 var link=document.createElement("a");link.className="game-video-source";
 link.href="https://www.youtube.com/watch?v="+video.id;
 link.target="_blank";link.rel="noopener noreferrer";
 link.textContent="원작 플레이 · World of Longplays / "+video.player+" ↗";
 link.setAttribute("aria-label","원본 게임 플레이 영상, 유튜브에서 시청");
 ui.appendChild(toggle);ui.appendChild(link);
 hero.classList.add("has-game-video");hero.insertBefore(layer,hero.firstChild);hero.appendChild(ui);
 var reduced=window.matchMedia("(prefers-reduced-motion: reduce)");
 var saveData=!!(navigator.connection&&navigator.connection.saveData);
 var enabled=!reduced.matches&&!saveData;
 var visible=true;
 var frame=null;
 function unload(){if(frame){frame.remove();frame=null;}}
 function resize(){
  if(!frame)return;
  var rect=layer.getBoundingClientRect();
  var w=Math.max(rect.width,rect.height*16/9);
  var h=w*9/16;
  frame.style.width=Math.ceil(w)+"px";frame.style.height=Math.ceil(h)+"px";
 }
 function synchronize(){
  toggle.textContent=enabled?"영상 끄기":"영상 켜기";
  toggle.setAttribute("aria-pressed",String(enabled));
  if(!enabled||!visible){unload();return;}
  if(!frame){
    frame=document.createElement("iframe");
    frame.title="World of Longplays 원본 게임 플레이 영상 (음소거)";
    frame.tabIndex=-1;
    frame.setAttribute("allow","autoplay; encrypted-media; picture-in-picture");
    frame.setAttribute("referrerpolicy","strict-origin-when-cross-origin");
    frame.setAttribute("loading","lazy");
    frame.src="https://www.youtube-nocookie.com/embed/"+video.id+"?autoplay=1&mute=1&loop=1&playlist="+video.id+"&controls=0&playsinline=1&rel=0&start="+video.start;
    layer.appendChild(frame);
  }
  resize();
 }
 toggle.addEventListener("click",function(){enabled=!enabled;synchronize();});
 if("IntersectionObserver" in window){
  var observer=new IntersectionObserver(function(entries){visible=entries[0].isIntersecting;synchronize();},{threshold:0.03});
  observer.observe(hero);
 }
 var resizer;
 window.addEventListener("resize",function(){if(resizer)cancelAnimationFrame(resizer);resizer=requestAnimationFrame(resize);},{passive:true});
 document.addEventListener("visibilitychange",function(){if(document.hidden){unload();}else{synchronize();}});
 if(reduced.addEventListener){reduced.addEventListener("change",function(event){if(event.matches){enabled=false;synchronize();}});}
 synchronize();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",ready,{once:true});else ready();
})();
