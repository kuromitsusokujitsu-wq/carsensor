import os, json
from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def extract_questions(vehicle: dict, raw_inquiry: str) -> list[dict]:
    prompt = f"車両情報: {json.dumps(vehicle, ensure_ascii=False)}\n問い合わせ文: {raw_inquiry}\n"
    rsp = client.responses.create(
        model="gpt-5",
        input=[{"role":"system","content": "日本語で出力。"},
               {"role":"user","content": f"以下を読み取り、必要質問をJSON配列で:\n{prompt}"}]
    )
    text = rsp.output_text
    try:
        return json.loads(text)
    except Exception:
        return []

def compose_reply(payload: dict) -> str:
    payload_text = json.dumps(payload, ensure_ascii=False)
    rsp = client.responses.create(
        model="gpt-5",
        input=[{"role":"system","content": "日本語で。"},
               {"role":"user","content": f"以下の材料で返信文を生成:\n{payload_text}"}]
    )
    return rsp.output_text.strip()
