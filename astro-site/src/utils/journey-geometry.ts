export type Coordinate = [number, number];
const radians = Math.PI / 180;
const earthRadiusKm = 6371.0088;
function vector([lng,lat]:Coordinate):[number,number,number] {
  return [Math.cos(lat*radians)*Math.cos(lng*radians),Math.cos(lat*radians)*Math.sin(lng*radians),Math.sin(lat*radians)];
}
export function distanceKm(from:Coordinate,to:Coordinate):number {
  const a=Math.sin((to[1]-from[1])*radians/2)**2+Math.cos(from[1]*radians)*Math.cos(to[1]*radians)*Math.sin((to[0]-from[0])*radians/2)**2;
  return 2*earthRadiusKm*Math.asin(Math.sqrt(Math.min(1,Math.max(0,a))));
}
export function distanceLabel(from:Coordinate,to:Coordinate):string {
  return `${(Math.round(distanceKm(from,to)/100)*100).toLocaleString('en-US')} km`;
}
/** Spherical interpolation follows the shortest surface arc, not a travel itinerary. */
export function arcPoint(from:Coordinate,to:Coordinate,t:number):Coordinate {
  if(t<=0)return [...from];if(t>=1)return [...to];
  const a=vector(from),b=vector(to);
  const angle=Math.acos(Math.min(1,Math.max(-1,a.reduce((sum,v,i)=>sum+v*b[i],0))));
  if(angle<1e-8)return [...from];
  if(Math.PI-angle<1e-8)throw new Error('An antipodal route has no unique shortest arc.');
  const w1=Math.sin((1-t)*angle)/Math.sin(angle),w2=Math.sin(t*angle)/Math.sin(angle);
  const [x,y,z]=a.map((v,i)=>v*w1+b[i]*w2);
  return [Math.atan2(y,x)/radians,Math.atan2(z,Math.hypot(x,y))/radians];
}
/** Split at the dateline so no segment draws a spurious line across a flat map. */
export function greatCircle(from:Coordinate,to:Coordinate,samples=128):Coordinate[][] {
  const lines:Coordinate[][]=[[arcPoint(from,to,0)]];
  for(let i=1;i<=samples;i++){
    const point=arcPoint(from,to,i/samples),line=lines.at(-1)!,previous=line.at(-1)!;
    if(Math.abs(point[0]-previous[0])>180){
      const adjusted=point[0]+(point[0]<previous[0]?360:-360),edge=adjusted>180?180:-180;
      // Locate the crossing on the sphere; latitude interpolation is inaccurate
      // for a route passing close to a pole, such as Nepal to southern Texas.
      let low=(i-1)/samples,high=i/samples;
      for(let step=0;step<40;step++){
        const middle=(low+high)/2,candidate=arcPoint(from,to,middle);
        let longitude=candidate[0];
        if(longitude-previous[0]>180)longitude-=360;
        if(longitude-previous[0]<-180)longitude+=360;
        if(adjusted>previous[0]?longitude<edge:longitude>edge)low=middle;else high=middle;
      }
      const latitude=arcPoint(from,to,(low+high)/2)[1];
      line.push([edge,latitude]);lines.push([[-edge,latitude],point]);
    }else line.push(point);
  }
  return lines;
}
