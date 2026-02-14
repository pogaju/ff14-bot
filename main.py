import requests

# 1. 질문자님의 디스코드 웹훅 주소 (정확한지 꼭 확인하세요!)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1472189236819005614/8u9BgqB0YDSnPFhe7njChe99IlO6P6Miwt0xPJpY3qED3VHN8lvbFJ4QceDIFRsP9NXS"

def check_paissa_api():
    # 2. 테스트용 메시지 전송 (정상 작동 확인용)
    test_payload = {"content": "📡 군힐드 알리미가 파티를 확인하는 중입니다... (정상 작동 중)"}
    requests.post(DISCORD_WEBHOOK_URL, json=test_payload)

    # 3. 실제 파티 데이터 가져오기
    url = "https://io.paissa.app/search?contents=Delubrum%20Reginae"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            parties = response.json().get('parties', [])
            if not parties:
                print("현재 사이트에 등록된 군힐드 파티가 없습니다.")
            
            for party in parties:
                send_discord_msg(party)
                print(f"✅ 파티 발견! 디코로 전송 완료: {party.get('ownerName')}")
        else:
            print(f"⚠️ 사이트 응답 없음 (코드: {response.status_code})")
                
    except Exception as e:
        print(f"연결 오류 발생: {e}")

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
            ],
            "footer": {"text": "FF14 실시간 알리미"}
        }]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    check_paissa_api()
