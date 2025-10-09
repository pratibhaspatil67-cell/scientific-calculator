from flask import Flask, request, render_template_string, jsonify
from calculator.core import sqrt, factorial, ln, power

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Scientific Calculator</title>
  <style>
    body {
      font-family: 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea, #764ba2);
      height: 100vh;
      margin: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .container {
      background: white;
      padding: 40px 50px;
      border-radius: 20px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.2);
      width: 350px;
      text-align: center;
      animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    h2 {
      margin-bottom: 25px;
      color: #333;
      letter-spacing: 0.5px;
    }

    select, input {
      width: 100%;
      padding: 10px;
      margin: 10px 0 20px 0;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-size: 1em;
      transition: 0.3s ease;
    }

    select:focus, input:focus {
      border-color: #667eea;
      box-shadow: 0 0 5px rgba(102,126,234,0.4);
      outline: none;
    }

    button {
      width: 100%;
      background: linear-gradient(90deg, #667eea, #764ba2);
      color: white;
      border: none;
      padding: 12px;
      border-radius: 8px;
      font-size: 1.1em;
      cursor: pointer;
      transition: background 0.3s ease;
    }

    button:hover {
      background: linear-gradient(90deg, #5a67d8, #6b46c1);
    }

    .result-box {
      margin-top: 25px;
      padding: 15px;
      background: #f1f3ff;
      border-radius: 10px;
      border: 1px solid #c3c7f3;
      display: none;
      font-size: 1.1em;
      color: #333;
    }

    .error {
      color: #e53e3e;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>🔢 Scientific Calculator</h2>
    <form method="post" action="/calc">
      <label>Operation:</label>
      <select name="op">
        <option value="sqrt">√x (Square Root)</option>
        <option value="fact">x! (Factorial)</option>
        <option value="ln">ln(x)</option>
        <option value="pow">xʸ (Power)</option>
      </select>

      <label>x:</label>
      <input name="x" placeholder="Enter value of x" required>

      <label>b (for power only):</label>
      <input name="b" placeholder="Enter value of b (optional)">

      <button type="submit">Compute</button>
    </form>

    <div id="result" class="result-box"></div>
  </div>

  <script>
  const form = document.querySelector('form');
  const resultBox = document.getElementById('result');

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = new FormData(form);
    const resp = await fetch('/calc', { method: 'POST', body: data });
    const json = await resp.json();

    resultBox.style.display = 'block';
    if (resp.ok) {
      resultBox.classList.remove('error');
      resultBox.innerHTML = '<b>✅ Result:</b> ' + json.result;
    } else {
      resultBox.classList.add('error');
      resultBox.innerHTML = '<b>⚠️ Error:</b> ' + (json.error || 'Unknown');
    }
  });
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/calc', methods=['POST'])
def calc():
    op = request.form.get('op')
    x = request.form.get('x', '')
    b = request.form.get('b', '')
    try:
        if op == 'fact':
            n = int(float(x))
            result = factorial(n)
        else:
            x_val = float(x)
            if op == 'sqrt':
                result = sqrt(x_val)
            elif op == 'ln':
                result = ln(x_val)
            elif op == 'pow':
                b_val = float(b) if b != '' else 1.0
                result = power(x_val, b_val)
            else:
                return jsonify({'error': 'Unknown op'}), 400
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
