"""Data models for IncuBrix Creator Lead schema."""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class CreatorLead:
    """Represents a qualified or audited creator lead strictly conforming to the 30-column workbook format."""
    lead_id: str
    creator_name: str
    creator_segment: str
    country_iso2: str
    primary_language: str
    primary_platform: str
    profile_url: str
    stable_creator_id: str
    followers_or_subscribers: str
    last_content_date: str
    recent_content_url: str
    content_count_30d: int
    longform_count_60d: int
    monetization_signal: str
    monetization_evidence_url: str
    incubrix_need: str
    need_evidence_url: str
    best_channel: str
    channel_handle_or_url: str
    channel_evidence_url: str
    backup_channel: str
    personalization_hook: str
    first_message: str
    checked_date: str
    priority: str  # "A", "B", "C"
    lead_score: float
    candidate_status: str  # "Qualified" or "Rejected"
    rejection_reason: str = ""
    duplicate_check: str = "UNIQUE"
    completeness_check: str = "COMPLETE"

    def to_dict(self) -> Dict[str, Any]:
        """Returns standard dictionary mapping to official columns."""
        return asdict(self)

    def validate_completeness(self) -> bool:
        """Verifies if all mandatory fields required by the workbook formula are non-empty."""
        if self.candidate_status == "Rejected":
            return bool(self.rejection_reason)
        
        mandatory_fields = [
            self.creator_name,
            self.creator_segment,
            self.country_iso2,
            self.primary_language,
            self.primary_platform,
            self.profile_url,
            self.stable_creator_id,
            self.last_content_date,
            self.recent_content_url,
            self.monetization_signal,
            self.monetization_evidence_url,
            self.incubrix_need,
            self.need_evidence_url,
            self.best_channel,
            self.channel_handle_or_url,
            self.channel_evidence_url,
            self.personalization_hook,
            self.first_message,
            self.checked_date,
            self.priority,
        ]
        return all(bool(str(f).strip()) for f in mandatory_fields)
