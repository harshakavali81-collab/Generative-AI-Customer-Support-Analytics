import React from 'react';
export default function Metric({label,value,detail,icon}){return <section className="metric"><div className="metric-title"><span>{label}</span><span className="metric-icon">{icon}</span></div><div className="metric-value">{value}</div><div className="metric-note">{detail}</div></section>}
