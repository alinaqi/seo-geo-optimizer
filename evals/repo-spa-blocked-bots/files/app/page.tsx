'use client';
import { useEffect, useState } from 'react';
export default function Home() {
  const [content, setContent] = useState<any>(null);
  useEffect(() => { fetch('/api/content/home').then(r => r.json()).then(setContent); }, []);
  if (!content) return <div>Loading...</div>;
  return (<main><h1>{content.title}</h1>{content.sections.map((s: any) => (<section key={s.id}><h2>{s.heading}</h2><p>{s.body}</p></section>))}</main>);
}
