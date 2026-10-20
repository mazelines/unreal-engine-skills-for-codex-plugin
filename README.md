# Unreal Engine Skills for Codex

Unreal Engine 작업을 **unrealMCP + Codex agent**로 수행하는 스킬 모음입니다. 기존 Claude Code용 스킬 3개를 모두 포팅했습니다. 원본의 ToolsetRegistry C++·Python 작성 지침은 참조 문서로 유지합니다.

| 스킬 | 용도 |
| --- | --- |
| `unreal-mcp` | 에디터 조회·편집, Blueprint·에셋 작업, C++ 수정 후 빌드·검증, MCP 연결 문제 해결 |
| `create-toolset` | 사용 중인 MCP 구현에 맞는 도구 확장, Epic ToolsetRegistry C++·Python 툴셋 작성 |
| `unreal-skill` | Unreal 작업용 Codex 스킬 작성, 지원되는 엔진에서 Agent Skill 등록·수정 |

## 설치

Python 3.11 이상을 사용합니다. Windows PowerShell, macOS, Linux에서 같은 명령을 사용하며 Bash 훅은 필요 없습니다.

```powershell
# 저장소 루트에서 실행. 사용자 경로 ~/.agents/skills에 3개 모두 설치
python scripts/install_skills.py

# 특정 Unreal 프로젝트에서만 사용
python scripts/install_skills.py --project "D:/Projects/MyGame"

# 이 설치기로 설치한 스킬 갱신 (수동 편집본·동명 스킬은 덮어쓰지 않음)
python scripts/install_skills.py --update
```

기존 경로를 사용하는 환경에서는 `--destination "C:/Users/YourName/.codex/skills"`를 지정할 수 있습니다. 같은 이름을 여러 검색 경로에 중복 설치하지 마세요. 설치 후 Codex에서 `$unreal-mcp`, `$create-toolset`, `$unreal-skill`로 호출하거나 자연어로 요청합니다. 새 스킬이 보이지 않으면 새 채팅을 열거나 Codex를 재시작하세요.

루트 `plugin.json`과 `skills/`는 Agent Plugins 패키지 형식입니다. 로컬 마켓플레이스의 plugin source를 이 폴더로 지정할 수 있습니다. 스킬 직접 설치와 플러그인 설치 중 하나를 선택하세요. 공개 마켓플레이스에 배포된 상태를 뜻하지 않습니다.

## unrealMCP 연결

먼저 기존 연결을 확인합니다. `unrealMCP`, `unreal-mcp` 또는 프록시가 연결돼 있으면 재사용합니다.

```powershell
codex mcp list
codex mcp get unrealMCP

# HTTP MCP 서버가 실제 이 주소로 구동된 경우에만 추가
codex mcp add unrealMCP --url http://127.0.0.1:8000/mcp
```

프로젝트별 설정은 [examples/codex-http.toml](examples/codex-http.toml)을 참고해 `.codex/config.toml`의 기존 내용에 필요한 MCP 테이블만 병합하세요. 프로젝트 설정은 신뢰된 프로젝트에서 적용됩니다. 설치기는 MCP 설정을 변경하지 않습니다.

**서버 이름만으로 구현을 판단하지 않습니다.** Epic `ModelContextProtocol` + `ToolsetRegistry` 계열은 메타 도구를 제공할 수 있고, 별도 UnrealMCP 플러그인·Python 브리지는 개별 MCP 도구를 제공할 수 있습니다. 포트·플러그인 이름·지원 기능은 설치한 구현에서 확인합니다. 모든 서버가 `AllToolsets`, `AgentSkillToolset`, Live Coding 또는 임의 Python 실행을 지원한다고 가정하지 않습니다.

연결 절차와 STDIO 설정은 [setup.md](skills/unreal-mcp/references/setup.md), 복구는 [operations.md](skills/unreal-mcp/references/operations.md)를 참고하세요. Unreal Editor가 실행 중이어야 라이브 작업을 검증할 수 있습니다. 로컬 MCP는 실행 호스트에서 접근할 수 있어야 하며, 클라우드에 스킬을 저장하는 것만으로 로컬 에디터가 연결되지는 않습니다.

## 사용 예

```text
$unreal-mcp 현재 프로젝트와 레벨을 확인하고 액터 목록을 보여줘.
$unreal-mcp BP_Door의 잠금 변수를 수정하고 컴파일·저장 후 다시 확인해줘.
$unreal-mcp 이 Actor C++ 코드를 고치고 빌드와 에디터 검증까지 해줘.
$create-toolset 선택한 액터의 머티리얼을 조회하는 MCP 도구를 추가해줘.
$unreal-skill 이 프로젝트의 레벨 제작 규칙을 Codex 스킬로 만들어줘.
```

Claude 전용 SessionStart 훅 대신 [examples/AGENTS.unreal.md](examples/AGENTS.unreal.md)의 필요한 지침을 대상 프로젝트의 기존 `AGENTS.md`에 병합할 수 있습니다. 설치기가 프로젝트 지침을 자동으로 덮어쓰지는 않습니다.

## 검증과 클라우드 보관

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/package_skills.py
```

패키징은 `dist/`에 스킬별 ZIP과 SHA-256 파일 목록을 생성합니다. 각 ZIP에는 `SKILL.md`, 모든 참조·UI 메타데이터, 라이선스가 포함됩니다. 로컬 설치·패키징과 ChatGPT 보관함 업로드는 별도 상태입니다. 기존 클라우드 ID가 있으면 재사용하고, 본문과 참조를 함께 갱신한 뒤 확인해야 동기화 완료입니다. 업로드 실패 시 ZIP을 보존합니다.

정적 검증은 구조·참조·메타데이터·패키지 무결성을 확인합니다. 에디터 기능은 대상 엔진과 MCP 서버에서 읽기 호출, 변경 후 재조회, Blueprint/C++ 컴파일 결과로 별도 검증합니다.

## 출처

- [Codex skills](https://developers.openai.com/codex/skills/): 검색 위치와 형식.
- [Codex MCP](https://developers.openai.com/codex/mcp/): HTTP·STDIO 연결과 TOML 설정.
- [Plugin packaging](https://developers.openai.com/plugins/build/plugins): 루트 매니페스트 형식.
- [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp): 별도 MCP 구현 예시. 사용자의 설치 구현으로 단정하지 않습니다.

원본 Epic Games MIT 저작권과 라이선스를 유지합니다. 이 포트는 OpenAI 또는 Epic Games의 공식 배포라는 의미가 아닙니다.
