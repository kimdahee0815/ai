# **DAY 1 SELF 1**

## Self 1 시작 전 한 줄 메모

.env = 잠긴 서랍, .venv = 작업실, uv = 관리인.
RNN = 귓속말 전달 (앞 내용 소실)
LSTM = 포스트잇으로 핵심만 기억
Attention = 형광펜. 프롬프트 핵심 어휘에만 집중
Transformer = 둥근 테이블 회의. Chatgpt 응답이 느린 이유
Diffusion = 노이즈 되감기. Chatgpt의 실제 이미지 생성 원리

chatgpt 프롬프트는 한번에 완결된 문장을 넘기기 때문에 RNN + LSTM/GRU 구조가 쓰이지는 않는다. 하지만, 이 한계를 극복하기 위해 Attention 구조가 쓰이는데, 프롬프트에서 특정 어휘 (ex. "고양이", "수채화", "일몰") 같은 핵심 어휘에 가중치를 두고 이미지를 생성한다.

chatgpt는 더 발전된 Transformer + LLM 구조를 쓰는데, 응답에 5~15초가 걸리는 이유가 이 구조의 병렬처리와 대규모 모델 추론 때문이다.

또한, GAN + Diffusion 을 통해서 프롬프트를 받으면 순수한 노이즈에서 시작해 점진적으로 노이즈를 제거하며 이미지를 만들어내는 원리도 쓰고 있다.

## Day 1 Self 1 개발 기록

배운점: chatgpt API를 사용해 이미지를 어떻게 생성하는지 배웠다. 막힌점은 없었는데, .env를 root 에 저장해야 된다는 것, outputs 폴더가 없으면 경로를 직접 생성할 수 있다는 것, 패키지는 uv로 설치할 수 있다는 걸 배웠다.
내일 시도할 점: 샷, 조명, 앵글을 바꿔서 장면이 어떤식으로 다르게 생성되는지 관찰해보기 위해 각각 다른 샷, 조명, 앵글 조합으로 장면 생성을 여러번 시도할 것이다.

# **DAY 1 SELF 2**

## Self 1 결과 확인

마음에 든 부분 : 카페와 횡단보도가 있다는 그림에 그려져 있다는 부분.

바꾸고 싶은 부분 : 그림 왼쪽에 중국어가 써져 있어서 그 부분은 없애고 싶다.

| 변형 | shot | angle     | lighting   | 영문 프롬프트 1줄                                                                                                                                                                                       |
| ---- | ---- | --------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A    | WS   | eye-level | rim light  | wide shot, eye-level, rim light, cloudy afternoon crosswalk, single ray of sunlight, people waiting at traffic light, soft gray sky, cafe reflection on glass, cool wind, watercolor diary illustration |
| B    | CU   | eye-level | soft front | close-up, eye-level, soft front, cloudy afternoon crosswalk, single ray of sunlight, people waiting at traffic light, soft gray sky, cafe reflection on glass, cool wind, watercolor diary illustration |
| C    | BS   | low       | backlit    | Bust shot, low angle, backlit, cloudy afternoon crosswalk, single ray of sunlight, people waiting at traffic light, soft gray sky, cafe reflection on glass, cool wind, watercolor diary illustration   |

## scene_draft_seed.md - Day 2 Self 1 입력 자료

### 일기 장면 후보 (5개)

1. 횡단보도 앞에 서 있는 사람들이 저마다 휴대폰을 보거나 가방 끈을 고쳐 메고 있다 - 후보 샷/앵글/조명: WS / eye-level / soft
2. 구름 사이로 햇빛 한 줄기가 비스듬히 내려오는 흐린 하늘 - 후보 샷/앵글/조명: WS / low / backlit
3. 맞은편 카페 유리창에 내 모습이 흐릿하게 비치는 순간 - 후보 샷/앵글/조명: MS / eye-level / rim
4. 초록 불이 켜지자 사람들이 일제히 움직이기 시작하고, 나도 그 흐름 속에 섞여 걷는다 - 후보 샷/앵글/조명: MS / eye-level / soft
5. 발아래 보도블록의 줄이 규칙적으로 지나가는 클로즈업 - 후보 샷/앵글/조명: CU / high / soft

## Gpt-image-2 와 Fal.ai 의 차이점

- gpt-image-2: response.data[0].b64_json (점 표기법)
- fal.ai: result["images"][0]["url"] (딕셔너리 키 표기법)

## Day 1 Self 2 기록

- 오늘 추가 생성: Wide Shot, Close-Up, Bust Shot 으로 샷, 조명, 앵글을 각각 다르게 한 장면을 3장 추가로 생성했다.
- 가장 차이가 크게 보인 변형: Bust Shot + Low Angle + Backlit 장면이었는데, 인물의 표정과 얼굴이 가장 크게 나타났고 기존에 배경위주였다면, 인물을 중심으로 구도가 바뀐 점이 가장 큰 변화였다.
- Day 2에서 다시 쓰고 싶은 장면 후보: Close-Up + Eye-Level + soft light 장면에서는 전체적인 거리의 분위기도 나타나면서 인물의 감정까지 보여주어서 이 장면을 가장 쓰고 싶었다.
