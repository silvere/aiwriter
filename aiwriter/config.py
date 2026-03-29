import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class VaultConfig:
    path: Path
    articles_folder: str = "AI-Articles"
    images_folder: str = "attachments"


@dataclass
class StyleConfig:
    default: str = "wechat"  # "wechat" or "xiaohongshu"
    default_language: str = "zh"


@dataclass
class ImagesConfig:
    prefer_web_search: bool = True
    max_images_per_section: int = 2
    min_image_width: int = 800


@dataclass
class SearchConfig:
    max_results: int = 8


@dataclass
class LLMConfig:
    writing_model: str = "claude-sonnet-4-6"
    auxiliary_model: str = "claude-haiku-4-5-20251001"


@dataclass
class Config:
    vault: VaultConfig
    style: StyleConfig = field(default_factory=StyleConfig)
    images: ImagesConfig = field(default_factory=ImagesConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)

    # API keys (from env)
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    unsplash_access_key: Optional[str] = None
    pexels_api_key: Optional[str] = None

    # Feature flags
    has_anthropic: bool = False
    has_openai: bool = False
    has_tavily: bool = False
    has_unsplash: bool = False
    has_pexels: bool = False
    has_ai_image: bool = False  # True if has_openai (for DALL-E)


def _find_file(filename: str) -> Optional[Path]:
    """Search for a file in current dir then ~/.config/aiwriter/."""
    candidates = [
        Path.cwd() / filename,
        Path.home() / ".config" / "aiwriter" / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _load_toml(path: Path) -> dict:
    """Load a TOML file using tomllib (3.11+) or tomli (3.9/3.10)."""
    if sys.version_info >= (3, 11):
        import tomllib
        with open(path, "rb") as f:
            return tomllib.load(f)
    else:
        import tomli
        with open(path, "rb") as f:
            return tomli.load(f)


def load_config() -> Config:
    """Load configuration from config.toml and .env files."""
    # Load .env first
    env_path = _find_file(".env")
    if env_path:
        from dotenv import load_dotenv
        load_dotenv(env_path)

    # Load config.toml
    config_path = _find_file("config.toml")
    raw: dict = {}
    if config_path:
        raw = _load_toml(config_path)

    # --- Vault ---
    vault_raw = raw.get("vault", {})
    vault_path_str = vault_raw.get("path", "")
    if not vault_path_str:
        from rich.console import Console
        Console().print(
            "[bold red]Error:[/bold red] vault.path is not configured.\n\n"
            "Please create a config.toml with:\n\n"
            "  [vault]\n"
            '  path = "~/Documents/Obsidian/MyVault"\n\n'
            "Copy config.toml.example to config.toml and edit it, or place it at "
            "~/.config/aiwriter/config.toml"
        )
        sys.exit(1)

    vault_path = Path(vault_path_str).expanduser().resolve()
    if not vault_path.exists():
        from rich.console import Console
        Console().print(
            f"[bold red]Error:[/bold red] Vault path does not exist: {vault_path}\n\n"
            "Please check your config.toml vault.path setting."
        )
        sys.exit(1)

    obsidian_dir = vault_path / ".obsidian"
    if not obsidian_dir.exists():
        from rich.console import Console
        Console().print(
            f"[bold red]Error:[/bold red] {vault_path} does not appear to be an Obsidian vault "
            f"(missing .obsidian directory).\n\n"
            "Please point vault.path to the root of your Obsidian vault."
        )
        sys.exit(1)

    vault = VaultConfig(
        path=vault_path,
        articles_folder=vault_raw.get("articles_folder", "AI-Articles"),
        images_folder=vault_raw.get("images_folder", "attachments"),
    )

    # --- Style ---
    style_raw = raw.get("style", {})
    style = StyleConfig(
        default=style_raw.get("default", "wechat"),
        default_language=style_raw.get("default_language", "zh"),
    )

    # --- Images ---
    images_raw = raw.get("images", {})
    images = ImagesConfig(
        prefer_web_search=images_raw.get("prefer_web_search", True),
        max_images_per_section=images_raw.get("max_images_per_section", 2),
        min_image_width=images_raw.get("min_image_width", 800),
    )

    # --- Search ---
    search_raw = raw.get("search", {})
    search = SearchConfig(
        max_results=search_raw.get("max_results", 8),
    )

    # --- LLM ---
    llm_raw = raw.get("llm", {})
    llm = LLMConfig(
        writing_model=llm_raw.get("writing_model", "claude-sonnet-4-6"),
        auxiliary_model=llm_raw.get("auxiliary_model", "claude-haiku-4-5-20251001"),
    )

    # --- API keys from environment ---
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY") or None
    openai_api_key = os.environ.get("OPENAI_API_KEY") or None
    tavily_api_key = os.environ.get("TAVILY_API_KEY") or None
    unsplash_access_key = os.environ.get("UNSPLASH_ACCESS_KEY") or None
    pexels_api_key = os.environ.get("PEXELS_API_KEY") or None

    has_anthropic = bool(anthropic_api_key)
    has_openai = bool(openai_api_key)
    has_tavily = bool(tavily_api_key)
    has_unsplash = bool(unsplash_access_key)
    has_pexels = bool(pexels_api_key)
    has_ai_image = has_openai  # DALL-E requires OpenAI

    return Config(
        vault=vault,
        style=style,
        images=images,
        search=search,
        llm=llm,
        anthropic_api_key=anthropic_api_key,
        openai_api_key=openai_api_key,
        tavily_api_key=tavily_api_key,
        unsplash_access_key=unsplash_access_key,
        pexels_api_key=pexels_api_key,
        has_anthropic=has_anthropic,
        has_openai=has_openai,
        has_tavily=has_tavily,
        has_unsplash=has_unsplash,
        has_pexels=has_pexels,
        has_ai_image=has_ai_image,
    )
