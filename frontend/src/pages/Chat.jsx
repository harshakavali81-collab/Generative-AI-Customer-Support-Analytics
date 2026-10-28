import React,{useState} from 'react';
const examples=['How long do refunds take?','Where can I track my order?','How do I reset my password?','Can I request account deletion?'];
function Citation({citation}){return <details className="citation"><summary>◫ {citation.source} <small>score {citation.score.toFixed(2)}</small></summary><p>{citation.excerpt}</p><span className="citation-id">Source ID: {citation.id}</span></details>}
export default function Chat(){
  const [question,setQuestion]=useState('');
  const [token,setToken]=useState('');
  const [messages,setMessages]=useState([{role:'assistant',answer:'Hello! Ask about the fictional support policies. I will show the sources for supported answers.',citations:[]}]);
  const [loading,setLoading]=useState(false),[error,setError]=useState('');
  async function ask(value){
    const q=value.trim(); if(!q||loading)return;
    setQuestion('');setError('');setLoading(true);setMessages(v=>[...v,{role:'user',answer:q}]);
    try {
      const headers={'Content-Type':'application/json'};
      if(token)headers['X-Chat-Token']=token;
      const res=await fetch('/api/chat',{method:'POST',headers,body:JSON.stringify({question:q})});
      if(!res.ok)throw new Error('Support API returned HTTP '+res.status);
      const data=await res.json();
      setMessages(v=>[...v,{role:'assistant',...data,feedback:'unrated'}]);
    }catch(e){setError(e.message+' — Check backend status and access token.');}
    finally{setLoading(false)}
  }
  async function vote(index,helpful){
    const message=messages[index];
    if(!message?.request_id || message.feedback!=='unrated')return;
    try{
      const headers={'Content-Type':'application/json'};
      if(token)headers['X-Chat-Token']=token;
      const result=await fetch('/api/feedback',{method:'POST',headers,body:JSON.stringify({request_id:message.request_id,helpful})});
      if(!result.ok)throw new Error('Rating could not be saved');
      setMessages(v=>v.map((m,i)=>i===index?{...m,feedback:helpful?'helpful':'unhelpful'}:m));
    }catch(e){setError(e.message)}
  }
  return <section className="content">
    <div className="hero"><div><span className="eyebrow">✦ INTELLIGENT SUPPORT</span><h1>Answers grounded<br/>in <em>real evidence.</em></h1><p>Ask about fictional support policies. Read the source passages, or get a human-support fallback when answers are unknown.</p></div><div className="hero-glyph" aria-hidden="true"><span>◉</span><span>✧</span><span>◌</span></div></div>
    <div className="chat-layout"><div className="chat-panel"><div className="panel-header"><div><span className="online-dot"/> SUPPORT ASSISTANT <small>DOCUMENT-GROUNDED</small></div><span className="pill">● Local prototype</span></div>
      <div className="messages" aria-live="polite">{messages.map((m,i)=><div className={'message '+m.role} key={i}><div className="avatar">{m.role==='assistant'?'✦':'Y'}</div><div className="message-main"><div className="message-label">{m.role==='assistant'?'SUPPORTLENS AI':'YOU'}</div><div className="bubble">{m.answer}</div>{m.citations?.length>0&&<div className="citations">{m.citations.map(c=><Citation citation={c} key={c.id}/>)}</div>}{m.role==='assistant'&&m.answered===false&&<div className="hint">No verified answer found. Contact a human support agent.</div>}{m.latency_ms!==undefined&&<div className="latency">Response time: {m.latency_ms} ms</div>}{m.request_id&&<div className="rating">{m.feedback==='unrated'?<>Was this answer helpful? <button type="button" onClick={()=>vote(i,true)} aria-label="Rate answer helpful">Yes</button><button type="button" onClick={()=>vote(i,false)} aria-label="Rate answer unhelpful">No</button></>:<span>Rating recorded: {m.feedback}</span>}</div>}</div></div>)}{loading&&<div className="working">✦ Searching documentation…</div>}</div>
      <form className="composer" onSubmit={e=>{e.preventDefault();ask(question)}}><label htmlFor="message">ASK A SUPPORT QUESTION</label><div className="compose-row"><input id="message" maxLength={900} value={question} onChange={e=>setQuestion(e.target.value)} placeholder="e.g. When will my refund arrive?" aria-label="Support question"/><button type="submit" disabled={loading||!question.trim()}>Send ↗</button></div>{error&&<p role="alert" className="error">{error}</p>}</form></div>
      <aside className="context-panel"><h3>Try asking</h3><p>Questions about fictional policies</p><div className="examples">{examples.map(e=><button type="button" onClick={()=>ask(e)} disabled={loading} key={e}>{e} <span>↗</span></button>)}</div><div className="context-note"><b>◈ Evidence-first answers</b><p>Unsupported questions are escalated, not invented.</p></div><div className="context-note"><b>◇ Data protection</b><p>Do not enter real customer details. Analytics retain only minimal metadata, with configurable retention.</p></div><div className="context-note"><label htmlFor="chat-token"><b>Local test access token</b></label><input id="chat-token" type="password" value={token} onChange={e=>setToken(e.target.value)} placeholder="Only if API requires one" autoComplete="off" style={{marginTop:9,width:'100%',padding:10,background:'#0b1828',border:'1px solid #3e6170',borderRadius:9,color:'#fff'}}/><p>Held in page memory only. A shared API token is not a substitute for production user authentication.</p></div></aside>
    </div>
  </section>;
}
