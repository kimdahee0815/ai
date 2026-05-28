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

## GitHub 저장소

`https://github.com/kimdahee0815/picture-diary`
