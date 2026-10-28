import React, {useState} from 'react';
import Chat from './pages/Chat';
import Analytics from './pages/Analytics';
export default function App(){
  const [page,setPage]=useState('chat');
  return <div className="shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-icon">✦</span><span><b>SupportLens</b><small>AI INTELLIGENCE</small></span></div>
      <div className="section-label">WORKSPACE</div>
      <nav aria-label="Primary"><button className={page==='chat'?'active':''} onClick={()=>setPage('chat')}>◈ <span>AI Support Chat</span></button><button className={page==='analytics'?'active':''} onClick={()=>setPage('analytics')}>▤ <span>Analytics Center</span></button></nav>
      <div className="sidebar-bottom"><span className="online-dot"/> Offline-first RAG<div className="muted-sm">Fictional example documents only</div></div>
    </aside>
    <main className="main">
      <header className="topbar"><span className="crumb">WORKSPACE <span>/</span> {page==='chat'?'AI Support Chat':'Analytics Center'}</span><span className="top-chip">✧ PORTFOLIO DEMO</span></header>
      {page==='chat'?<Chat/>:<Analytics/>}
      <footer>SupportLens AI · All support policies are fictional. No private customer data is needed for this demo.</footer>
    </main>
  </div>
}
