// Run the exact browser renderer without a browser/GPU and save its PNG.
const fs=require('fs'),path=require('path'),vm=require('vm'),zlib=require('zlib');
const root=__dirname,output=path.join(root,'exports');
let frame=null;
const context={createImageData:(w,h)=>({width:w,height:h,data:new Uint8ClampedArray(w*h*4)}),putImageData:image=>frame=image};
function node(){return {style:{},append(){},click(){if(this.onclick)this.onclick()},addEventListener(){},setPointerCapture(){},getContext:()=>context,width:0,height:0}}
const nodes=new Map(),document={querySelector:key=>{if(!nodes.has(key))nodes.set(key,node());return nodes.get(key)},createElement:()=>node(),createTextNode:x=>x};
const source=fs.readFileSync(path.join(root,'viewer.js'),'utf8').replace('__MESH_DATA__',fs.readFileSync(path.join(output,'viewer_meshes.json'),'utf8'));
const sandbox={console,document,innerWidth:1600,innerHeight:1000,devicePixelRatio:1,Float32Array,Uint32Array,Uint8ClampedArray,
 requestAnimationFrame:fn=>fn(),addEventListener(){},window:{},URLSearchParams,location:{search:process.argv[2]==='inside'?'?view=inside':''}};
vm.runInNewContext(source,sandbox,{timeout:60000});
if(!frame)throw Error('No rendered frame: '+document.querySelector('#status').textContent);
let colored=0;const pixels=new Uint32Array(frame.data.buffer);for(const p of pixels)if(p!==0xff201811)colored++;
if(colored<10000)throw Error('Rendered image unexpectedly empty');
function crc32(buf){let c=0xffffffff;for(const b of buf){c^=b;for(let k=0;k<8;k++)c=(c>>>1)^((c&1)?0xedb88320:0)}return (c^0xffffffff)>>>0}
function chunk(name,data){const type=Buffer.from(name),size=Buffer.alloc(4),crc=Buffer.alloc(4);size.writeUInt32BE(data.length);crc.writeUInt32BE(crc32(Buffer.concat([type,data])));return Buffer.concat([size,type,data,crc])}
const ihdr=Buffer.alloc(13);ihdr.writeUInt32BE(frame.width,0);ihdr.writeUInt32BE(frame.height,4);ihdr[8]=8;ihdr[9]=6;
const stride=frame.width*4,raw=Buffer.alloc((stride+1)*frame.height),rgba=Buffer.from(frame.data.buffer);
for(let y=0;y<frame.height;y++)rgba.copy(raw,y*(stride+1)+1,y*stride,(y+1)*stride);
const png=Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',ihdr),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))]);
const file=path.join(output,process.argv[2]==='inside'?'interior-preview.png':'case-preview.png');fs.writeFileSync(file,png);
console.log(path.basename(file)+': '+colored+' model pixels; Canvas 2D rendered successfully.');
