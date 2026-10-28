/* Click-to-enlarge image modal for Korean patch project pages. */
(function(){
  "use strict";
  function init(){
    var main=document.querySelector("main.shell")||document.querySelector("main");
    if(!main||document.querySelector(".project-lightbox"))return;
    // All content images, excluding decorative navigation/support images.
    var photos=Array.prototype.slice.call(main.querySelectorAll("img")).filter(function(img){
      return !!img.getAttribute("src")&&!img.closest(".support-coffee, .download-link");
    });
    if(!photos.length)return;
    var dialog=document.createElement("dialog");
    dialog.className="project-lightbox";
    dialog.setAttribute("aria-label","게임 이미지 크게 보기");
    dialog.innerHTML='<div class="project-lightbox-frame">'+
      '<div class="project-lightbox-header"><span class="project-lightbox-title">게임 이미지</span><button class="project-lightbox-close" type="button" aria-label="이미지 닫기">×</button></div>'+
      '<div class="project-lightbox-stage"><img alt=""></div>'+
      '<div class="project-lightbox-footer"><div class="project-lightbox-caption" aria-live="polite"></div>'+
      '<div class="project-lightbox-controls" hidden><button class="project-lightbox-prev" type="button" aria-label="이전 이미지">‹</button><span class="project-lightbox-counter"></span><button class="project-lightbox-next" type="button" aria-label="다음 이미지">›</button></div></div></div>';
    document.body.appendChild(dialog);
    var shownImage=dialog.querySelector(".project-lightbox-stage img");
    var caption=dialog.querySelector(".project-lightbox-caption");
    var count=dialog.querySelector(".project-lightbox-counter");
    var controls=dialog.querySelector(".project-lightbox-controls");
    var back=dialog.querySelector(".project-lightbox-prev");
    var forward=dialog.querySelector(".project-lightbox-next");
    var close=dialog.querySelector(".project-lightbox-close");
    var group=[],position=0,returnFocus=null;
    function display(){
      var item=group[position];
      if(!item)return;
      var fig=item.closest("figure");
      var label=fig&&fig.querySelector("figcaption") ? fig.querySelector("figcaption").textContent.replace(/\s+/g," ").trim() : (item.alt||"게임 이미지");
      shownImage.src=item.currentSrc||item.src;
      shownImage.alt=item.alt||"게임 이미지";
      caption.textContent=label;
      controls.hidden=group.length<2;
      count.textContent=(position+1)+" / "+group.length;
      back.disabled=position===0;
      forward.disabled=position===group.length-1;
    }
    function open(img){
      var gallery=img.closest(".catalogue-gallery");
      var article=img.closest(".scope");
      group=gallery?Array.prototype.slice.call(gallery.querySelectorAll("img")):
        article?Array.prototype.slice.call(article.querySelectorAll("img")):[img];
      position=Math.max(0,group.indexOf(img));
      returnFocus=img.closest("a")||img;
      display();
      if(typeof dialog.showModal==="function"){
        dialog.showModal();
        document.documentElement.classList.add("project-lightbox-open");
        close.focus();
      }else{
        // Images inside catalogue retain their direct-link fallback if dialog is unsupported.
        window.open(img.currentSrc||img.src,"_blank","noopener");
      }
    }
    function dismiss(){if(dialog.open)dialog.close();}
    photos.forEach(function(img){
      img.classList.add("project-lightbox-target");
      if(!img.closest("a")){
        img.setAttribute("tabindex","0");
        img.setAttribute("role","button");
        img.setAttribute("aria-label","이미지 크게 보기: "+(img.alt||"게임 이미지"));
        img.addEventListener("keydown",function(event){
          if(event.key==="Enter"||event.key===" "){event.preventDefault();open(img);}
        });
      }else{
        // Existing image links already support keyboard Enter.
        var anchor=img.closest("a");
        if(anchor.closest(".catalogue-gallery"))anchor.setAttribute("aria-label","이미지 크게 보기: "+(img.alt||"게임 이미지"));
      }
    });
    main.addEventListener("click",function(event){
      if(event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
      var img=event.target.closest("img.project-lightbox-target");
      if(!img||!main.contains(img))return;
      var link=img.closest("a");
      if(link&&!link.closest(".catalogue-gallery")&&link.href!==img.src&&link.href!==img.currentSrc)return;
      event.preventDefault();
      open(img);
    });
    back.addEventListener("click",function(){if(position>0){position--;display();}});
    forward.addEventListener("click",function(){if(position<group.length-1){position++;display();}});
    close.addEventListener("click",dismiss);
    dialog.addEventListener("click",function(event){if(event.target===dialog)dismiss();});
    dialog.addEventListener("keydown",function(event){
      if(event.key==="ArrowLeft"&&position>0){event.preventDefault();position--;display();}
      if(event.key==="ArrowRight"&&position<group.length-1){event.preventDefault();position++;display();}
    });
    dialog.addEventListener("close",function(){
      document.documentElement.classList.remove("project-lightbox-open");
      shownImage.removeAttribute("src");
      if(returnFocus&&document.contains(returnFocus))returnFocus.focus({preventScroll:true});
    });
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});
  else init();
})();
