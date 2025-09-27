import os
import json
from typing import Dict, Any

PROFILE_DIR = os.path.join(os.path.dirname(__file__), '../data/user_profiles')

os.makedirs(PROFILE_DIR, exist_ok=True)

def get_profile_path(user_id: str) -> str:
    return os.path.join(PROFILE_DIR, f'{user_id}.json')

def register_user(user_id: str, info: Dict[str, Any]) -> Dict[str, Any]:
    path = get_profile_path(user_id)
    if os.path.exists(path):
        return {'error': 'User already exists'}
    profile = {
        'user_id': user_id,
        'info': info,
        'progress': {},
        'history': {
            'tests': [],
            'corrections': [],
            'slang': [],
            'vision': []
        }
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    return {'success': True, 'profile': profile}

def get_user_profile(user_id: str) -> Dict[str, Any]:
    path = get_profile_path(user_id)
    if not os.path.exists(path):
        return {'error': 'User not found'}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_user_profile(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    path = get_profile_path(user_id)
    if not os.path.exists(path):
        return {'error': 'User not found'}
    with open(path, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    profile.update(updates)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    return {'success': True, 'profile': profile}

def add_history(user_id: str, module: str, record: Dict[str, Any]) -> Dict[str, Any]:
    path = get_profile_path(user_id)
    if not os.path.exists(path):
        return {'error': 'User not found'}
    with open(path, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    if module not in profile['history']:
        profile['history'][module] = []
    profile['history'][module].append(record)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    return {'success': True, 'profile': profile} 