from flask import Flask, render_template, request, jsonify
from calc import TournamentCalculator

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

DISTRIBUTION_PATTERNS = {
    'conservative': [(1.0, 1000), (2.0, 200), (5.0, 50), (10.0, 10), (50.0, 1)],
    'balanced': [(1.0, 500), (2.0, 250), (5.0, 100), (20.0, 25), (100.0, 5)],
    'volatile': [(1.0, 800), (2.0, 150), (10.0, 30), (100.0, 10), (1000.0, 1)]
}

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        pattern = data['distribution_pattern']
        base_dist = DISTRIBUTION_PATTERNS[pattern]
        
        calculator = TournamentCalculator()
        analysis = calculator.analyze_tournament(
            min_bet=float(data['min_bet']),
            max_multiplier=float(data['max_multiplier']),
            rtp=float(data['rtp']),
            tournament_prize=float(data['tournament_prize']),
            goal_multiplier=float(data['goal_multiplier']),
            expected_players=int(data['expected_players']),
            volatility=float(data['volatility']),
            base_distribution=base_dist
        )
        
        return jsonify(analysis)
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Pattern: {pattern}")
        print(f"Base distribution: {base_dist}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)