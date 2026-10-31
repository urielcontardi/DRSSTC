// Canvas 2D renderer: works without WebGL, GPU drivers or external libraries.
const data=__MESH_DATA__;
const names={pcb_reference:'PCB e componentes',heatsink_reference:'Dissipador 100 × 100 × 30',C14_reference:'Tomada C14 fornecida',
 '01_lower_tray':'Ventilated lower tray','02_upper_sleeve':'Removable side walls','03_C14_inlet_plate':'C14 mounting plate',
 '04_structural_lid':'Structural lid','05_modular_deck_NO_WIRE_HOLDER':'Plataforma modular · primário pendente',secondary_tube_60x280:'Tubo secundário Ø60 × 280','06_separate_feet':'Separate feet'};
const canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d',{alpha:false});
const explosion={"07_secondary_base_clamp":2.5,"10_secondary_top_clamp":3,"11_topload_pedestal":3.1,"toroid_150x40_center_M4":3.2,pcb_reference:0,heatsink_reference:-.4,C14_reference:.7,'06_separate_feet':-1,'01_lower_tray':-1,'02_upper_sleeve':.7,'03_C14_inlet_plate':.7,'04_structural_lid':1.8,'05_modular_deck_NO_WIRE_HOLDER':2.3,secondary_tube_60x280:2.7,secondary_1500_turns_envelope:2.7,primary_8_turns_reference:2.3,toroid_150x40:3.2,"11_topload_pedestal":3.0};
for(const m of data){
 m.visible=m.kind!=='placeholder';m.positions=new Float32Array(m.positions);
 m.palette=Array.from({length:20},(_,i)=>{const c=m.color.map(v=>Math.round(v*255*(.42+i*.028)));return (255<<24)|(c[2]<<16)|(c[1]<<8)|c[0]});
 const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=m.visible;
 input.onchange=()=>{m.visible=input.checked;requestDraw()};m.input=input;label.append(input,document.createTextNode(' '+(names[m.name]||m.name)));document.querySelector('#parts').append(label);
}
let az=2.46,el=1.02,zoom=1,exp=0,pending=false;
function requestDraw(){if(!pending){pending=true;requestAnimationFrame(()=>{pending=false;try{draw()}catch(e){document.querySelector('#status').textContent='Static preview available. Error: '+e.message;canvas.style.display='none'}})}}
function draw(){
 const d=1,w=innerWidth,h=innerHeight;
 if(canvas.width!==Math.round(w*d)||canvas.height!==Math.round(h*d)){canvas.width=Math.round(w*d);canvas.height=Math.round(h*d)}
 const image=ctx.createImageData(w,h),pixels=new Uint32Array(image.data.buffer),depth=new Float32Array(w*h);pixels.fill(0xff201811);depth.fill(-Infinity);
 const ca=Math.cos(az),sa=Math.sin(az),cb=Math.cos(el),sb=Math.sin(el);
 const scale=h/(2*(265+exp*1.3))*zoom,cx=w*(w>700?.59:.54),cy=h*.5,tri=[];
 for(const m of data){
  if(!m.visible)continue;
  const a=m.positions,p=new Float32Array(a.length),dz=(explosion[m.name]||0)*exp-160-exp*.4;
  const dy=(m.name==='C14_reference'||m.name==='03_C14_inlet_plate'?exp*.5:0)-50;
  for(let i=0;i<a.length;i+=3){const x=a[i]-50,y=a[i+1]+dy,z=a[i+2]+dz;
   const rx=ca*x-sa*y,ry=sa*x+ca*y;p[i]=cx+rx*scale;p[i+1]=cy-(cb*ry+sb*z)*scale;p[i+2]=-sb*ry+cb*z;
  }
  for(let i=0;i<a.length;i+=9){
   const x1=p[i],y1=p[i+1],x2=p[i+3],y2=p[i+4],x3=p[i+6],y3=p[i+7];
   if(Math.abs((x2-x1)*(y3-y1)-(y2-y1)*(x3-x1))<.02)continue;
   if(Math.max(x1,x2,x3)<0||Math.min(x1,x2,x3)>w||Math.max(y1,y2,y3)<0||Math.min(y1,y2,y3)>h)continue;
   const ax=a[i+3]-a[i],ay=a[i+4]-a[i+1],az=a[i+5]-a[i+2],bx=a[i+6]-a[i],by=a[i+7]-a[i+1],bz=a[i+8]-a[i+2];
   const nx=ay*bz-az*by,ny=az*bx-ax*bz,nz=ax*by-ay*bx,l=Math.hypot(nx,ny,nz)||1;
   const shade=Math.min(19,Math.round(7+8*Math.abs(nz/l)+3*Math.abs(nx/l)));
   tri.push([x1,y1,x2,y2,x3,y3,p[i+2],p[i+5],p[i+8],m.palette[shade]]);
  }
 }
 // Rasterize with a depth buffer; triangle sorting cannot correctly hide
 // intersecting or very long CAD tessellation faces.
 for(const t of tri){
  const [x1,y1,x2,y2,x3,y3,z1,z2,z3,color]=t;
  const area=(x2-x1)*(y3-y1)-(y2-y1)*(x3-x1);
  const xmin=Math.max(0,Math.floor(Math.min(x1,x2,x3))),xmax=Math.min(w-1,Math.ceil(Math.max(x1,x2,x3)));
  const ymin=Math.max(0,Math.floor(Math.min(y1,y2,y3))),ymax=Math.min(h-1,Math.ceil(Math.max(y1,y2,y3)));
  const a0=(y2-y3)/area,b0=(x3-x2)/area,c0=(x2*y3-x3*y2)/area;
  const a1=(y3-y1)/area,b1=(x1-x3)/area,c1=(x3*y1-x1*y3)/area;
  for(let y=ymin;y<=ymax;y++){
   let u=a0*(xmin+.5)+b0*(y+.5)+c0,v=a1*(xmin+.5)+b1*(y+.5)+c1;
   for(let x=xmin;x<=xmax;x++,u+=a0,v+=a1){
    if(u<-.000001||v<-.000001||u+v>1.000001)continue;
    const z=z3+u*(z1-z3)+v*(z2-z3),index=y*w+x;
    if(z>depth[index]){depth[index]=z;pixels[index]=color}
   }
  }
 }
 ctx.putImageData(image,0,0);
 document.querySelector('#status').textContent='Drag to rotate · Scroll to zoom · No WebGL';
 const fallback=document.querySelector('#fallback');if(fallback)fallback.style.display='none';
}
function setVisible(m,v){m.visible=v;m.input.checked=v}
document.querySelector('#explode').oninput=e=>{exp=+e.target.value;requestDraw()};
document.querySelector('#assembly').onclick=()=>{exp=0;document.querySelector('#explode').value=0;for(const m of data)setVisible(m,m.kind!=='placeholder');requestDraw()};
document.querySelector('#inside').onclick=()=>{exp=0;document.querySelector('#explode').value=0;for(const m of data)setVisible(m,!['02_upper_sleeve','04_structural_lid','05_modular_deck_NO_WIRE_HOLDER','secondary_tube_60x280','secondary_1500_turns_envelope','toroid_150x40_center_M4','07_secondary_base_clamp','10_secondary_top_clamp','11_topload_pedestal','hardware_fasteners'].includes(m.name));requestDraw()};
document.querySelector('#exploded').onclick=()=>{exp=55;document.querySelector('#explode').value=55;for(const m of data)setVisible(m,m.kind!=='hardware');requestDraw()};
document.querySelector('#iso').onclick=()=>{az=2.46;el=1.02;requestDraw()};
document.querySelector('#top').onclick=()=>{az=0;el=0;requestDraw()};
document.querySelector('#bottom').onclick=()=>{az=0;el=Math.PI;requestDraw()};
let drag=null;
canvas.onpointerdown=e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId)};
canvas.onpointerup=()=>drag=null;canvas.onpointercancel=()=>drag=null;
canvas.onpointermove=e=>{if(!drag)return;az+=(e.clientX-drag[0])*.008;el+=(e.clientY-drag[1])*.008;drag=[e.clientX,e.clientY];requestDraw()};
canvas.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(.35,Math.min(5,zoom*Math.exp(-e.deltaY*.001)));requestDraw()},{passive:false});
addEventListener('resize',requestDraw);
const view=new URLSearchParams(location.search).get('view');
if(['inside','exploded'].includes(view))document.querySelector('#'+view).click();else requestDraw();
window.caseViewer={draw:requestDraw,data,setVisible};
