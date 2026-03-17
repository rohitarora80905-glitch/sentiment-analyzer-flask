from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
from collections import Counter

app = Flask(__name__, static_folder='static')
CORS(app)

# Lexicon-based sentiment analysis (no external ML libs needed)
POSITIVE_WORDS = set([
    "good","great","excellent","amazing","wonderful","fantastic","love","loved","like","liked",
    "happy","happiness","joy","joyful","best","better","brilliant","outstanding","superb",
    "positive","perfect","awesome","beautiful","enjoy","enjoyed","nice","pleasant","pleased",
    "impressive","incredible","magnificent","marvelous","terrific","delightful","splendid",
    "glad","grateful","thankful","excited","thrilled","elated","ecstatic","cheerful","satisfied",
    "helpful","useful","efficient","effective","recommend","recommended","easy","simple","clean",
    "fast","quick","reliable","trustworthy","honest","kind","friendly","polite","caring",
    "innovative","creative","smart","intelligent","talented","skilled","professional"
])

NEGATIVE_WORDS = set([
    "bad","terrible","awful","horrible","hate","hated","dislike","disliked","worst","worse",
    "poor","disappointing","disappointed","sad","unhappy","angry","frustrated","annoyed",
    "negative","ugly","disgusting","boring","dull","useless","waste","broken","failure",
    "failed","error","wrong","incorrect","slow","expensive","overpriced","rude","unfriendly",
    "difficult","complicated","confusing","unclear","unreliable","dishonest","scam","fraud",
    "problem","issue","bug","crash","miss","missed","lack","lacking","missing","never",
    "nothing","nobody","nowhere","harmful","dangerous","toxic","offensive","inappropriate"
])

INTENSIFIERS = {"very": 1.5, "extremely": 2.0, "really": 1.5, "absolutely": 2.0,
                "completely": 1.8, "totally": 1.8, "so": 1.3, "quite": 1.2, "rather": 1.1}

NEGATORS = {"not", "no", "never", "neither", "nor", "nothing", "nobody", "nowhere", "isn't",
            "aren't", "wasn't", "weren't", "don't", "doesn't", "didn't", "won't", "can't",
            "couldn't", "wouldn't", "shouldn't", "hardly", "barely", "scarcely"}

def analyze_sentiment(text):
    text_lower = text.lower()
    words = re.findall(r"\b\w+'\w+|\b\w+\b", text_lower)
    
    pos_score = 0
    neg_score = 0
    matched_pos = []
    matched_neg = []
    
    for i, word in enumerate(words):
        # Check for negation in window of 3 words before
        negated = any(words[j] in NEGATORS for j in range(max(0, i-3), i))
        # Check for intensifier just before
        multiplier = 1.0
        if i > 0 and words[i-1] in INTENSIFIERS:
            multiplier = INTENSIFIERS[words[i-1]]
        
        if word in POSITIVE_WORDS:
            if negated:
                neg_score += 1 * multiplier
                matched_neg.append(word)
            else:
                pos_score += 1 * multiplier
                matched_pos.append(word)
        elif word in NEGATIVE_WORDS:
            if negated:
                pos_score += 1 * multiplier
                matched_pos.append(word)
            else:
                neg_score += 1 * multiplier
                matched_neg.append(word)
    
    total = pos_score + neg_score
    if total == 0:
        compound = 0.0
        label = "Neutral"
        confidence = 50
    else:
        compound = (pos_score - neg_score) / total
        if compound >= 0.15:
            label = "Positive"
        elif compound <= -0.15:
            label = "Negative"
        else:
            label = "Neutral"
        confidence = int(min(99, 50 + abs(compound) * 60))
    
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    
    word_count = len(words)
    
    return {
        "label": label,
        "compound": round(compound, 3),
        "positive_score": round(pos_score / max(word_count, 1) * 100, 1),
        "negative_score": round(neg_score / max(word_count, 1) * 100, 1),
        "neutral_score": round(max(0, 100 - (pos_score + neg_score) / max(word_count, 1) * 100), 1),
        "confidence": confidence,
        "word_count": word_count,
        "matched_positive": list(set(matched_pos))[:8],
        "matched_negative": list(set(matched_neg))[:8],
        "sentence_count": len(sentences)
    }

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text too long (max 5000 chars)"}), 400
    result = analyze_sentiment(text)
    return jsonify(result)

@app.route('/batch', methods=['POST'])
def batch_analyze():
    data = request.get_json()
    texts = data.get('texts', [])
    if not texts or len(texts) > 20:
        return jsonify({"error": "Provide 1-20 texts"}), 400
    results = [analyze_sentiment(t) for t in texts if t.strip()]
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
