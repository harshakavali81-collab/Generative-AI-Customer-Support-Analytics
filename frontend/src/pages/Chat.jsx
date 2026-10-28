import React,{useState} from 'react';
const examples=['How long do refunds take?','Where can I track my order?','How do I reset my password?','Can I request account deletion?'];
function Citation({citation}){return <details className="citation"><summary><span className="citation-icon">◫</span> {citation.source} <small>score {citation.score.toFixed(2)}</small></summary><p>{citation.excerpt}</p><span className="citation-id">Source ID: {citation.id}</span></details>}
export default function Chat(){
  const [question,setQuestion]=useState('');
  const [messages,setMessages]=useState([{role:'assistant',answer:'Hello! I can answer questions from the fictional store support documentation. I will show the source passages used for each supported answer.',citations:[]}]);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  async function ask(value){const q=value.trim(); if(!q||loading) return; setQuestion('');setError('');setLoading(true);setMessages(v=>[...v,{role:'user',answer:q}]);
    try{const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});if(!res.ok)throw new Error('The support API returned '+res.status);const data=await res.json();setMessages(v=>[...v,{role:'assistant',...data}]);}
    catch(e){setError(e.message+' — Start the Python API or check your connection.');}
    finally{setLoading(false)}
  }
  return <section className="content">
    <div className="hero"><div><span className="eyebrow">✦ INTELLIGENT SUPPORT</span><h1>Answers grounded<br/>in <em>real evidence.</em></h1><p>Ask about the sample store policies. Every supported response links back to a documented source, with no invented policies.</p></div><div className="hero-glyph" aria-hidden="true"><span>◉</span><span>✧</span><span>◌</span></div></div>
    <div className="chat-layout"><div className="chat-panel"><div className="panel-header"><div><span className="online-dot"/> SUPPORT ASSISTANT <small>DOCUMENT-GROUNDED</small></div><span className="pill">● Available locally</span></div>
      <div className="messages" aria-live="polite">{messages.map((m,i)=><div className={'message '+m.role} key={i}><div className="avatar">{m.role==='assistant'?'✦':'Y'}</div><div className="message-main"><div className="message-label">{m.role==='assistant'?'SUPPORTLENS AI':'YOU'}</div><div className="bubble">{m.answer}</div>{m.citations?.length>0&&<div className="citations">{m.citations.map(c=><Citation citation={c} key={c.id}/>)}</div>}{m.role==='assistant'&&m.answered===false&&<div className="hint">No verified answer found. Try asking a human support agent.</div>}{m.latency_ms!==undefined&&<div className="latency">Response recorded in {m.latency_ms} ms</div>}</div></div>)}{loading&&<div className="working">✦ Searching the knowledge base…</div>}</div>
      <form className="composer" onSubmit={e=>{e.preventDefault();ask(question)}}><label htmlFor="message">ASK A SUPPORT QUESTION</label><div className="compose-row"><input id="message" maxLength={900} value={question} onChange={e=>setQuestion(e.target.value)} placeholder="e.g. When will my refund arrive?" aria-label="Support question"/><button type="submit" disabled={loading||!question.trim()}>Send <span aria-hidden="true">↗</span></button></div>{error&&<p role="alert" className="error">{error}</p>}</form></div>
      <aside className="context-panel"><h3>Try asking</h3><p>Explore common support questions</p><div className="examples">{examples.map(e=><button onClick={()=>ask(e)} disabled={loading} key={e}>{e} <span>↗</span></button>)}</div><div className="context-note"><b>◈ Evidence-first answers</b><p>Only the supplied sample documentation is used. Unknown answers are routed to human support.</p></div><div className="context-note"><b>◇ Privacy by design</b><p>Metrics contain topic and latency only. Raw question text is not saved to analytics.</p></div></aside>
    </div>
  </section>;
}
