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

## Gpt-image-2 와 Fal.ai 의 차이점

- gpt-image-2: response.data[0].b64_json (점 표기법)
- fal.ai: result["images"][0]["url"] (딕셔너리 키 표기법)

## Day 1 Self 2 개발 기록

- 오늘 추가 생성: Wide Shot, Close-Up, Bust Shot 으로 샷, 조명, 앵글을 각각 다르게 한 장면을 3장 추가로 생성했다.
- 가장 차이가 크게 보인 변형: Bust Shot + Low Angle + Backlit 장면이었는데, 인물의 표정과 얼굴이 가장 크게 나타났고 기존에 배경위주였다면, 인물을 중심으로 구도가 바뀐 점이 가장 큰 변화였다.
- Day 2에서 다시 쓰고 싶은 장면 후보: Close-Up + Eye-Level + soft light 장면에서는 전체적인 거리의 분위기도 나타나면서 인물의 감정까지 보여주어서 이 장면을 가장 쓰고 싶었다.

# **DAY 2 SELF 1**

## Day 2 Self 1 개발 기록

- 오늘 만든 파일: scene_draft.md, day2_self1.py
- 장면 1: 횡단보도 전체 풍경을 보여주는 도입부라 WS(Wide-Shot)와 24mm로 넓은 공간을 담았다.
- 장면 2: 유리창 반사라는 좌우 대칭 구도가 핵심이라 symmetric과 rim light로 윤곽을 살렸다.
- 장면 3: 신호가 바뀌며 사람들이 움직이는 역동적인 순간이라 low angle과 backlit으로 에너지를 강조했다.
- 장면 4: 보도블록 줄이 시선을 이끄는 마무리 장면이라 CU(Close-Up)와 85mm로 발밑에 집중했다.
- 가장 어려웠던 선택: 장면 2에서 카페 유리창 반사 장면을 MS로 할지 CU로 할지 고민했다. 반사된 주인공 모습 전체를 보여주고 싶어서 MS를 골랐지만, 유리창 질감을 더 강조하려면 CU도 괜찮을 것 같았다.
- 다음 self2에서 확인할 것: scene_draft.md를 JSON으로 변환할 때 prompt_en 키워드가 이미지 생성에 충분한지 확인한다.
- 막혔던 점: re.split으로 장면을 나눌 때 ## 장면 1 앞부분이 sections[0]에 들어가서
  scene_idx + 1로 접근해야 한다는 걸 몰랐다.

# **DAY 2 SELF 2**

## Fal.ai 와 Gpt-image-2의 차이점

| 모델         | 분위기                                     | 디테일                                                                   | 응답 구조                  |
| ------------ | ------------------------------------------ | ------------------------------------------------------------------------ | -------------------------- |
| Gpt-image-2  | 그림일기처럼 따뜻하고 일러스트 느낌이 강함 | 전반적으로 잘 살아있으나 가방 고치기나 핸드폰 보기 같은 세부 행동은 부족 | response.data[0].url       |
| FLUX-schnell | 실제 사진처럼 사실적이고 현실감이 강함     | 인물은 있으나 가방 고치기나 핸드폰 보기 같은 지정 행동이 표현되지 않음   | result["images"][0]["url"] |

## Day 2 Self 2 개발 기록 - scene_prompts.json + fal.ai 첫 호출

- 완료 시각: 11:06
- 생성 파일: scene_prompts.json, day2_self2.py, outputs/scene01_fal.png
- FLUX vs GPT-IMAGE-2 차이: FLUX는 사진처럼 사실적인 느낌이 강했고, GPT-IMAGE-2는 그림일기 같은 일러스트 느낌이 강했다. 디테일 면에서는 둘 다 가방 고치기나 핸드폰 보기 같은 세부 행동은 잘 표현되지 않았다.
- 막힌 부분:
    1. FAL_KEY가 잘못 설정되어 있어 401 오류 발생 -> .env에서 키 교체로 해결
    2. scene_prompts.json 구조가 리스트가 아닌 딕셔너리라 `data[0]`이 KeyError -> `data["scenes"][0]["prompt_en"]`으로 수정
    3. `requests.get(url)` 반환값을 그대로 write_bytes에 넘겨 TypeError 발생 -> `.content` 추가로 해결
