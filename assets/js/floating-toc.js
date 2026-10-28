/* Accessible floating section navigator for all project detail pages. */
(function(){
  "use strict";
  function init(){
    var main=document.querySelector("main.shell")||document.querySelector("main");
    if(!main||document.querySelector(".floating-toc"))return;
    var sections=Array.prototype.slice.call(main.querySelectorAll(".body > section")).filter(function(el){
      return !!el.querySelector("h2");
    });
    if(sections.length<2)return;
    var labels={
      "game":"게임 정보","game-spotlight":"게임 카탈로그",
      "features":"한국어화","scope":"한국어화","patch":"한국어화",
      "progress":"검수 현황","status":"검수 현황",
      "changelog":"업데이트 내역","source":"원본 파일","original":"원본 파일","hash":"원본·해시",
      "release":"패치 다운로드","download":"패치 다운로드",
      "install":"적용 방법","credits":"제작·검수","patch-warning":"주의 사항",
      "notice":"이용 고지","legal":"이용 고지"
    };
    var aside=document.createElement("aside");
    aside.className="floating-toc";
    aside.setAttribute("aria-label","페이지 빠른 이동");
    aside.innerHTML='<button class="floating-toc-trigger" type="button" aria-expanded="false" aria-controls="floating-toc-panel">목차</button>'+
      '<div class="floating-toc-panel" id="floating-toc-panel"><div class="floating-toc-title">페이지 목차</div>'+
      '<nav class="floating-toc-list" aria-label="상세 페이지 목차"></nav>'+
      '<div class="floating-toc-bottom"><button class="floating-toc-top" type="button">↑ 맨 위로</button></div></div>';
    var list=aside.querySelector(".floating-toc-list");
    var trigger=aside.querySelector(".floating-toc-trigger");
    var items=[];
    var autoNum=0;
    sections.forEach(function(section){
      var heading=section.querySelector("h2");
      if(!section.id){
        do{autoNum+=1;section.id="page-toc-section-"+autoNum;}
        while(document.querySelectorAll('[id="'+section.id+'"]').length>1);
      }
      var title=labels[section.id]||heading.textContent.trim().replace(/\s+/g," ");
      if(!labels[section.id]){
        if(/한국어화|패치 주요/.test(title))title="한국어화";
        else if(/제작|테스트/.test(title))title="제작·검수";
        else if(/패치 정보/.test(title))title="검수 현황";
        else if(/패치 파일|다운로드/.test(title))title="패치 다운로드";
      }
      var anchor=document.createElement("a");
      anchor.href="#"+section.id;
      anchor.textContent=title;
      anchor.setAttribute("aria-label",title+"로 이동");
      list.appendChild(anchor);
      items.push({section:section,link:anchor});
    });
    document.body.appendChild(aside);
    function closeMenu(returnFocus){
      var opened=aside.classList.contains("is-open");
      aside.classList.remove("is-open");
      trigger.setAttribute("aria-expanded","false");
      if(returnFocus&&opened)trigger.focus();
    }
    trigger.addEventListener("click",function(){
      var open=!aside.classList.contains("is-open");
      aside.classList.toggle("is-open",open);
      trigger.setAttribute("aria-expanded",String(open));
    });
    list.addEventListener("click",function(event){
      if(event.target.closest("a"))closeMenu(false);
    });
    aside.querySelector(".floating-toc-top").addEventListener("click",function(){
      closeMenu(false);
      window.scrollTo({top:0,behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
    });
    document.addEventListener("pointerdown",function(event){
      if(aside.classList.contains("is-open")&&!aside.contains(event.target))closeMenu(false);
    });
    document.addEventListener("keydown",function(event){
      if(event.key==="Escape"&&aside.classList.contains("is-open"))closeMenu(true);
    });
    var ticking=false;
    function markActive(){
      ticking=false;
      var current=items[0];
      items.forEach(function(item){
        if(item.section.getBoundingClientRect().top<=140)current=item;
      });
      items.forEach(function(item){
        if(item===current){item.link.setAttribute("aria-current","location");}
        else{item.link.removeAttribute("aria-current");}
      });
    }
    function schedule(){
      if(!ticking){ticking=true;window.requestAnimationFrame(markActive);}
    }
    window.addEventListener("scroll",schedule,{passive:true});
    window.addEventListener("resize",function(){closeMenu(false);schedule();},{passive:true});
    window.addEventListener("hashchange",schedule);
    markActive();
  }
  if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",init,{once:true});}
  else{init();}
})();
