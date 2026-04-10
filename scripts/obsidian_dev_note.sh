#!/bin/bash

# 옵시디언 개발 학습 노트 자동 생성 스크립트
OBSIDIAN_VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
LEARNING_PATH="$OBSIDIAN_VAULT/02_Learning"
TODAY=$(date +%Y-%m-%d)

# 함수: 개발 학습 노트 생성
create_dev_note() {
    local topic="$1"
    local category="$2"
    local content="$3"
    local file_path="$LEARNING_PATH/$category/${TODAY}_${topic}.md"

    # 카테고리 폴더 생성
    mkdir -p "$LEARNING_PATH/$category"

    # 노트 생성
    cat > "$file_path" << EOF
# $topic

## 날짜
$TODAY

## 카테고리
$category

## 학습 내용
$content

## 코드 예제
\`\`\`${4:-javascript}
${5}
\`\`\`

## 핵심 포인트
${6}

## 참고 자료
${7}

---
[[_MOC_$category]]
EOF

    echo "학습 노트 생성: $file_path"
}

# 사용 예시
# create_dev_note "React Hooks 최적화" "React" "useMemo와 useCallback 활용법" "javascript" "코드 예제" "핵심 포인트" "참고 링크"