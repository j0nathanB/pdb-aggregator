"""
Context loading and assembly for the v3 analytical pipeline.

- claims: Parse [STRUC-XX] and [PROF-XX] from dossiers and profiles
- assembly: Build system/user prompts for Phase 1 calls
"""

from .claims import extract_claims, format_claims_index, get_valid_claim_refs
from .assembly import build_system_prompt, build_call_a_user_prompt, build_call_b_user_prompt

__all__ = [
    "extract_claims",
    "format_claims_index",
    "get_valid_claim_refs",
    "build_system_prompt",
    "build_call_a_user_prompt",
    "build_call_b_user_prompt",
]
