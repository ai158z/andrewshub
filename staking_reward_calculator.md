# Staking Reward Calculator

## Overview
A simple Flask-based staking reward calculator that demonstrates economic utility by processing blockchain data (or mock data if APIs are unavailable).

## Formula
Rewards = Stake Amount × (1 + Annual APR)^(Duration in Years)

## Setup
1. Install dependencies:
   pip install flask
2. Run the app:
   python app.py
3. Access at http://localhost:5000

## Code
```python
from flask import Flask, request, render_template

app = Flask(__name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    stake = float(request.form['stake'])
    duration_years = float(request.form['duration'])
    apr = float(request.form['apr']) / 100
    
    rewards = stake * (1 + apr) ** duration_years - stake
    
    return render_template('index.html', rewards=rewards)

if __name__ == '__main__':
    app.run(debug=True)
```

## Templates
Create `templates/index.html`:
```html
<!doctype html>
<html>
  <head><title>Staking Rewards</title></head>
  <body>
    <h1>Staking Reward Calculator</h1>
    <form method='post' action='/calculate'>
      <label>Stake Amount ($): <input type='number' name='stake' required></label><br>
      <label>Duration (years): <input type='number' name='duration' required></label><br>
      <label>Annual APR (%): <input type='number' name='apr' required></label><br>
      <button type='submit'>Calculate</button>
    </form>
    {% if rewards is not none %}
      <h2>Estimated Rewards: ${:.2f}</h2>
    {% endif %}
  </body>
</html>
```

## Testing
Try with:
- Stake: 1000
- Duration: 1
- APR: 5%
Expected: $50.00 in rewards

## Limitations
- Simple compound formula (annual compounding)
- No real blockchain integration (mock data only)
- Frontend is basic HTML