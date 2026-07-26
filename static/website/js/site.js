document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("loading");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const releasePage = () => document.body.classList.remove("loading");
  setTimeout(releasePage, 2400);
  const q = s => document.querySelector(s), qa = s => [...document.querySelectorAll(s)];
  if (window.gsap) {
    gsap.timeline({onComplete:releasePage})
      .to(".loader__line i",{x:"0%",duration:.7,ease:"power2.inOut"})
      .to(".loader__brand",{opacity:0,y:-8,duration:.3})
      .to(".loader",{yPercent:-100,duration:.75,ease:"power4.inOut"});
  } else { q(".loader")?.remove(); releasePage(); }



  if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);

    const directionalReveal = (el, distance = 28) => {
      const show = fromY => gsap.fromTo(el,{y:fromY,opacity:0},{y:0,opacity:1,duration:.62,ease:"power2.out",overwrite:true});
      gsap.set(el,{opacity:0,y:distance});
      ScrollTrigger.create({
        trigger:el,start:"top 94%",end:"bottom 6%",
        onEnter:()=>show(distance),
        onEnterBack:()=>show(-distance)
      });
    };
    const animated = new Set(qa(".reveal,.services-heading,.products-intro,.work-title,.work .project,.process .process-step,.testimonial-card"));
    animated.forEach(el=>directionalReveal(el));

    const splitTypography = el => {
      if (el.dataset.typeSplit) return [...el.querySelectorAll(".type-word>i")];
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      const nodes = [];
      while (walker.nextNode()) if (walker.currentNode.nodeValue.trim()) nodes.push(walker.currentNode);
      nodes.forEach(node => {
        const fragment = document.createDocumentFragment();
        node.nodeValue.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) fragment.appendChild(document.createTextNode(part));
          else {
            const word = document.createElement("span"), inner = document.createElement("i");
            word.className = "type-word";
            inner.textContent = part;
            word.appendChild(inner);
            fragment.appendChild(word);
          }
        });
        node.replaceWith(fragment);
      });
      el.dataset.typeSplit = "true";
      return [...el.querySelectorAll(".type-word>i")];
    };
    const premiumType = (el, strong = false) => {
      const words = splitTypography(el);
      if (!words.length) return;
      const show = direction => gsap.fromTo(words,
        {yPercent:direction > 0 ? 112 : -105,scale:strong ? .68 : .82,rotateX:direction > 0 ? -38 : 32,opacity:0,filter:"blur(9px)"},
        {yPercent:0,scale:1,rotateX:0,opacity:1,filter:"blur(0px)",duration:strong ? 1.05 : .78,stagger:strong ? .055 : .032,ease:"power4.out",overwrite:true}
      );
      gsap.set(words,{yPercent:105,scale:strong ? .68 : .82,opacity:0,transformOrigin:"50% 100%",transformPerspective:800});
      ScrollTrigger.create({trigger:el,start:"top 92%",end:"bottom 8%",onEnter:()=>show(1),onEnterBack:()=>show(-1)});
      requestAnimationFrame(()=>{const r=el.getBoundingClientRect();if(r.top<innerHeight*.92&&r.bottom>innerHeight*.08)show(1)});
    };
    const typeTargets = new Set(qa(".hero__title,.local-intro h2,.about .display,.services-heading .display,.products-intro .display,.work-title .display,.process-hero .display,.testimonials .section-head h2,.faq__intro .display,.contact .display,.page-hero h1,.page-cta h2"));
    typeTargets.forEach(el=>premiumType(el,el.classList.contains("hero__title")||el.matches(".page-hero h1")));

    qa("[data-scroll-copy]").forEach(section => {
      const front = section.querySelector(".scroll-copy--front");
      const back = section.querySelector(".scroll-copy--back");
      gsap.fromTo(front,{xPercent:-12},{xPercent:5,ease:"none",scrollTrigger:{trigger:section,start:"top bottom",end:"bottom top",scrub:.65,invalidateOnRefresh:true}});
      gsap.fromTo(back,{xPercent:4},{xPercent:-13,ease:"none",scrollTrigger:{trigger:section,start:"top bottom",end:"bottom top",scrub:.65,invalidateOnRefresh:true}});
    });

    qa("[data-lettering]").forEach(title => {
      const label = title.textContent.trim();
      title.textContent = "";
      [...label].forEach((character,index) => {
        const span = document.createElement("span");
        span.className = character === " " ? "lettering-space" : "lettering-char";
        span.textContent = character === " " ? "\u00a0" : character;
        span.setAttribute("aria-hidden","true");
        span.style.setProperty("--letter-index",index);
        title.appendChild(span);
      });
      const letters = [...title.querySelectorAll(".lettering-char")];
      gsap.fromTo(letters,
        {yPercent:index=>index%2?135:-135,rotateX:index=>index%2?-80:80,rotateZ:index=>(index%3-1)*7,scale:.56,opacity:.06,filter:"blur(12px)"},
        {yPercent:0,rotateX:0,rotateZ:0,scale:1,opacity:1,filter:"blur(0px)",stagger:.045,ease:"power2.out",scrollTrigger:{trigger:title.closest(".lettering-section"),start:"top 82%",end:"bottom 28%",scrub:.7,invalidateOnRefresh:true}}
      );
    });
    if(q(".process__line b")) gsap.to(".process__line b",{scaleY:1,scrollTrigger:{trigger:".process__track",start:"top 60%",end:"bottom 70%",scrub:true}});
    gsap.to(".dashboard-scene",{y:-90,scrollTrigger:{trigger:".hero",start:"top top",end:"bottom top",scrub:1}});
  }
  const nav = q(".nav"), progress = q(".scroll-progress");
  addEventListener("scroll",()=>{nav?.classList.toggle("scrolled",scrollY>30);if(progress)progress.style.transform=`scaleX(${scrollY/(document.documentElement.scrollHeight-innerHeight)})`},{passive:true});
  qa('a[href^="#"]').forEach(a=>a.addEventListener("click",e=>{const target=q(a.getAttribute("href"));if(target){e.preventDefault();target.scrollIntoView({behavior:reduce?"auto":"smooth"})}}));
  qa(".career-apply-link").forEach(link=>link.addEventListener("click",()=>{const role=q("#id_opening"),form=q("#application");if(role&&link.dataset.careerRole){role.value=link.dataset.careerRole;role.dispatchEvent(new Event("change",{bubbles:true}))}if(form)setTimeout(()=>{form.scrollIntoView({behavior:reduce?"auto":"smooth",block:"start"});setTimeout(()=>role?.focus({preventScroll:true}),reduce?0:650)},20)}));  const formState=new URLSearchParams(location.search),formTarget=formState.has("applied")?q("#application"):formState.has("submitted")?(q("#project-brief")||q("#contact")):q(".form-errors,.career-form-errors,.errorlist")?.closest("form")?.closest("section");
  if(formTarget){
    if("scrollRestoration" in history)history.scrollRestoration="manual";
    const showFormFeedback=()=>{formTarget.scrollIntoView({behavior:"auto",block:"start"});const feedback=formTarget.querySelector(".form-success,.career-form-message,.form-errors,.career-form-errors,.errorlist");if(feedback){feedback.setAttribute("tabindex","-1");feedback.focus({preventScroll:true})}};
    setTimeout(showFormFeedback,reduce?80:1850);setTimeout(showFormFeedback,2450);
  }
  qa(".accordion__item button").forEach(btn=>btn.addEventListener("click",()=>{
    const item=btn.parentElement, body=item.querySelector(".accordion__body"), active=item.classList.toggle("active");
    btn.setAttribute("aria-expanded",active); body.style.height=active?body.scrollHeight+"px":"0px";
  }));
