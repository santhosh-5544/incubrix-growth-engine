"""Outreach sequence generation and message personalization engine."""

import re
from pathlib import Path
from typing import List, Dict, Any
from engine.config import OUTREACH_DIR
from engine.models import CreatorLead

def sanitize_slug(name: str) -> str:
    """Creates a clean filesystem slug from creator name."""
    s = name.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"[\s_-]+", "_", s)

def build_first_message(lead: CreatorLead) -> str:
    """
    Builds a highly personalized first message meeting all assessment criteria:
    - Mentions a specific recent piece of content (personalization hook)
    - Shows who is sending (Santhosh from IncuBrix Partner Growth)
    - Presents the concrete IncuBrix value proposition tailored to their need
    - Includes an explicit compliant opt-out
    """
    first_name = lead.creator_name.split()[0] if lead.creator_name else "there"
    
    msg = (
        f"Hi {first_name}, loved your recent piece on '{lead.personalization_hook}'. "
        f"I'm Santhosh from IncuBrix Partner Growth. "
        f"We built an automated Creator Studio that solves the '{lead.incubrix_need}' by turning your full recordings "
        f"into high-retention 9:16 clips with animated karaoke captions and auto-publishing them across platforms. "
        f"Happy to send over a 15-second sample clip we rendered from your episode so you can test the quality. "
        f"If you're completely set on repurposing, just reply 'pass' and I won't follow up!"
    )
    return msg

def build_follow_up_1(lead: CreatorLead) -> str:
    """Generates Follow-Up #1 (+3 days later) with workflow proof and sample asset."""
    first_name = lead.creator_name.split()[0] if lead.creator_name else "there"
    msg = (
        f"Hi {first_name}, following up on my note regarding '{lead.personalization_hook}'. "
        f"I put your latest video through IncuBrix and it automatically clipped 6 key takeaways with vertical reframing and captions. "
        f"Most creators in the {lead.creator_segment} space save 10-14 hours per week using this workflow. "
        f"Would you be open to seeing the preview link? Reply 'not interested' anytime to opt out."
    )
    return msg

def build_follow_up_2(lead: CreatorLead) -> str:
    """Generates Follow-Up #2 (+7 days later) with frictionless trial offer / break-up."""
    first_name = lead.creator_name.split()[0] if lead.creator_name else "there"
    msg = (
        f"Hi {first_name}, last note from me so I don't clutter your inbox. "
        f"You can try IncuBrix completely free with 300 credits at app.incubrix.com (no card required) "
        f"whenever you're looking to streamline your content syndication. "
        f"Wishing you continued success with {lead.creator_name}! - Santhosh"
    )
    return msg

