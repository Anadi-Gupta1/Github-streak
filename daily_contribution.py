#!/usr/bin/env python3
import os
import json
import datetime
import random
import time
from pathlib import Path

def load_stats():
    """Load contribution statistics from JSON file or create if not exists."""
    stats_file = Path("contribution_data.json")
    streak_file = Path("streak_stats.json")
    
    if stats_file.exists():
        with open(stats_file, "r") as f:
            stats = json.load(f)
    else:
        stats = {"total_contributions": 0, "last_contribution": None}
    
    if streak_file.exists():
        with open(streak_file, "r") as f:
            streak = json.load(f)
    else:
        streak = {"current_streak": 0, "longest_streak": 0, "start_date": None}
        
    return stats, streak

def update_stats(stats, streak):
    """Update contribution statistics and streak information."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Update total contributions
    stats["total_contributions"] += 1
    
    # Update streak information
    if stats["last_contribution"] == yesterday or stats["last_contribution"] is None:
        # Continuing streak or first contribution
        if streak["current_streak"] == 0:
            streak["start_date"] = today
        streak["current_streak"] += 1
        if streak["current_streak"] > streak["longest_streak"]:
            streak["longest_streak"] = streak["current_streak"]
    elif stats["last_contribution"] != today:
        # Streak broken
        streak["current_streak"] = 1
        streak["start_date"] = today
    
    stats["last_contribution"] = today
    
    # Save updated stats
    with open("contribution_data.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    with open("streak_stats.json", "w") as f:
        json.dump(streak, f, indent=2)
    
    # Update README with stats
    update_readme(stats["total_contributions"], streak["current_streak"], streak["longest_streak"])
    
    return stats, streak

def update_readme(total, current_streak, longest_streak):
    """Update README.md with current statistics."""
    with open("README.md", "r") as f:
        content = f.read()
    
    # Update stats in README
    content = content.replace(f"Total contributions: {total-1}", f"Total contributions: {total}")
    content = content.replace(f"Current streak: {current_streak-1} days", f"Current streak: {current_streak} days")
    
    if current_streak > longest_streak-1:
        content = content.replace(f"Longest streak: {longest_streak-1} days", f"Longest streak: {longest_streak} days")
    
    with open("README.md", "w") as f:
        f.write(content)

def update_log(stats, streak):
    """Update contribution log with details of this contribution."""
    log_file = Path("contribution_log.md")
    
    if not log_file.exists():
        with open(log_file, "w") as f:
            f.write("# Contribution Log\n\n")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a") as f:
        f.write(f"\n## Contribution on {timestamp}\n")
        f.write(f"- Total contributions: {stats['total_contributions']}\n")
        f.write(f"- Current streak: {streak['current_streak']} days\n")
        f.write(f"- Longest streak: {streak['longest_streak']} days\n")

def create_daily_file():
    """Create a unique file for today's contribution."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    daily_dir = Path("daily_contributions")
    daily_dir.mkdir(exist_ok=True)
    
    file_path = daily_dir / f"contribution_{timestamp}.md"
    
    with open(file_path, "w") as f:
        f.write(f"# Daily Contribution - {timestamp}\n\n")
        f.write(f"This file was automatically generated on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}.\n\n")
        f.write("## Random Quote\n\n")
        
        quotes = [
            "The best way to predict the future is to create it.",
            "Success is not final, failure is not fatal: It is the courage to continue that counts.",
            "The only way to do great work is to love what you do.",
            "Believe you can and you're halfway there.",
            "It does not matter how slowly you go as long as you do not stop.",
            "Quality is not an act, it is a habit.",
            "The secret of getting ahead is getting started.",
            "Don't watch the clock; do what it does. Keep going.",
            "The future belongs to those who believe in the beauty of their dreams.",
            "You are never too old to set another goal or to dream a new dream."
        ]
        
        f.write(f"> {random.choice(quotes)}\n")
    
    return file_path

def main():
    """Main function to make daily contributions."""
    num_contributions = random.randint(20, 25)  # Random number between 20-25
    
    stats, streak = load_stats()
    
    for i in range(num_contributions):
        file_path = create_daily_file()
        print(f"Created file: {file_path}")
        
        # Update stats and log for each contribution
        stats, streak = update_stats(stats, streak)
        update_log(stats, streak)
        
        # Sleep for a random interval to space out commits
        if i < num_contributions - 1:
            sleep_time = random.uniform(1, 3)
            time.sleep(sleep_time)
    
    print(f"Made {num_contributions} contributions successfully.")
    print(f"Current streak: {streak['current_streak']} days")
    print(f"Total contributions: {stats['total_contributions']}")

if __name__ == "__main__":
    main()
