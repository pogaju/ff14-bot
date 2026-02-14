import requests
import time

# 질문자님의 디스코드 웹훅 주소
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1472189236819005614/8u9BgqB0YDSnPFhe7njChe99IlO6P6Miwt0xPJpY3qED3VHN8lvbFJ4QceDIFRsP9NXS"

def check_paissa_api():
    url = "https://io.paissa.app/search?contents=Delubrum%20Reginae"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            parties = response.json().get('parties', [])
            for party in parties:
                # 깃허브 액션은 매번 새로 실행되므로 ALREADY_SEEN 없이 모든 파티를 보냅니다.
                send_discord_msg(party)
                print(f"✅ 새 파티 발견! 디코로 전송 완료")
    except Exception as e:
        print(f"연결 오류: {e}")

def send_discord_msg(party):
    title = party.get('description') if party.get('description') else "소개말 없음"
    payload = {
        "embeds": [{
            "title": "🔔 군힐드 사원 파티 포착!",
            "description": f"**제목:** {title}\n**모집자:** {party.get('ownerName')}",
            "color": 15844367,
            "fields": [
                {"name": "인원", "value": f"{party.get('slotsFilled')}/{party.get('slotsTotal')}", "inline": True},
                {"name": "월드", "value": party.get('worldName'), "inline": True}
            ]
        }]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    check_paissa_api()