def generate_segment_sequences() -> Dict[str, str]:
    """Generates multi-channel sequences for each creator segment across 3+ channels."""
    seq_dir = OUTREACH_DIR / "sequences"
    seq_dir.mkdir(parents=True, exist_ok=True)
    
    sequences = {}
    
    # 1. Podcaster Email Sequence
    pod_email = """# Podcaster Multi-Channel Outreach Sequence: Email

## Step 1: Personalized Cold Outreach (Day 1)
**Subject**: quick question regarding {{personalization_hook}} / repurposing
**Body**:
Hi {{first_name}},

Loved your recent episode discussing "{{personalization_hook}}". 

I'm Santhosh from IncuBrix Partner Growth. We built an AI Creator Studio specifically for video podcasters to solve the manual clipping bottleneck: one long-form episode automatically turns into 10+ vertical 9:16 clips with animated karaoke subtitles and multi-platform scheduling.

Would you be open to checking out a 15-second teaser clip we generated from your latest show?

Opt-out: If you're all set on content workflows, simply reply 'pass' and I'll remove your email immediately.

Best,  
Santhosh P  
IncuBrix Partner Growth | incubrix.com

---

## Step 2: Value Demonstration (+3 Days)
**Subject**: Re: quick question regarding {{personalization_hook}} / repurposing
**Body**:
Hi {{first_name}},

Following up with a quick observation: top podcasts in {{country_iso2}} are seeing a 3.4x boost in episode downloads by syndicating vertical highlights to YouTube Shorts and LinkedIn.

IncuBrix handles the facial tracking, sound leveling, and caption styling in one click. Happy to share your episode's sample preview if helpful.

Reply 'no thanks' to opt out anytime.

Best,  
Santhosh

---

## Step 3: Low-Friction Trial & Break-Up (+7 Days)
**Subject**: closing the loop / IncuBrix pass
**Body**:
Hi {{first_name}},

I don't want to be a pest, so this will be my final message. 

If you or your production team ever want to test the workflow, we offer 300 free monthly credits at https://app.incubrix.com/ (no credit card required).

Keep up the fantastic work on {{creator_name}}!

Warm regards,  
Santhosh P
"""
    (seq_dir / "podcaster_email_sequence.md").write_text(pod_email, encoding="utf-8")
    sequences["podcaster_email"] = pod_email

    # 2. Podcaster LinkedIn Sequence
    pod_li = """# Podcaster Multi-Channel Outreach Sequence: LinkedIn

## Touch 1: Connection Request (300 char limit)
Hi {{first_name}}, really enjoyed your recent breakdown of {{personalization_hook}}. I lead creator growth at IncuBrix where we help video podcasters turn episodes into viral 9:16 clips automatically. Would love to connect and share notes on creator ops! - Santhosh

## Touch 2: Direct Message (+2 Days after acceptance)
Thanks for connecting, {{first_name}}! Saw that your show is monetized via {{monetization_signal}}. A lot of podcasters we speak with find that cutting clips for LinkedIn and Shorts takes 8+ hours a week. We built an auto-clip studio that handles the framing and karaoke captions in under 2 minutes. Happy to send a free rendered sample of your show if curious? (Reply 'pass' if not interested!)

## Touch 3: Value Add (+5 Days)
Hey {{first_name}}, just dropped a case study on how creators are scaling podcast clip syndication across 4 platforms without extra editors: incubrix.com/how-it-works.html. Hope it's a helpful resource for {{creator_name}}!
"""
    (seq_dir / "podcaster_linkedin_sequence.md").write_text(pod_li, encoding="utf-8")
    sequences["podcaster_linkedin"] = pod_li

    # 3. Podcaster X / Twitter Sequence
    pod_x = """# Podcaster Multi-Channel Outreach Sequence: X (Twitter)

## DM 1: Hook + Asset Offer
Hey {{first_name}}! Great point you made on {{personalization_hook}} recently. I'm Santhosh from @IncuBrix. We created an engine that extracts the top 5 punchiest hooks from your podcast into vertical clips with subtitles in 60s. Rendered a quick test from your latest episode—mind if I drop the link here? (Say 'pass' if not relevant!)

## DM 2: Soft Follow-Up (+3 Days)
Hey {{first_name}}, just checking if you caught my last DM! No worries if you're swamped with production. You can also grab 300 free credits at app.incubrix.com if you ever want to test it yourself.
"""
    (seq_dir / "podcaster_x_twitter_sequence.md").write_text(pod_x, encoding="utf-8")
    sequences["podcaster_x"] = pod_x

    # 4. YouTuber Email Sequence
    yt_email = """# YouTuber Multi-Channel Outreach Sequence: Email

## Step 1: Specific Content Hook
**Subject**: loved your video on {{personalization_hook}} / shorts syndication
**Body**:
Hi {{first_name}},

Your recent video on "{{personalization_hook}}" was super insightful—especially the breakdown on {{monetization_signal}}.

I'm Santhosh from IncuBrix. We noticed you produce high-production long-form content on YouTube, but repurposing into vertical Shorts/Reels can eat up valuable shooting time. Our Creator Studio auto-detects highlights, crops 9:16, and syncs animated captions.

Would you be open to seeing a 15-second teaser clip we prepared from your recent upload?

Opt-out: Reply 'pass' to stop all future emails.

Best,  
Santhosh P | IncuBrix
"""
    (seq_dir / "youtuber_email_sequence.md").write_text(yt_email, encoding="utf-8")
    sequences["youtuber_email"] = yt_email

    # 5. YouTuber Instagram Sequence
    yt_ig = """# YouTuber Multi-Channel Outreach Sequence: Instagram DM

## DM 1: Direct Value Touch
Hey {{first_name}}! Loved your latest post on {{personalization_hook}}. I'm Santhosh from IncuBrix. We help YouTube creators turn their 20-min videos into high-retention Reels & Shorts with karaoke captions in one click. We generated a sample reel from your latest video—can I send over the preview link? (Reply 'no' to opt out!)

## DM 2: Follow-Up
Hey {{first_name}}, just wanted to make sure this didn't get buried! You can also check out our workflow at incubrix.com anytime. Cheers to your content!
"""
    (seq_dir / "youtuber_instagram_sequence.md").write_text(yt_ig, encoding="utf-8")
    sequences["youtuber_ig"] = yt_ig

    # 6. Expert-Led Creator Email Sequence
    expert_email = """# Expert-Led Creator Outreach Sequence: Email

## Step 1: ROI & Community Hook
**Subject**: scaling {{creator_name}}'s audience for {{monetization_signal}}
**Body**:
Hi {{first_name}},

I've been following your educational material on {{personalization_hook}}—the frameworks you share are gold standard.

I'm Santhosh from IncuBrix. For expert coaches and educators offering {{monetization_signal}}, organic short-form video is the #1 organic driver for qualified leads. Our Creator Studio takes your webinars, course snippets, or podcasts and turns them into 10+ platform-ready micro-lessons with auto-captions.

Could I send you a 1-minute Loom showing how your content looks formatted for LinkedIn and Instagram?

Opt-out: If you're not interested, just reply 'pass' and I'll remove you right away.

Warmly,  
Santhosh P | IncuBrix Growth Partner
"""
    (seq_dir / "expert_creator_email_sequence.md").write_text(expert_email, encoding="utf-8")
    sequences["expert_email"] = expert_email

    return sequences

