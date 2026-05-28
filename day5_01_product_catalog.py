from typing import Literal

shot_type= Literal["close-up", "macro", "medium_shot", "full_shot"]

products=[
    {
        "name": "earbuds",
        "desc": "화이트 색상, 미니멀 디자인, 충전 케이스 포함"
    },
    {
        "name": "tumbler",
        "desc": "매트 블랙, 스테인리스 소재, 450ml 용량"
    }, 
    {
        "name": "keyboard",
        "desc": "기계식, 화이트 키캡, RGB 백라이트, 텐키리스"
    }
]

shot_map: dict[str, shot_type] = {
    "small": "macro", # 이어폰, 반지, 시계
    "medium": "close-up", # 텀블러, 키보드, 책
    "large": "full_shot" # 가방, 신발, 소형 가전
}

angle_map = {
    "tall": "eye-level angle", # 텀블러, 긴 병
    "flat": "slight high angle view", # 키보드, 책, 태블릿
    "small": "bird's eye view to-down" # 이어폰, 반지, 동전
}
