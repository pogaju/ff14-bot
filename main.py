import requests

# 1. 질문자님의 디스코드 웹훅 주소
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1472189236819005614/8u9BgqB0YDSnPFhe7njChe99IlO6P6Miwt0xPJpY3qED3VHN8lvbFJ4QceDIFRsP9NXS"

def check_paissa_api():
    url = "https://io.paissa.app/search?contents=Delubrum%20Reginae"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            parties = response.json().get('parties', [])
            for party in parties:
                send_discord_msg(party)
        else:
            print(f"⚠️ 사이트 응답 없음 (코드: {response.status_code})")
                
    except Exception as e:
        print(f"연결 오류 발생: {e}")

def send_discord_msg(party):
    # 정보 추출
    description = party.get('description', '내용 없음')
    owner = party.get('ownerName', '알 수 없음')
    world = party.get('worldName', '알 수 없음')
    filled = party.get('slotsFilled', 0)
    total = party.get('slotsTotal', 0)
    
    # 디스코드 전송 데이터 구성
    payload = {
        "embeds": [{
            "title": "⚔️ 군힐드 사원 파티 모집 포착!",
            "description": f"**[{world}]** {owner} 님의 모집",
            "color": 3447003, # 파란색 계열
            "fields": [
                {
                    "name": "📝 파티 소개글",
                    "value": f"```{description}```",
                    "inline": False
                },
                {
                    "name": "👥 파티원 현황",
                    "value": f"**{filled}** / **{total}** 명",
                    "inline": True
                },
                {
                    "name": "🌐 서버(월드)",
                    "value": world,
                    "inline": True
                }
            ],
            "footer": {
                "text": "FF14 파티 알리미 • Paissa 데이터 기반"
            },
            "timestamp": requests.utils.quote(str("")) # 현재 시간 표시용 (생략 가능)
        }]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    check_paissa_api()