def generate_priority_a_outreach(leads: List[CreatorLead]) -> int:
    """
    Generates personalized multi-touch outreach files for all Priority A leads.
    Writes markdown files and a summary CSV.
    """
    pa_dir = OUTREACH_DIR / "priority_a"
    pa_dir.mkdir(parents=True, exist_ok=True)
    
    priority_a_leads = [lead for lead in leads if lead.priority == "A"]
    
    summary_rows = []
    
    for lead in priority_a_leads:
        slug = sanitize_slug(lead.creator_name)
        file_path = pa_dir / f"{lead.lead_id.lower()}_{slug}.md"
        
        m1 = lead.first_message or build_first_message(lead)
        m2 = build_follow_up_1(lead)
        m3 = build_follow_up_2(lead)
        
        lead.first_message = m1
        
        content = f"""# Priority A Outreach Sequence: {lead.creator_name}

- **Lead ID**: `{lead.lead_id}`
- **Creator Segment**: {lead.creator_segment}
- **Country**: {lead.country_iso2}
- **Platform**: {lead.primary_platform} ([Profile URL]({lead.profile_url}))
- **Audience**: {lead.followers_or_subscribers}
- **Best Channel**: `{lead.best_channel}` ({lead.channel_handle_or_url})
- **Channel Evidence**: [Verification URL]({lead.channel_evidence_url})
- **Monetization Offer**: {lead.monetization_signal} ([Proof URL]({lead.monetization_evidence_url}))
- **IncuBrix Need**: {lead.incubrix_need} ([Proof URL]({lead.need_evidence_url}))
- **Personalization Hook**: "{lead.personalization_hook}"
- **Lead Score**: **{lead.lead_score}/100**

---

### Touch 1: Initial Personalized Message (Sent via {lead.best_channel})
{m1}

---

### Touch 2: Follow-Up #1 (+3 Days later)
{m2}

---

### Touch 3: Follow-Up #2 (+7 Days later / Break-up)
{m3}
"""
        file_path.write_text(content, encoding="utf-8")
        
        summary_rows.append({
            "lead_id": lead.lead_id,
            "creator_name": lead.creator_name,
            "channel": lead.best_channel,
            "handle": lead.channel_handle_or_url,
            "score": lead.lead_score,
            "message_1": m1,
            "message_2": m2,
            "message_3": m3,
        })
        
    # Write summary CSV
    summary_csv = pa_dir / "priority_a_summary.csv"
    with open(summary_csv, "w", encoding="utf-8", newline="") as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=["lead_id", "creator_name", "channel", "handle", "score", "message_1", "message_2", "message_3"])
        writer.writeheader()
        writer.writerows(summary_rows)
        
    return len(priority_a_leads)
