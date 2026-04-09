#!/usr/bin/env /opt/homebrew/bin/python3.11
"""
Sanskrit Word Explorer — Local server with Claude API fallback.

Serves the static demo and provides /api/analyze for arbitrary terms.
Tier 1 (20 pre-analyzed terms) is handled client-side.
Tier 2 (any Sanskrit term) calls Claude API via this server.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python3.11 demo/server.py

Then open http://localhost:8765
"""

import http.server
import json
import os
import sys

# ── CONFIG ──
PORT = 8765
DEMO_DIR = os.path.dirname(os.path.abspath(__file__))

SYSTEM_PROMPT = """You are a Sanskrit morphological analyzer for a philosophy class project.

Given a Sanskrit term (in Devanagari, IAST, or informal romanization), return a JSON object with exactly these fields:

{
  "id": "normalized_slug",
  "devanagari": "term in Devanagari",
  "transliteration": "IAST with diacritics",
  "chapter": "YS references if applicable, or relevant text references",
  "segmentation": "prefix + root + suffix breakdown",
  "roots": [{"root": "√dhā", "devanagari": "√धा", "meaning": "to place", "dhatu_number": null}],
  "prefixes": [{"prefix": "sam-", "meaning": "together"}],
  "suffixes": [{"suffix": "-i", "meaning": "action noun", "grammatical_function": "forms masculine action noun"}],
  "compound_type": null,
  "literal_gloss": "compositional meaning from parts",
  "philosophical_gloss": "how the term functions in Yoga/Buddhist philosophy",
  "doctrinal_significance": "why this term matters (1-3 sentences)",
  "ambiguity_notes": null,
  "confidence": "high or medium or low",
  "chinese_counterparts": null,
  "search_aliases": ["slug", "transliteration"],
  "ai_generated": true
}

Guidelines:
- Always provide Devanagari + IAST transliteration.
- Use standard IAST with diacritics.
- Cite Yoga Sutras by number (YS 1.2) when relevant.
- If a derivation is debated, note it in ambiguity_notes.
- Do NOT fabricate etymologies. If uncertain, say so and set confidence to "low".
- Prefer Monier-Williams and Apte as implicit references.
- Return ONLY the JSON object, no markdown, no explanation outside the JSON."""


class DemoHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DEMO_DIR, **kwargs)

    def do_POST(self):
        if self.path == '/api/analyze':
            self.handle_analyze()
        else:
            self.send_error(404)

    def handle_analyze(self):
        # Read request body
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        term = body.get('term', '').strip()

        if not term:
            self.send_json(400, {'error': 'No term provided'})
            return

        api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        if not api_key:
            self.send_json(500, {'error': 'ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY=sk-ant-...'})
            return

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": f"Analyze this Sanskrit term: {term}"}],
            )

            # Extract JSON from response
            response_text = message.content[0].text.strip()
            # Handle potential markdown code blocks
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0].strip()

            result = json.loads(response_text)
            result['ai_generated'] = True
            self.send_json(200, result)

        except json.JSONDecodeError:
            self.send_json(500, {'error': 'AI returned invalid JSON', 'raw': response_text[:500]})
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def send_json(self, code, data):
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(response))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Cleaner logging
        if '/api/' in (args[0] if args else ''):
            sys.stderr.write(f"  API: {args[0]}\n")


def main():
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    print(f"\n  Sanskrit Word Explorer")
    print(f"  {'─' * 40}")
    print(f"  Server:  http://localhost:{PORT}")
    print(f"  API key: {'✓ set' if api_key else '✗ not set (Tier 2 disabled)'}")
    if not api_key:
        print(f"  To enable Tier 2: export ANTHROPIC_API_KEY=sk-ant-...")
    print(f"  {'─' * 40}")
    print(f"  Tier 1: 20 pre-analyzed terms (always works)")
    print(f"  Tier 2: any Sanskrit term via Claude API")
    print(f"  {'─' * 40}\n")

    server = http.server.HTTPServer(('', PORT), DemoHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == '__main__':
    main()
