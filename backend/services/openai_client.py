import os, json, re
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def _force_json_array(text: str):
    m = re.search(r"\[.*\]", text, flags=re.S)
    if not m:
        return []
    try:
        return json.loads(m.group(0))
    except Exception:
        return []

def extract_questions(vehicle: dict, raw_inquiry: str) -> list[dict]:
    """
    問い合わせ文から販売担当者に確認すべき質問をJSON配列で返す。
    """
    messages = [
        {"role": "system",
         "content": "日本語で。必ずJSON配列のみを返してください。他の文章やコードブロックは禁止。"},
        {"role": "user",
         "content": (
            f"車両情報: {json.dumps(vehicle, ensure_ascii=False)}\n"
            f"問い合わせ文: {raw_inquiry}\n"
            '出力例のみ許可: '
            '[{"key":"windscreen_chip","question":"フロントガラスの飛び石傷はありますか？"}]'
         )},
    ]

    rsp = client.chat.completions.create(
        model="gpt-4o-mini",   # 安定版
        messages=messages,
        temperature=0.2,
        max_tokens=400,
    )
    text = rsp.choices[0].message.content or "[]"
    try:
        return json.loads(text)
    except Exception:
        return _force_json_array(text)

def compose_reply(payload: dict) -> str:
    """
    QAと設定から返信文を生成。
    """
    messages = [
        {"role": "system",
         "content": (
             "あなたは上質で誠実な営業ライターです。"
             "丁寧な敬語で、宛名→導入→実務回答(箇条書き)→未来描写(1段落)→二者択一→署名 の順で作成。"
             "不明は『現時点で未確認です。確認の上ご案内いたします。』と明記。"
             "過度な煽り表現は使用しないこと。"
         )},
        {"role": "user",
         "content": f"材料: {json.dumps(payload, ensure_ascii=False)}"}
    ]

    rsp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6,
        max_tokens=1200,
    )
    return (rsp.choices[0].message.content or "").strip()
