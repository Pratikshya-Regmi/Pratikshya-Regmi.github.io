import type {Map as TerrainMap, Marker} from 'maplibre-gl';
import {greatCircle} from '../utils/journey-geometry';
import {createJourneyTour,type TourBeat} from './journey-tour';

interface Chapter {id:string;label:string;lat:number;lng:number;zoom:number;bearing:number;branch:boolean;areaRadiusKm?:number}
export function setupJourney(shell:HTMLElement) {
  const chapters:Chapter[]=JSON.parse(shell.dataset.chapters!);
  const main=chapters.filter(c=>!c.branch);
  const tour=createJourneyTour(main);
  const panels=[...shell.querySelectorAll<HTMLElement>('[data-chapter]')];
  const stops=[...shell.querySelectorAll<HTMLAnchorElement>('[data-stop]')];
  const get=<T extends HTMLElement>(selector:string)=>shell.querySelector<T>(selector)!;
  const load=get<HTMLButtonElement>('[data-journey-load]');
  const play=get<HTMLButtonElement>('[data-play]');
  const prev=get<HTMLButtonElement>('[data-previous]');
  const next=get<HTMLButtonElement>('[data-next]');
  const status=get<HTMLElement>('[data-journey-status]');
  const canvas=get<HTMLElement>('[data-journey-canvas]');
  const cover=get<HTMLElement>('[data-journey-cover]');
  const terrain=get<HTMLButtonElement>('[data-terrain]');
  const labels=get<HTMLButtonElement>('[data-labels]');
  const maximize=get<HTMLButtonElement>('[data-maximize]');
  const layout=get<HTMLElement>('[data-journey-layout]');
  const picker=get<HTMLSelectElement>('[data-place-picker]');
  const google=get<HTMLAnchorElement>('[data-google-maps]');
  const restart=get<HTMLButtonElement>('[data-restart]');
  const tourCaption=get<HTMLElement>('[data-tour-caption]');
  const tourHeading=get<HTMLElement>('[data-tour-heading]');
  const tourDetail=get<HTMLElement>('[data-tour-detail]');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let map:TerrainMap|undefined;
  let markers:Marker[]=[];
  let selected=0,playing=false,ready=false,terrainOn=true,degraded=false;
  let timer:ReturnType<typeof setTimeout>|undefined;
  let watchdog:ReturnType<typeof setTimeout>|undefined;
  let sequence=tour.beats,cursor=0,hasStarted=false;
  let visible=false;
  function cameraZoom(beat:TourBeat) {
    if(beat.zoom!==0)return beat.zoom;
    const responsive=Math.log2(Math.max(200,Math.min(canvas.clientWidth,canvas.clientHeight))/510);
    return (beat.id==='nepal-to-usa'?-1.35-(canvas.clientWidth<500?0.45:0):1)+responsive;
  }
  function caption(title:string,detail:string,phase:string) {
    tourCaption.hidden=false;tourHeading.textContent=title;tourDetail.textContent=detail;shell.dataset.tourPhase=phase;
    status.textContent=`${title}. ${detail}`;
  }
  function crossingVisible(show:boolean) {
    if(ready&&map)map.setLayoutProperty('distance-arc','visibility',show?'visible':'none');
  }
  function refreshMarkers() {
    if(!map)return;const global=map.getZoom()<5;
    markers.forEach((marker,i)=>{marker.getElement().hidden=global&&![0,4].includes(i);marker.getElement().classList.toggle('journey-marker-global',global);const name=marker.getElement().querySelector('.journey-marker-name');if(name)name.textContent=global?(i===0?'Nepal':'Texas, United States'):chapters[i].label;});
  }
  function pause() {
    playing=false;clearTimeout(timer);map?.stop();shell.dataset.tourRunning='false';play.textContent=reduced.matches?'Motion reduced':hasStarted?'Resume journey':'Play journey';
    play.setAttribute('aria-pressed','false');
  }
  function select(index:number, fly=true) {
    selected=index;
    const chapter=chapters[index];
    picker.value=String(index);
    google.href=`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${chapter.lat},${chapter.lng}`)}`;
    panels.forEach((panel,i)=>panel.hidden=i!==index);
    stops.forEach((stop,i)=>i===index?stop.setAttribute('aria-current','step'):stop.removeAttribute('aria-current'));
    markers.forEach((marker,i)=>marker.getElement().setAttribute('aria-pressed',String(i===index)));
    get<HTMLElement>('[data-step-count]').textContent=chapter.branch?'Research stop':`${String(index+1).padStart(2,'0')} / 06`;
    prev.disabled=index===0;next.disabled=index===main.length-1;
    status.textContent=`${chapter.label}. ${degraded?'Some imagery or terrain is unavailable. All chapter stories remain available.':ready?'Use the chapter controls or map to explore.':'Open the map to explore the terrain.'}`;
    if(ready&&map&&fly){
      crossingVisible(false);map.setTerrain(terrainOn?{source:'terrain',exaggeration:1}:null);
      caption(chapter.label,index<4?'Nepal':chapter.id==='tamucc'?'Texas, United States':chapter.id==='ncsu'?'North Carolina, United States':'Tennessee, United States',chapter.id);
      map.flyTo({center:[chapter.lng,chapter.lat],zoom:chapter.zoom,pitch:terrainOn?50:0,bearing:chapter.bearing,duration:reduced.matches?0:3200,essential:false});
    }
  }
  const hashIndex=chapters.findIndex(c=>location.hash===`#journey-${c.id}`);
  select(hashIndex>=0?hashIndex:0,false);
  load.hidden=false;get<HTMLElement>('[data-journey-controls]').hidden=false;
  function runBeat() {
    if(!playing||!ready||!map)return;
    const beat=sequence[cursor];
    if(!beat){pause();hasStarted=false;cursor=0;sequence=tour.beats;play.textContent='Replay journey';status.textContent='Journey complete: my current research home at NC State.';return;}
    if(beat.chapter!==undefined)select(beat.chapter,false);
    crossingVisible(Boolean(beat.crossing));
    caption(beat.title,beat.detail,beat.id);
    map.setTerrain(beat.terrain&&terrainOn?{source:'terrain',exaggeration:1}:null);
    map.flyTo({center:beat.center,zoom:cameraZoom(beat),pitch:beat.terrain&&!terrainOn?0:beat.pitch,bearing:beat.bearing,duration:beat.duration,essential:false,minZoom:beat.minZoom});
    timer=setTimeout(()=>{cursor++;runBeat();},beat.duration+beat.hold);
  }
  function startTour(beats?:TourBeat[]) {
    if(!ready||reduced.matches)return;
    clearTimeout(timer);map?.stop();
    if(beats){sequence=beats;cursor=0;}
    hasStarted=true;playing=true;play.textContent='Pause journey';play.setAttribute('aria-pressed','true');shell.dataset.tourRunning='true';runBeat();
  }
  function goTo(index:number) {
    const fromNepal=selected<4;
    pause();sequence=tour.beats;cursor=0;hasStarted=false;play.textContent=reduced.matches?'Motion reduced':'Play journey';
    if(ready&&!reduced.matches&&fromNepal&&index===4){startTour(tour.crossing);return;}
    select(index);
  }
  stops.forEach((stop,index)=>stop.addEventListener('click',event=>{event.preventDefault();goTo(index);}));
  picker.addEventListener('change',()=>goTo(Number(picker.value)));
  maximize.addEventListener('click',()=>layout.querySelector<HTMLButtonElement>('.maplibregl-ctrl-fullscreen,.maplibregl-ctrl-shrink')?.click());
  prev.addEventListener('click',()=>goTo(selected>=main.length?main.length-1:Math.max(0,selected-1)));
  next.addEventListener('click',()=>goTo(selected>=main.length?main.length-1:Math.min(main.length-1,selected+1)));
  play.addEventListener('click',()=>{if(playing)pause();else startTour();});
  restart.addEventListener('click',()=>{if(reduced.matches){pause();showOverview(tour.earth);}else startTour(tour.beats);});
  const motionChanged=()=>{pause();play.disabled=!ready||reduced.matches;if(reduced.matches)status.textContent='Reduced motion is on. Choose individual chapters for instant map changes.';};
  reduced.addEventListener('change',motionChanged);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(!visible)pause();},{threshold:0}).observe(canvas);
  shell.addEventListener('keydown',event=>{
    if(event.key==='Escape'){pause();if(layout.classList.contains('maplibregl-pseudo-fullscreen'))maximize.click();}
    if(event.key==='Tab'&&layout.classList.contains('maplibregl-pseudo-fullscreen')){
      const focusable=[...layout.querySelectorAll<HTMLElement>('button:not(:disabled),a[href],select,[tabindex="0"]')].filter(el=>el.getClientRects().length);
      const first=focusable[0],last=focusable.at(-1);
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}
      if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
    }
  });
  function showOverview(beat:TourBeat) {
    if(!map||!ready)return;pause();map.setTerrain(null);crossingVisible(Boolean(beat.crossing));caption(beat.title,beat.detail,beat.id);
    map.flyTo({center:beat.center,zoom:cameraZoom(beat),pitch:0,bearing:0,duration:reduced.matches?0:2400,essential:false});
  }
  get<HTMLButtonElement>('[data-overview]').addEventListener('click',()=>showOverview(tour.earth));
  get<HTMLButtonElement>('[data-distance-view]').addEventListener('click',()=>showOverview(tour.crossing[1]));
  terrain.addEventListener('click',()=>{
    if(!map||!ready)return;pause();terrainOn=!terrainOn;terrain.setAttribute('aria-pressed',String(terrainOn));
    map.setTerrain(terrainOn?{source:'terrain',exaggeration:1}:null);
    map.easeTo({pitch:terrainOn?50:0,duration:reduced.matches?0:700});
  });
  labels.addEventListener('click',()=>{
    if(!map||!ready)return;
    const show=labels.getAttribute('aria-pressed')!=='true';
    labels.setAttribute('aria-pressed',String(show));shell.classList.toggle('journey-labels-hidden',!show);
    for(const id of ['place-labels','road-labels','water-labels'])map.setLayoutProperty(id,'visibility',show?'visible':'none');
  });
  function fail() {
    clearTimeout(watchdog);pause();ready=false;play.disabled=true;restart.disabled=true;tourCaption.hidden=true;
    map?.remove();map=undefined;markers=[];
    canvas.hidden=true;cover.hidden=false;load.hidden=false;load.disabled=false;load.textContent='Retry interactive map';
    get<HTMLElement>('[data-map-tools]').hidden=true;
    status.textContent='The interactive map is unavailable. All chapters remain available using the place links and arrows.';
  }
  load.addEventListener('click',async()=>{
    load.disabled=true;degraded=false;status.textContent='Loading satellite imagery and terrain…';
    try {
      const [{Map,Marker,NavigationControl,FullscreenControl,setWorkerUrl},worker,stylesheet]=await Promise.all([import('maplibre-gl'),import('maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url'),import('maplibre-gl/dist/maplibre-gl.css?url')]);
      setWorkerUrl(worker.default);
      if(!document.querySelector('[data-journey-map-style]'))await new Promise<void>((resolve,reject)=>{
        const link=document.createElement('link');link.rel='stylesheet';link.href=stylesheet.default;link.dataset.journeyMapStyle='';
        const timeout=setTimeout(()=>{link.remove();reject(new Error('Map stylesheet timed out'));},15000);
        link.onload=()=>{clearTimeout(timeout);resolve();};
        link.onerror=()=>{clearTimeout(timeout);link.remove();reject(new Error('Map stylesheet unavailable'));};
        document.head.append(link);
      });
      canvas.hidden=false;cover.hidden=true;
      terrainOn=true;terrain.setAttribute('aria-pressed','true');
      labels.setAttribute('aria-pressed','true');shell.classList.remove('journey-labels-hidden');
      const home=chapters.find(c=>c.id==='home')!;
      const radius=home.areaRadiusKm??1;
      const ring=Array.from({length:65},(_,i)=>{const angle=i/64*Math.PI*2;return [home.lng+radius*Math.cos(angle)/(111.32*Math.cos(home.lat*Math.PI/180)),home.lat+radius*Math.sin(angle)/111.32];});
      map=new Map({container:canvas,center:tour.earth.center,zoom:cameraZoom(tour.earth),pitch:0,bearing:0,minZoom:-3,
        pixelRatio:Math.min(window.devicePixelRatio,1.5),maxTileCacheSize:128,
        maxZoom:15,maxPitch:65,cooperativeGestures:true,attributionControl:{compact:false},
        style:{version:8,projection:{type:'globe'},sky:{'atmosphere-blend':['interpolate',['linear'],['zoom'],0,1,5,1,7,0]},glyphs:'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',sources:{
          labels:{type:'vector',url:'https://tiles.openfreemap.org/planet',attribution:'Labels: <a href="https://openfreemap.org/">OpenFreeMap</a> · <a href="https://openmaptiles.org/">OpenMapTiles</a> · © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'},
          'home-area':{type:'geojson',data:{type:'Feature',properties:{},geometry:{type:'Polygon',coordinates:[ring]}}},
          satellite:{type:'raster',tiles:['https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2020_3857/default/g/{z}/{y}/{x}.jpg'],tileSize:256,maxzoom:14,attribution:'Sentinel-2 cloudless © <a href="https://s2maps.eu/">EOX</a> · Contains modified Copernicus Sentinel data 2020 · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>'},
          terrain:{type:'raster-dem',url:'https://tiles.mapterhorn.com/tilejson.json',attribution:'Terrain: <a href="https://mapterhorn.com/attribution">Mapterhorn & data contributors</a>'},
          route:{type:'geojson',data:{type:'Feature',properties:{},geometry:{type:'MultiLineString',coordinates:main.slice(1).flatMap((c,i)=>greatCircle([main[i].lng,main[i].lat],[c.lng,c.lat]))}}},
          crossing:{type:'geojson',data:{type:'Feature',properties:{},geometry:{type:'MultiLineString',coordinates:greatCircle([main[3].lng,main[3].lat],[main[4].lng,main[4].lat])}}}
        },layers:[{id:'background',type:'background',paint:{'background-color':'#0a1512'}},{id:'satellite',type:'raster',source:'satellite'},
          {id:'home-area-fill',type:'fill',source:'home-area',paint:{'fill-color':'#b8df9a','fill-opacity':0.16}},
          {id:'home-area-outline',type:'line',source:'home-area',paint:{'line-color':'#d6f5ba','line-width':2,'line-dasharray':[3,3]}},
          {id:'journey-line',type:'line',source:'route',paint:{'line-color':'#d6f5ba','line-width':2,'line-dasharray':[2,3],'line-opacity':0.85}},
          {id:'distance-arc',type:'line',source:'crossing',layout:{visibility:'none'},paint:{'line-color':'#ffc978','line-width':4}},
          {id:'place-labels',type:'symbol',source:'labels','source-layer':'place',filter:['!', ['in','thama pidalla',['downcase',['concat',['coalesce',['get','name:en'],''],' ',['coalesce',['get','name:latin'],''],' ',['coalesce',['get','name'],'']]]]],layout:{'text-field':['coalesce',['get','name:en'],['get','name:latin'],['get','name']],'text-font':['Noto Sans Regular'],'text-size':['interpolate',['linear'],['zoom'],3,11,14,16],'text-max-width':9},paint:{'text-color':'#ffffff','text-halo-color':'#10231d','text-halo-width':1.7}},
          {id:'road-labels',type:'symbol',source:'labels','source-layer':'transportation_name',minzoom:12,layout:{'symbol-placement':'line','text-field':['coalesce',['get','name:en'],['get','name:latin'],['get','name']],'text-font':['Noto Sans Regular'],'text-size':12},paint:{'text-color':'#ffffff','text-halo-color':'#10231d','text-halo-width':1.5}},
          {id:'water-labels',type:'symbol',source:'labels','source-layer':'water_name',minzoom:9,layout:{'text-field':['coalesce',['get','name:en'],['get','name:latin'],['get','name']],'text-font':['Noto Sans Regular'],'text-size':12},paint:{'text-color':'#c8efff','text-halo-color':'#10231d','text-halo-width':1.5}}
        ]}});
      map.scrollZoom.disable();map.addControl(new NavigationControl({visualizePitch:true}),'top-right');
      const fullscreen=new FullscreenControl({container:layout});
      map.addControl(fullscreen,'top-right');
      fullscreen.on('fullscreenstart',()=>{pause();maximize.textContent='Restore map';maximize.setAttribute('aria-pressed','true');requestAnimationFrame(()=>{map?.resize();maximize.focus();});});
      fullscreen.on('fullscreenend',()=>{pause();maximize.textContent='Maximize map';maximize.setAttribute('aria-pressed','false');requestAnimationFrame(()=>{map?.resize();maximize.focus();});});
      map.getCanvas().setAttribute('aria-label','Journey map. Use arrow keys to pan and plus or minus to zoom; chapter controls are below.');
      watchdog=setTimeout(()=>{if(!ready)fail();},25000);
      map.on('error',()=>{degraded=true;status.textContent='Some imagery or terrain could not load. Chapter stories remain available; try another place or retry later.';});
      map.getCanvas().addEventListener('webglcontextlost',event=>{event.preventDefault();fail();},{once:true});
      map.on('movestart',event=>{if(event.originalEvent)pause();});
      map.on('zoom',refreshMarkers);
      map.on('load',()=>{
        clearTimeout(watchdog);ready=true;load.hidden=true;
        get<HTMLElement>('[data-map-tools]').hidden=false;
        markers=chapters.map((c,index)=>{
          const button=document.createElement('button');button.type='button';button.className='journey-marker';
          button.textContent=c.branch?'↗':String(index+1);button.setAttribute('aria-label',`Show ${c.label}`);button.setAttribute('aria-controls',`journey-${c.id}`);
          if(c.id==='home')button.classList.add('journey-marker-home');
          const name=document.createElement('span');name.className='journey-marker-name';name.textContent=c.label;name.setAttribute('aria-hidden','true');button.append(name);
          button.addEventListener('click',()=>{pause();select(index);});
          return new Marker({element:button,opacityWhenCovered:0}).setLngLat([c.lng,c.lat]).addTo(map!);
        });
        motionChanged();select(selected,false);refreshMarkers();restart.disabled=false;caption(tour.earth.title,tour.earth.detail,'earth');
        if(!reduced.matches&&visible&&!document.hidden)startTour(tour.beats);
      });
    }catch(error){console.warn('Journey map could not initialize.',error);fail();}
  });
}
