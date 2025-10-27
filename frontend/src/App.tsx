import { useState } from "react";
const API = import.meta.env.VITE_API_BASE as string;

export default function App() {
  const [vehicle, setVehicle] = useState({ model:"SLクラス", year:2017, color:"白", price:"1168.0万円" });
  const [inquiry, setInquiry] = useState("");
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<string,string>>({});
  const [draft, setDraft] = useState("");

  const start = async () => {
    const r = await fetch(`${API}/cases`, { method:"POST", headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ vehicle, raw_inquiry: inquiry }) });
    const j = await r.json(); setQuestions(j.initial_questions || []);
  };

  const generate = async () => {
    const qa = questions.map(q=>({ key:q.key, question:q.question, answer:answers[q.key]||"", status: answers[q.key]?"answered":"unconfirmed"}));
    const r = await fetch(`${API}/cases/generate`, { method:"POST", headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ qa_items: qa, tone:"誠実",
        closing_variant:"実際にご覧いただくなら、平日と土日、どちらがご都合よろしいでしょうか？",
        future_style:"open_sport", signature_block:"〇〇株式会社／担当：〇〇\nTEL：00-0000-0000\nMAIL：info@example.com" })});
    const j = await r.json(); setDraft(j.draft_text || "");
  };

  return (
    <div style={{maxWidth:900,margin:"40px auto",fontFamily:"system-ui"}}>
      <h1>CarSensor Smart Reply (MVP)</h1>
      <h3>車両情報</h3>
      <input placeholder="モデル" value={vehicle.model} onChange={e=>setVehicle({...vehicle, model:e.target.value})}/>
      <input placeholder="年式" value={vehicle.year} onChange={e=>setVehicle({...vehicle, year:Number(e.target.value)})}/>
      <input placeholder="色" value={vehicle.color} onChange={e=>setVehicle({...vehicle, color:e.target.value})}/>
      <input placeholder="価格" value={vehicle.price} onChange={e=>setVehicle({...vehicle, price:e.target.value})}/>
      <h3>問い合わせ本文</h3>
      <textarea rows={6} value={inquiry} onChange={e=>setInquiry(e.target.value)} />
      <div><button onClick={start}>AIで質問を作る</button></div>
      {questions.length>0 && (
        <>
          <h3>確認事項に回答</h3>
          {questions.map((q:any)=>(
            <div key={q.key} style={{margin:"8px 0"}}>
              <div>{q.question}</div>
              <input value={answers[q.key]||""} onChange={e=>setAnswers({...answers, [q.key]: e.target.value})}/>
            </div>
          ))}
          <button onClick={generate}>返信文を生成</button>
        </>
      )}
      {draft && (<><h3>返信文</h3><textarea rows={12} value={draft} readOnly /><button onClick={()=>navigator.clipboard.writeText(draft)}>コピー</button></>)}
    </div>
  );
}
