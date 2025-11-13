from flask import Flask, render_template, request
from collections import deque
import time
import re
import os
import math

app = Flask(__name__)

# --- Data & History ---
# New constant to define the file path
ANALYZER_STORAGE_FILE = 'password.txt'

# --- MODIFICATION: Function to load passwords from password.txt ---
def load_password_list():
    """Reads passwords from password.txt, stripping whitespace and filtering out empty lines/comments."""
    try:
        with open(ANALYZER_STORAGE_FILE, 'r') as f:
            # Read lines, strip whitespace, and filter out comments (#) and empty lines
            passwords = [
                line.strip() 
                for line in f 
                if line.strip() and not line.strip().startswith('#')
            ]
        return passwords
    except FileNotFoundError:
        print(f"Warning: {ANALYZER_STORAGE_FILE} not found. Cracking simulation will use an empty list.")
        return []

# The PASSWORD_LIST is now dynamically loaded on every request (or you can load it once if performance is critical)
# For simplicity and to include newly saved passwords, we will call it inside the route or make it a global call.

# History for Search Simulation (Newest to the left/top)
search_history = deque(maxlen=5)
# History for Strength Analyzer (Changed to appendleft for newest to the top)
analyze_history = deque(maxlen=5)


CRITERIA = {
    'length': lambda p: len(p) >= 8,
    'digit': lambda p: bool(re.search(r'\d', p)),
    'upper': lambda p: bool(re.search(r'[A-Z]', p)),
    'lower': lambda p: bool(re.search(r'[a-z]', p)),
    'special': lambda p: bool(re.search(r'[!@#$%^&*()_+=\-{}[\]:;"\'<,>.?/`~]', p))
}

# --- Search Simulation Functions (Unchanged) ---

def linear_search(target, password_list, delay=0.2):
    attempts = []
    start = time.time()
    for p in password_list:
        attempts.append({"tried": p, "match": p == target})
        time.sleep(delay)
        if p == target:
            break
    end = time.time()
    found = any(a["match"] for a in attempts)
    return attempts, found, len(attempts), end - start

def binary_search(target, password_list, delay=0.2):
    arr = sorted(password_list) 
    attempts = []
    low, high = 0, len(arr) - 1
    start = time.time()
    while low <= high:
        mid = (low + high) // 2
        tried = arr[mid]
        attempts.append({"tried": tried, "match": tried == target})
        time.sleep(delay)
        if tried == target:
            break
        if target < tried: 
            high = mid - 1
        else:
            low = mid + 1
    end = time.time()
    found = any(a["match"] for a in attempts)
    return arr, attempts, found, len(attempts), end - start

# --- Function to log analyzed password to password.txt (From previous step) ---
def log_analyzed_password(password):
    """Appends the analyzed password to the password.txt file if it's not already present."""
    if not password:
        return
    
    try:
        # Read existing passwords to check for duplicates
        with open(ANALYZER_STORAGE_FILE, 'r') as f:
            existing_passwords = set(line.strip() for line in f)
    except FileNotFoundError:
        existing_passwords = set()

    if password not in existing_passwords:
        try:
            with open(ANALYZER_STORAGE_FILE, 'a') as f:
                # Add a newline character before appending the new password
                f.write(f"\n{password}")
        except Exception as e:
            print(f"Error writing to password.txt: {e}")

# --- Strength Analyzer Functions (Unchanged) ---

def calculate_entropy(password):
    """Calculates password entropy in bits."""
    length = len(password)
    if length == 0:
        return 0.0

    N = 0
    if re.search(r'[a-z]', password):
        N += 26
    if re.search(r'[A-Z]', password):
        N += 26
    if re.search(r'\d', password):
        N += 10
    if re.search(r'[!@#$%^&*()_+=\-{}[\]:;"\'<,>.?/`~]', password):
        N += 32

    if N == 0:
        return 0.0
    
    entropy_bits = length * math.log2(N)
    return entropy_bits

