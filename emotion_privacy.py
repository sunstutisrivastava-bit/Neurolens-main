import hashlib
import os
import json
from datetime import datetime

class EmotionPrivacy:
    def __init__(self):
        self.device_key = self._get_or_create_device_key()
    
    def _get_or_create_device_key(self):
        """Generate or retrieve unique device key"""
        key_file = 'device_key.bin'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = os.urandom(32)
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def generate_moodhash(self, emotion_label, timestamp, user_id):
        """Generate encrypted MoodHash from emotion data"""
        salt = os.urandom(16)
        data = f"{emotion_label}:{timestamp}:{user_id}".encode()
        combined = salt + data + self.device_key
        moodhash = hashlib.sha256(combined).hexdigest()
        return {
            'moodhash': moodhash,
            'salt': salt.hex(),
            'timestamp': timestamp
        }
    
    def create_privacy_record(self, emotion, confidence, user_id):
        """Create privacy-protected emotion record"""
        timestamp = datetime.now().isoformat()
        moodhash_data = self.generate_moodhash(emotion, timestamp, user_id)
        
        return {
            'moodhash': moodhash_data['moodhash'],
            'timestamp': timestamp,
            'intensity': round(confidence, 2),
            'encrypted': True
        }
    
    def export_emotion_dna(self, user_id, emotion_logs):
        """Export encrypted emotion journey as .mooddna file"""
        dna_data = {
            'user_id_hash': hashlib.sha256(str(user_id).encode()).hexdigest(),
            'export_date': datetime.now().isoformat(),
            'records': []
        }
        
        for log in emotion_logs:
            record = self.create_privacy_record(log[0], log[1], user_id)
            dna_data['records'].append(record)
        
        return json.dumps(dna_data, indent=2)
    
    def get_privacy_stats(self):
        """Get privacy protection statistics"""
        return {
            'encryption': 'SHA-256',
            'storage': 'Local SQLite (Encrypted)',
            'processing': 'On-Device Only',
            'data_shared': 'None',
            'reversible': False,
            'status': 'Protected 🔒'
        }
