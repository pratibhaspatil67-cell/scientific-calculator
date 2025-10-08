# app.py
from flask import Flask, request, render_template_string, jsonify
from calculator.core import sqrt, factorial, ln, power

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Scientific Calculator</title>
<h2>Scientific Calculator</h2>
<form method="post" action="/calc">
  <label>Operation:
    <select name="op">
      <option value="sqrt">√x</option>
      <option value="fact">x!</option>
      <option value="ln">ln(x)</option>
      <option value="pow">x^b</option>
    </select>
  </label>
  <br><br>
  <label>x: <input name="x" required></label>
  <br><br>
  <label>b (for power only): <input name="b"></label>
  <br><br>
  <button type="submit">Compute</button>
</form>
<div id="result"></div>
<script>
const form = document.querySelector('form');
form.addEventListener('submit', async e => {
  e.preventDefault();
  const data = new FormData(form);
  const resp = await fetch('/calc', { method: 'POST', body: data });
  const json = await resp.json();
  if (resp.ok) {
    alert('Result: ' + json.result);
  } else {
    alert('Error: ' + (json.error || 'unknown'));
  }
});
</script>
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

