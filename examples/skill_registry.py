from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillDefinition:
    """Skill metadata and guidance loaded from SKILL.md files."""

    id: str
    name: str
    description: str
    tags: tuple[str, ...]
    examples: tuple[str, ...]
    guidance: str


ROLE_SKILL_PATHS: dict[str, tuple[Path, ...]] = {
    "policy": (Path("skills/policy/SKILL.md"),),
    "research": (Path("skills/research/SKILL.md"),),
    "provider": (Path("skills/provider/SKILL.md"),),
    "healthcare": (Path("skills/healthcare/SKILL.md"),),
}


def _parse_skill_file(skill_path: Path) -> tuple[dict[str, str], str]:
    content = skill_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing frontmatter in {skill_path}")

    metadata: dict[str, str] = {}
    end_index = -1

    for idx, raw_line in enumerate(lines[1:], start=1):
        line = raw_line.strip()
        if line == "---":
            end_index = idx
            break
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()

    if end_index == -1:
        raise ValueError(f"Frontmatter terminator not found in {skill_path}")

    guidance = "\n".join(lines[end_index + 1 :]).strip()
    return metadata, guidance


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _split_examples(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split("|") if item.strip())


def _load_skill_definition(skill_path: Path) -> SkillDefinition:
    metadata, guidance = _parse_skill_file(skill_path)

    required = ("id", "name", "description", "tags", "examples")
    missing = [key for key in required if key not in metadata]
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(f"Missing required fields [{missing_str}] in {skill_path}")

    return SkillDefinition(
        id=metadata["id"],
        name=metadata["name"],
        description=metadata["description"],
        tags=_split_csv(metadata["tags"]),
        examples=_split_examples(metadata["examples"]),
        guidance=guidance,
    )


def get_skills(role: str) -> tuple[SkillDefinition, ...]:
    """Returns role skills by loading role-specific SKILL.md files."""
    role_paths = ROLE_SKILL_PATHS.get(role, ())
    if not role_paths:
        return ()

    base_dir = Path(__file__).resolve().parent
    return tuple(_load_skill_definition(base_dir / relative_path) for relative_path in role_paths)


def build_instruction_block(role: str) -> str:
    """Builds an instruction block so each example agent auto-applies SKILL.md guidance."""
    skills = get_skills(role)
    if not skills:
        return ""

    lines = ["Auto-attached skills from SKILL.md for this agent:"]
    for skill in skills:
        tags = ", ".join(skill.tags)
        lines.append(f"- {skill.name}: {skill.description} (tags: {tags})")
        if skill.guidance:
            lines.append("  Guidance:")
            for guidance_line in skill.guidance.splitlines():
                if guidance_line.strip():
                    lines.append(f"  - {guidance_line.strip()}")

    lines.append("Always prefer these skills when the user request matches their scope.")
    return "\n".join(lines)
