const BASE = "http://127.0.0.1:8000/api";
async function request(path:string, init?:RequestInit) {
  const r = await fetch(BASE+path, init);
  const data = await r.json().catch(()=>({detail:"Invalid server response"}));
  if(!r.ok) throw new Error(data.detail || `Request failed (${r.status})`);
  return data;
}
export const api = {
  health:()=>request("/health"),
  system:()=>request("/system"),
  loadWhisper:()=>request("/models/whisper/load",{method:"POST"}),
  loadBert:()=>request("/models/bert/load",{method:"POST"}),
  transcribe:(file:File)=>{const f=new FormData();f.append("file",file);return request("/transcribe",{method:"POST",body:f});},
  analyze:(text:string)=>request("/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})}),
  gloss:(text:string)=>request("/gloss",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})}),
  embed:(text:string)=>request("/bert/embed",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})}),
  examples:()=>request("/examples"),
  evaluate:(body:object)=>request("/evaluate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)})
};