if(window.Swiper)new Swiper(".quote-slider",{loop:true,speed:650,spaceBetween:16,slidesPerView:1,autoplay:{delay:5200,disableOnInteraction:false,pauseOnMouseEnter:true},observer:true,observeParents:true,navigation:{nextEl:".quote-next",prevEl:".quote-prev"},pagination:{el:".swiper-pagination",clickable:true},breakpoints:{720:{slidesPerView:2},1100:{slidesPerView:3}}});
  const menuToggle=q(".menu-toggle"),primaryNav=q("#primary-navigation");
  let menuScrollY=0;
  const setMenuOpen=open=>{
    if(!nav||!menuToggle)return;
    if(open){
      menuScrollY=window.scrollY;
      nav.classList.add("menu-open");
      document.body.classList.add("menu-active");
      document.body.style.top=`-${menuScrollY}px`;
    }else{
      nav.scrollTop=0;
      nav.classList.remove("menu-open");
      document.body.classList.remove("menu-active");
      document.body.style.removeProperty("top");
      window.scrollTo(0,menuScrollY);
      requestAnimationFrame(()=>window.scrollTo(0,menuScrollY));
    }
    menuToggle.setAttribute("aria-expanded",String(open));
    menuToggle.setAttribute("aria-label",open?"Close navigation menu":"Open navigation menu");
  };
  menuToggle?.addEventListener("click",()=>setMenuOpen(!nav.classList.contains("menu-open")));
  primaryNav?.addEventListener("click",event=>{if(event.target.closest("a"))setMenuOpen(false)});
  document.addEventListener("keydown",event=>{if(event.key==="Escape"&&nav?.classList.contains("menu-open")){setMenuOpen(false);menuToggle?.focus()}});
  addEventListener("resize",()=>{if(innerWidth>1050&&nav?.classList.contains("menu-open"))setMenuOpen(false)},{passive:true});
  qa(".industry-filter button").forEach(button=>button.addEventListener("click",()=>{qa(".industry-filter button").forEach(x=>x.classList.remove("active"));button.classList.add("active");const key=button.dataset.industry;qa(".client-grid article").forEach(card=>{card.hidden=key!=="all"&&card.dataset.industry!==key})}));
  const portfolioCards=qa("[data-portfolio-category]");
  if(portfolioCards.length){
    const pageSize=6,portfolioCount=q("#portfolio-result-count"),portfolioEmpty=q(".portfolio-no-results"),pager=q(".portfolio-pagination"),status=q(".portfolio-page-status"),prev=q(".portfolio-page-prev"),next=q(".portfolio-page-next");
    let activeFilter="all",currentPage=1;
    const renderPortfolio=()=>{
      const matches=portfolioCards.filter(card=>activeFilter==="all"||card.dataset.portfolioCategory===activeFilter);
      const totalPages=Math.max(1,Math.ceil(matches.length/pageSize));currentPage=Math.min(currentPage,totalPages);
      portfolioCards.forEach(card=>{card.hidden=true;card.style.removeProperty("opacity");card.style.removeProperty("transform");card.style.removeProperty("visibility")});
      matches.slice((currentPage-1)*pageSize,currentPage*pageSize).forEach(card=>{card.hidden=false});
      if(portfolioCount)portfolioCount.textContent=`${matches.length} project${matches.length===1?"":"s"}`;
      if(portfolioEmpty)portfolioEmpty.hidden=matches.length!==0;
      if(pager)pager.hidden=matches.length<=pageSize;
      if(status)status.textContent=`Page ${currentPage} of ${totalPages}`;
      if(prev)prev.disabled=currentPage===1;if(next)next.disabled=currentPage===totalPages;
      if(window.ScrollTrigger)requestAnimationFrame(()=>ScrollTrigger.refresh());
    };
    qa("[data-portfolio-filter]").forEach(button=>button.addEventListener("click",()=>{
      qa("[data-portfolio-filter]").forEach(item=>item.classList.remove("active"));button.classList.add("active");
      activeFilter=button.dataset.portfolioFilter;currentPage=1;
      if(history.replaceState)history.replaceState(null,"",activeFilter==="all"?location.pathname:`${location.pathname}#${activeFilter}`);
      renderPortfolio();
    }));
    const movePortfolioPage=direction=>{currentPage+=direction;renderPortfolio();q(".portfolio-library__head")?.scrollIntoView({behavior:reduce?"auto":"smooth",block:"start"})};
    prev?.addEventListener("click",()=>movePortfolioPage(-1));next?.addEventListener("click",()=>movePortfolioPage(1));
    const initialPortfolioFilter=location.hash.slice(1),initialButton=initialPortfolioFilter?q(`[data-portfolio-filter="${CSS.escape(initialPortfolioFilter)}"]`):null;
    if(initialButton)initialButton.click();else renderPortfolio();
  }
  const cursor=q(".cursor");
  if(cursor && matchMedia("(pointer:fine)").matches){
    addEventListener("mousemove",e=>gsap.to(cursor,{x:e.clientX,y:e.clientY,duration:.15}));
    qa(".cursor-view").forEach(el=>{el.addEventListener("mouseenter",()=>cursor.classList.add("is-view"));el.addEventListener("mouseleave",()=>cursor.classList.remove("is-view"))});
    qa(".magnetic").forEach(el=>{el.addEventListener("mousemove",e=>{const r=el.getBoundingClientRect();gsap.to(el,{x:(e.clientX-r.left-r.width/2)*.15,y:(e.clientY-r.top-r.height/2)*.15,duration:.25})});el.addEventListener("mouseleave",()=>gsap.to(el,{x:0,y:0,duration:.4}))});
    addEventListener("mousemove",e=>qa("[data-depth]").forEach(el=>{const d=+el.dataset.depth;gsap.to(el,{x:(e.clientX/innerWidth-.5)*d,y:(e.clientY/innerHeight-.5)*d,duration:1,ease:"power2.out"})}));
  }
  if(!reduce && window.THREE && q("#hero-canvas")){
    const canvas=q("#hero-canvas"), scene=new THREE.Scene(), camera=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,100), renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
    renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setSize(innerWidth,innerHeight);camera.position.z=6;
    const geo=new THREE.IcosahedronGeometry(2.1,2), mat=new THREE.MeshBasicMaterial({color:0xc7ff4a,wireframe:true,transparent:true,opacity:.075}), mesh=new THREE.Mesh(geo,mat);scene.add(mesh);mesh.position.x=2.8;
    const animate=()=>{mesh.rotation.x+=.0015;mesh.rotation.y+=.002;renderer.render(scene,camera);requestAnimationFrame(animate)};animate();
    addEventListener("resize",()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});
  }


  qa(".product-story,.service-tile,.feature-grid article").forEach(card=>{card.addEventListener("mousemove",e=>{if(!matchMedia("(pointer:fine)").matches)return;const r=card.getBoundingClientRect(),rx=(e.clientY-r.top-r.height/2)/r.height*-3,ry=(e.clientX-r.left-r.width/2)/r.width*4;gsap.to(card,{rotateX:rx,rotateY:ry,transformPerspective:900,duration:.35})});card.addEventListener("mouseleave",()=>gsap.to(card,{rotateX:0,rotateY:0,duration:.5}))});  const productRail=q(".product-rail");
  if(productRail){let productTimer,productVisible=false;const productStep=()=>{const card=productRail.querySelector(".product-story");return card?card.getBoundingClientRect().width+24:0};const moveProduct=direction=>{const step=productStep();if(!step)return;const atEnd=productRail.scrollLeft+productRail.clientWidth>=productRail.scrollWidth-20;const atStart=productRail.scrollLeft<=20;let left=productRail.scrollLeft+(step*direction);if(direction>0&&atEnd)left=0;if(direction<0&&atStart)left=Math.max(0,productRail.scrollWidth-productRail.clientWidth);productRail.scrollTo({left,behavior:"smooth"})};const rotateProducts=()=>{if(productVisible)moveProduct(1)};const stopProducts=()=>clearInterval(productTimer);const startProducts=()=>{stopProducts();if(productVisible)productTimer=setInterval(rotateProducts,5200)};new IntersectionObserver(entries=>{productVisible=entries[0]?.isIntersecting===true;if(productVisible)startProducts();else stopProducts()},{threshold:.12}).observe(productRail);q(".product-prev")?.addEventListener("click",()=>{moveProduct(-1);startProducts()});q(".product-next")?.addEventListener("click",()=>{moveProduct(1);startProducts()});productRail.addEventListener("mouseenter",stopProducts);productRail.addEventListener("mouseleave",startProducts);}  qa("[data-counter]").forEach(el=>{const raw=el.dataset.counter,match=raw.match(/[\d.]+/);if(!match)return;const target=parseFloat(match[0]),decimals=(match[0].split(".")[1]||"").length,suffix=raw.slice(match.index+match[0].length),state={value:0};ScrollTrigger.create({trigger:el,start:"top 92%",once:true,onEnter:()=>gsap.to(state,{value:target,duration:1.4,ease:"power2.out",onUpdate:()=>{el.textContent=(decimals?state.value.toFixed(decimals):Math.round(state.value))+suffix}})})});  if(!reduce && window.gsap && window.ScrollTrigger){
    qa(".product-story__image img,.page-hero__photo").forEach(image=>gsap.fromTo(image,{scale:1.12},{scale:1,ease:"none",scrollTrigger:{trigger:image.parentElement||image,start:"top bottom",end:"bottom top",scrub:1.2}}));  }
  if (window.ScrollTrigger) {
    addEventListener("load", () => ScrollTrigger.refresh(), {once:true});
    let resizeTimer;
    addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => ScrollTrigger.refresh(), 180);
    }, {passive:true});
  }
});