def format_crack_time(seconds):
    """Formats a large number of seconds into human-readable time."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    if seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    if seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} hours"
    if seconds < 31536000:
        days = seconds / 86400
        return f"{days:.1f} days"
    
    years = seconds / 31536000
    return f"{years:.1f} years"

def analyze_password_strength(password, crack_speed=10**9):
    """Analyzes strength, calculates entropy, and estimates crack time."""
    results = {
        name: check(password)
        for name, check in CRITERIA.items()
    }
    
    passed_count = sum(results.values())
    
    if passed_count == 5:
        strength = "Strong"
    elif passed_count >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    entropy_bits = calculate_entropy(password)
    total_combinations = 2**entropy_bits
    
    if crack_speed > 0:
        time_seconds = total_combinations / crack_speed
        crack_time_readable = format_crack_time(time_seconds)
    else:
        crack_time_readable = "N/A"

    stack_sim = "".join(reversed(password))
    
    results['strength'] = strength
    results['stack'] = stack_sim
    results['entropy_bits'] = round(entropy_bits, 2)
    results['crack_time'] = crack_time_readable
    results['crack_speed_gph'] = f"{crack_speed/10**9} Billion / second"
    
    return results

# --- Flask Route (Handles both GET and POST for both features) ---

@app.route('/', methods=['GET', 'POST'])
def index():
    # --- MODIFICATION: Load passwords here to ensure the list is always up-to-date --
    PASSWORD_LIST = load_password_list()
    
    context = {
        'list_size': len(PASSWORD_LIST), # This size is now the number of passwords in password.txt
        'search_history': list(search_history),
        'analyze_history': list(analyze_history),
        'active_tab': 'search' # Default tab on GET
    }

    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'search_simulation':
            context['active_tab'] = 'search'
            password = request.form.get('password', '').strip()
            
            try:
                delay = float(request.form.get('delay', '0.2'))
                if delay < 0: delay = 0.2
            except:
                delay = 0.2

            # PASSWORD_LIST is used here, which is loaded from password.txt
            linear_attempts, linear_found, linear_count, linear_time = linear_search(password, PASSWORD_LIST, delay=delay)
            sorted_list, binary_attempts, binary_found, binary_count, binary_time = binary_search(password, PASSWORD_LIST, delay=delay)

            linear_message = (f"Password found in {linear_count} attempts using Linear Search." if linear_found
                              else f"Password NOT found after {linear_count} attempts using Linear Search.")
            binary_message = (f"Password found in {binary_count} attempts using Binary Search." if binary_found
                              else f"Password NOT found after {binary_count} attempts using Binary Search.")

            search_history.appendleft({"password": password,
                                "linear": f"{linear_count} attempts ({'found' if linear_found else 'not found'})",
                                "binary": f"{binary_count} attempts ({'found' if binary_found else 'not found'})"})

            context.update({
                "linear_attempts": linear_attempts,
                "binary_attempts": binary_attempts,
                "linear_message": linear_message,
                "binary_message": binary_message,
                "linear_time": linear_time,
                "binary_time": binary_time,
                "linear_count": linear_count,
                "binary_count": binary_count,
                "sorted_list": sorted_list,
                "delay": delay
            })
            context['search_history'] = list(search_history)
            context['list_size'] = len(PASSWORD_LIST) # Update list size in context

        elif form_type == 'strength_analyzer':
            context['active_tab'] = 'analyze'
            password = request.form.get('analyze_password', '')
            
            # 1. Store the password in password.txt (Saves it for future cracking simulations)
            log_analyzed_password(password)
            
            # 2. Analyze the password
            result = analyze_password_strength(password) 
            
            history_item = {
                'password': password,
                'strength': result['strength']
            }
            analyze_history.appendleft(history_item)
            
            context['analyze_result'] = result
            context['analyze_history'] = list(analyze_history)

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True, port=5001)