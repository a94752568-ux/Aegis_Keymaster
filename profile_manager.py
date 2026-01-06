"""
Profile Manager Module
Handles player progression, statistics, and data persistence
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Set
from achievements import AchievementManager


class PlayerProfile:
    """Manages player profile, progression, and statistics"""
    
    def __init__(self):
        self.filename = "keymaster_profile.json"
        
        # Core progression
        self.xp = 0
        self.level = 1
        
        # Statistics
        self.total_challenges_completed = 0
        self.perfect_challenges = 0
        self.best_survival_score = 0
        self.fastest_wpm = 0
        self.total_keystrokes = 0
        self.total_errors = 0
        self.total_time_played = 0
        
        # Learning progress
        self.completed_concepts: Set[str] = set()
        self.current_learning_path = "basics"
        self.mastered_paths: Set[str] = set()
        
        # Daily challenges
        self.daily_completed = []
        self.daily_streak = 0
        self.last_daily_date = ""
        
        # Power-ups
        self.powerups = {
            "hint": 3,
            "skip": 2,
            "slow_time": 1
        }
        
        # Combo tracking
        self.highest_combo = 0
        
        # Achievement system
        self.achievement_manager = AchievementManager()
        
        self.load_profile()
    
    @property
    def rank(self) -> str:
        """Get player rank based on level"""
        ranks = {
            1: "🐣 Novato",
            5: "📜 Scripter",
            10: "💻 Coder",
            15: "🔧 Developer",
            20: "🎯 Senior Dev",
            30: "🚀 Tech Lead",
            40: "🧙 Architect",
            50: "👑 Guru",
            75: "🌟 Legend",
            100: "🤖 AI Singularity"
        }
        for lvl in sorted(ranks.keys(), reverse=True):
            if self.level >= lvl:
                return ranks[lvl]
        return "Unknown"
    
    @property
    def xp_for_next_level(self) -> int:
        """Calculate XP needed for next level"""
        return self.level * 100
    
    @property
    def accuracy(self) -> float:
        """Calculate typing accuracy percentage"""
        if self.total_keystrokes == 0:
            return 100.0
        return ((self.total_keystrokes - self.total_errors) / self.total_keystrokes) * 100
    
    def add_xp(self, amount: int) -> bool:
        """
        Add XP to player profile
        Returns True if leveled up
        """
        self.xp += amount
        self.achievement_manager.stats["total_xp_earned"] += amount
        
        leveled_up = False
        while self.xp >= self.xp_for_next_level:
            self.xp -= self.xp_for_next_level
            self.level += 1
            leveled_up = True
        
        if leveled_up:
            self.save_profile()
        
        return leveled_up
    
    def record_challenge_completion(self, wpm: int, errors: int, keystrokes: int, 
                                   concept: str = "", perfect: bool = False):
        """Record stats from a completed challenge"""
        self.total_challenges_completed += 1
        self.achievement_manager.stats["total_challenges"] += 1
        
        if perfect:
            self.perfect_challenges += 1
            self.achievement_manager.stats["perfect_challenges"] += 1
        
        if wpm > self.fastest_wpm:
            self.fastest_wpm = wpm
            self.achievement_manager.stats["fastest_wpm"] = wpm
        
        self.total_keystrokes += keystrokes
        self.total_errors += errors
        self.achievement_manager.stats["total_keystrokes"] += keystrokes
        self.achievement_manager.stats["errors_made"] += errors
        
        if concept:
            self.completed_concepts.add(concept)
            self.achievement_manager.stats["python_concepts_mastered"].add(concept)
        
        self.save_profile()
    
    def update_survival_score(self, score: int, combo: int) -> bool:
        """
        Update survival mode statistics
        Returns True if new high score
        """
        is_new_record = score > self.best_survival_score
        if is_new_record:
            self.best_survival_score = score
        
        if combo > self.highest_combo:
            self.highest_combo = combo
            self.achievement_manager.stats["highest_combo"] = combo
        
        self.achievement_manager.stats["survival_runs"] += 1
        self.save_profile()
        
        return is_new_record
    
    def update_combo(self, combo: int):
        """Update highest combo if needed"""
        if combo > self.highest_combo:
            self.highest_combo = combo
            self.achievement_manager.stats["highest_combo"] = combo
            self.save_profile()
    
    def complete_daily_challenge(self, challenge_id: int):
        """Mark a daily challenge as completed"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check streak
        if self.last_daily_date:
            last_date = datetime.strptime(self.last_daily_date, "%Y-%m-%d")
            days_diff = (datetime.now() - last_date).days
            
            if days_diff == 1:
                self.daily_streak += 1
            elif days_diff > 1:
                self.daily_streak = 1
        else:
            self.daily_streak = 1
        
        self.last_daily_date = today
        if challenge_id not in self.daily_completed:
            self.daily_completed.append(challenge_id)
        
        # Award bonus XP for daily
        self.add_xp(50)
        
        self.save_profile()
    
    def use_powerup(self, powerup_type: str) -> bool:
        """
        Use a power-up if available
        Returns True if successful
        """
        if powerup_type in self.powerups and self.powerups[powerup_type] > 0:
            self.powerups[powerup_type] -= 1
            self.save_profile()
            return True
        return False
    
    def earn_powerup(self, powerup_type: str, amount: int = 1):
        """Earn a power-up"""
        if powerup_type in self.powerups:
            self.powerups[powerup_type] += amount
            self.save_profile()
    
    def check_achievements(self) -> list:
        """Check for newly unlocked achievements"""
        player_data = {
            "level": self.level,
            "fastest_wpm": self.fastest_wpm,
            "best_survival": self.best_survival_score
        }
        
        return self.achievement_manager.check_achievements(player_data)
    
    def save_profile(self):
        """Save profile to JSON file"""
        data = {
            "xp": self.xp,
            "level": self.level,
            "total_challenges_completed": self.total_challenges_completed,
            "perfect_challenges": self.perfect_challenges,
            "best_survival_score": self.best_survival_score,
            "fastest_wpm": self.fastest_wpm,
            "total_keystrokes": self.total_keystrokes,
            "total_errors": self.total_errors,
            "total_time_played": self.total_time_played,
            "completed_concepts": list(self.completed_concepts),
            "current_learning_path": self.current_learning_path,
            "mastered_paths": list(self.mastered_paths),
            "daily_completed": self.daily_completed,
            "daily_streak": self.daily_streak,
            "last_daily_date": self.last_daily_date,
            "powerups": self.powerups,
            "highest_combo": self.highest_combo,
            "achievements": self.achievement_manager.to_dict()
        }
        
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_profile(self):
        """Load profile from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                self.xp = data.get("xp", 0)
                self.level = data.get("level", 1)
                self.total_challenges_completed = data.get("total_challenges_completed", 0)
                self.perfect_challenges = data.get("perfect_challenges", 0)
                self.best_survival_score = data.get("best_survival_score", 0)
                self.fastest_wpm = data.get("fastest_wpm", 0)
                self.total_keystrokes = data.get("total_keystrokes", 0)
                self.total_errors = data.get("total_errors", 0)
                self.total_time_played = data.get("total_time_played", 0)
                self.completed_concepts = set(data.get("completed_concepts", []))
                self.current_learning_path = data.get("current_learning_path", "basics")
                self.mastered_paths = set(data.get("mastered_paths", []))
                self.daily_completed = data.get("daily_completed", [])
                self.daily_streak = data.get("daily_streak", 0)
                self.last_daily_date = data.get("last_daily_date", "")
                self.powerups = data.get("powerups", {"hint": 3, "skip": 2, "slow_time": 1})
                self.highest_combo = data.get("highest_combo", 0)
                
                if "achievements" in data:
                    self.achievement_manager.from_dict(data["achievements"])
            except Exception as e:
                print(f"Error loading profile: {e}")
                # Keep default values if load fails
    
    def get_stats_summary(self) -> Dict:
        """Get a summary of player statistics"""
        return {
            "Level": self.level,
            "Rank": self.rank,
            "Total Challenges": self.total_challenges_completed,
            "Perfect Runs": self.perfect_challenges,
            "Fastest WPM": self.fastest_wpm,
            "Accuracy": f"{self.accuracy:.1f}%",
            "Best Survival": self.best_survival_score,
            "Highest Combo": self.highest_combo,
            "Daily Streak": self.daily_streak,
            "Achievements": f"{self.achievement_manager.get_unlocked_count()}/{self.achievement_manager.get_total_count()}"
        }