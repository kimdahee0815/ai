# 그림일기 프로젝트 - 5일 결과 회고

## Day별 핵심 산출물

| Day   | 강의 트랙                                                        | 셀프 트랙                                                             | 실행 확인 |
| ----- | ---------------------------------------------------------------- | --------------------------------------------------------------------- | --------- |
| Day 1 | 환경 구성 (.env, .venv, uv), gpt-image-2 첫 호출                 | 장면 1장 이미지 생성, outputs/ 폴더 자동 생성 확인                    | ✅        |
| Day 2 | scene_draft.md 작성 → JSON 변환, fal.ai 첫 호출                 | scene_prompts.json 수동 작성, FLUX vs GPT-IMAGE-2 비교               | ✅        |
| Day 3 | agents/scene.py로 diary.md → scene_extracted.json 자동 추출     | COMMON_STYLE 정의, gpt-image-2로 4장면 일괄 생성 (scene_1~4.png)      | ✅        |
| Day 4 | 비동기 폴링 구조 학습 (submit → status → result), 가드레일 4종 | picture_diary_pipeline() 완성, Kling으로 scene_1.mp4 생성             | ✅        |
| Day 5 | 도메인별 프롬프트 어휘 설계 (product / emoji / travel)           | domains/ JSON 3종 작성, A/B 테스트 실행, cost_report.md + README 작성 | ✅        |

## 잘 된 점

* **파이프라인 완주** : 텍스트 → 장면 추출 → 이미지 → 영상까지 end-to-end로 연결했다. `picture_diary_pipeline()` 하나로 전체 흐름이 실행된다.
* **오류를 직접 해결** : `FAL_KEY` 401 오류, `data[0]` KeyError, `requests.get().content` 누락, `video_url` NameError 등 실제 디버깅 경험을 쌓았다.
* **모델 비교 관점 확보** : FLUX(사실적)와 GPT-IMAGE-2(일러스트) 차이를 직접 생성해서 비교했고, 결과를 표로 정리했다.
* **도메인 어휘 체계화** : product / emoji / travel 세 도메인을 JSON 스키마로 분리해 재사용 가능한 구조로 만들었다.
* **비용 가시화** : 5일 누적 호출을 cost_report.md에 기록해 $0.136이라는 실측값을 남겼다.

## 개선할 점

* **프롬프트 어휘 부족** : GPT 자동 추출 장면(scene_extracted.json)은 shot·angle·lighting 어휘가 수동 작성(scene_prompts.json)보다 단순했다. 추출 프롬프트에 어휘 템플릿을 포함시켜야 한다.
* **`animate_first=False` 예외 처리 미흡** : `video_url` 초기값 없이 `if` 블록을 쓰다가 NameError가 발생했다. 변수 초기값은 분기 위에 선언하는 습관이 필요하다.
* **A/B 비교 장면 수 부족** : n_calls=3으로 P95를 계산했는데 샘플이 적어 신뢰도가 낮다. 실제 운영에서는 n=10 이상이 필요하다.

## 다음 주 시도할 것

* **프롬프트 자동 강화** : `extract_scenes()` 출력에 shot/angle/lighting 키워드를 자동으로 덧붙이는 후처리 함수 추가
* **도메인 확장** : emoji 도메인으로 실제 이미지 생성 후 product, travel과 결과 비교
* **seed 범위 확대** : A/B를 넘어 seed 5개 이상으로 분산 측정, P95 외에 중앙값도 함께 기록


## 13종 비유 카드 — 셀프 실습 연결
 
| # | 비유 카드 | 핵심 개념 | 셀프 실습 연결 | 연결 파일 |
|---|---|---|---|---|
| 1 | 전화기 게임 (귓속말 전달) | RNN - 순차 처리, 앞 내용 소실 | GPT 프롬프트는 한 호출에 완결 → RNN 순차 전달 불필요 | `diary.md` |
| 2 | 비서의 포스트잇 | LSTM - 중요 정보만 선택 기억 | 장면 추출 시 핵심 어휘(shot/angle/lighting)만 압축해 JSON에 저장 | `agents/scene.py` |
| 3 | 형광펜 치기 | Attention - 중요 단어에 가중치 | 프롬프트에서 `"golden hour"`, `"watercolor"` 같은 핵심 어휘가 이미지 결과를 결정 | `scene_prompts.json` |
| 4 | 둥근 테이블 회의 | Transformer - 병렬 Self-Attention | GPT 응답에 5~15초 걸리는 이유 = 병렬 처리 + 대규모 추론 | `pipeline.py` |
| 5 | 거대한 도서관 사서 | LLM - 사전학습 + 스케일 | `extract_scenes()`가 일기 문장을 장면 JSON으로 변환할 수 있는 근거 | `agents/scene.py` |
| 6 | 잉크 퍼짐 되감기 | Diffusion - 노이즈 점진적 제거 | GPT/FLUX가 프롬프트를 받아 노이즈에서 이미지를 복원하는 원리 | `agents/image.py` |
| 7 | 위조지폐범 vs 경찰 | GAN - 생성자/판별자 경쟁 | FLUX-schnell 내부 GAN 구조 → 사실적 이미지 출력 | `agents/image.py` |
| 8 | 잠긴 서랍 | `.env` - 비밀값 격리 | `OPENAI_API_KEY`, `FAL_KEY`를 `.env`에 보관, `.gitignore`로 push 차단 | `.env`, `check_git.py` |
| 9 | 작업실 | `.venv` - 프로젝트 격리 환경 | `uv venv`로 의존성 충돌 없이 패키지 관리 | `requirements.txt` |
| 10 | 작업실 관리인 | `uv` - 패키지 설치·관리 | `uv pip install`로 fal-client, openai 등 설치 | `requirements.txt` |
| 11 | 택배 기사 (task_id 전달) | 비동기 폴링 - submit → status → result | Kling 영상 생성: `submit_kling()` → `status_kling()` 루프 → `result_kling()` | `agents/video.py` |
| 12 | 신호등 (가드레일) | 가드레일 4종 - 반복/시간/조건/비용 제한 | `check_max_iter`, `check_timeout`, `check_predicate`, `check_budget`으로 무한 대기 방지 | `guardrails.py` |
| 13 | 보석 가게 손님 | Self-Attention - 필요한 진열대만 참조 | 도메인별 프롬프트(product/emoji/travel)에서 shot/lighting 어휘만 선택적으로 조합 | `domains/*.json` |


## GitHub 저장소

`https://github.com/kimdahee0815/picture-diary`
