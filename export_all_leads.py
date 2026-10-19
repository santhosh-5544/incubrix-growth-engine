import csv
import json
import os

leads = list(csv.DictReader(open('output/leads.csv', encoding='utf-8')))
print(f'Total leads in CSV: {len(leads)}')
all_leads = []
for l in leads:
    all_leads.append({
        'lead_id': l['lead_id'],
        'name': l['creator_name'],
        'segment': l['creator_segment'],
        'country': l['country_iso2'],
        'platform': l['primary_platform'],
        'profile_url': l['profile_url'],
        'followers': l['followers_or_subscribers'],
        'content_30d': l['content_count_30d'],
        'content_60d': l['longform_count_60d'],
        'monetization': l['monetization_signal'],
        'monetization_url': l['monetization_evidence_url'],
        'need': l['incubrix_need'],
        'need_url': l['need_evidence_url'],
        'best_channel': l['best_channel'],
        'channel_contact': l['channel_handle_or_url'],
        'backup_channel': l['backup_channel'],
        'hook': l['personalization_hook'],
        'first_message': l['first_message'],
        'priority': l['priority'],
        'score': float(l['lead_score']),
        'status': l['candidate_status']
    })

with open('all_leads.json', 'w', encoding='utf-8') as f:
    json.dump(all_leads, f)

print(f"Dumped all {len(all_leads)} leads. File size: {os.path.getsize('all_leads.json')} bytes")
