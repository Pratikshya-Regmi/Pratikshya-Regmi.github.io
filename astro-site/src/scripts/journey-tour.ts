import {arcPoint,distanceLabel,type Coordinate} from '../utils/journey-geometry';
export interface TourPlace {id:string;label:string;lng:number;lat:number;zoom:number;bearing:number}
export interface TourBeat {
  id:string;title:string;detail:string;center:Coordinate;zoom:number;pitch:number;bearing:number;
  duration:number;hold:number;chapter?:number;terrain:boolean;crossing?:boolean;minZoom?:number;
}
export function createJourneyTour(places:TourPlace[]) {
  const point=(id:string):Coordinate=>{const p=places.find(p=>p.id===id)!;return [p.lng,p.lat];};
  const from=point('kathmandu'),to=point('tamucc');
  const middle=arcPoint(from,to,0.5);
  // Looking down from the northern hemisphere keeps both endpoints in one view.
  const distance=distanceLabel(from,to);
  const earth:TourBeat={id:'earth',title:'One Earth. A journey across it.',detail:'From Jaljala–5, Parbat, Nepal to the United States.',center:[70,24],zoom:0,pitch:0,bearing:0,duration:1800,hold:2200,terrain:false};
  const nepal:TourBeat={id:'nepal',title:'The first chapters: Nepal',detail:'Home, childhood school, high school and undergraduate study — all in Nepal.',center:[84.5,28],zoom:6.5,pitch:15,bearing:0,duration:3500,hold:1500,terrain:false};
  const arrival=(id:string,title:string,detail:string,duration=3200):TourBeat=>{
    const chapter=places.findIndex(p=>p.id===id),p=places[chapter];
    return {id,title,detail,center:[p.lng,p.lat],zoom:p.zoom,pitch:50,bearing:p.bearing,duration,hold:3200,terrain:true,chapter,minZoom:id==='capitol'?7:undefined};
  };
  const crossing:TourBeat[]=[
    {...nepal,id:'depart-nepal',title:'A new chapter, across the world',detail:'Leaving the Nepal chapter for graduate study in Texas.',duration:3300,hold:900},
    {id:'nepal-to-usa',title:`Nepal → United States · ${distance}`,detail:'Kathmandu University → Texas A&M–Corpus Christi. Great-circle distance; not an actual flight route.',center:[middle[0],Math.min(82,middle[1])],zoom:0,pitch:0,bearing:0,duration:4000,hold:5000,terrain:false,crossing:true},
    {id:'usa',title:'Across the world, to Texas',detail:'The Gulf Coast of the United States.',center:to,zoom:4.5,pitch:0,bearing:0,duration:4000,hold:1400,terrain:false,crossing:true},
    arrival('tamucc','Graduate study on the Texas coast','Texas A&M University-Corpus Christi · Master’s studies',4200)
  ];
  return {earth,nepal,crossing,distance,beats:[
    earth,nepal,
    arrival('home','Jaljala–5, Parbat','Where my journey began.',4500),
    arrival('beni','Beni Horizon Academy','Childhood school · Nepal',2500),
    arrival('capitol','Capitol Hill Academy','High school · Nepal',3800),
    arrival('kathmandu','Kathmandu University','Undergraduate studies · Nepal',2700),
    ...crossing,
    arrival('ncsu','My current research home','North Carolina State University · Current Ph.D.',4200)
  ]};
}
