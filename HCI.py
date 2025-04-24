from flask import Flask, request, render_template_string
import re
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LegalEase Assistant</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #2c3e50;
            --secondary: #3498db;
            --accent: #e74c3c;
            --light: #ecf0f1;
            --dark: #2c3e50;
            --success: #27ae60;
            --warning: #f39c12;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Roboto', sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background-color: #f5f7fa;
            padding: 0;
            margin: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        header {
            background-color: var(--primary);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .tagline {
            font-weight: 300;
            opacity: 0.9;
        }
        
        .main {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        @media (max-width: 768px) {
            .main {
                grid-template-columns: 1fr;
            }
        }
        
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .card-header {
            background-color: var(--primary);
            color: white;
            padding: 1rem 1.5rem;
            font-weight: 500;
        }
        
        .card-body {
            padding: 1.5rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        select, textarea {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        select:focus, textarea:focus {
            outline: none;
            border-color: var(--secondary);
        }
        
        textarea {
            min-height: 150px;
            resize: vertical;
        }
        
        .btn {
            display: inline-block;
            background-color: var(--secondary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.3s;
            text-align: center;
        }
        
        .btn:hover {
            background-color: #2980b9;
        }
        
        .btn-block {
            display: block;
            width: 100%;
        }
        
        .result-container {
            margin-top: 2rem;
            border-top: 1px solid #eee;
            padding-top: 1.5rem;
        }
        
        .result-title {
            font-weight: 500;
            margin-bottom: 1rem;
            color: var(--primary);
            display: flex;
            align-items: center;
        }
        
        .result-title svg {
            margin-right: 0.5rem;
        }
        
        .result-content {
            background-color: var(--light);
            padding: 1rem;
            border-radius: 4px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.7;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .highlight {
            background-color: rgba(255, 255, 0, 0.3);
            padding: 0 2px;
        }
        
        footer {
            text-align: center;
            padding: 2rem 0;
            color: #7f8c8d;
            font-size: 0.9rem;
        }
        
        .watermark {
            opacity: 0.6;
            font-size: 0.8rem;
        }
        
        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animated {
            animation: fadeIn 0.5s ease-out;
        }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div>
                <h1>LegalEase Assistant</h1>
                <p class="tagline">Your smart legal document companion</p>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="main">
            <div class="card">
                <div class="card-header">
                    Document Drafting
                </div>
                <div class="card-body">
                    <form action="/draft" method="post">
                        <div class="form-group">
                            <label for="doc_type">Document Type</label>
                            <select id="doc_type" name="doc_type">
                                <option value="nda">Non-Disclosure Agreement</option>
                                <option value="contract">Service Contract</option>
                                <option value="will">Last Will</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="details">Describe Your Needs</label>
                            <textarea id="details" name="details" placeholder="Example: 'I need an NDA between my tech startup and a potential investor for 2 years protecting our software designs'"></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-block">
                            Generate Document
                        </button>
                    </form>
                    
                    {% if draft_result %}
                    <div class="result-container animated">
                        <div class="result-title">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                                <line x1="16" y1="13" x2="8" y2="13"></line>
                                <line x1="16" y1="17" x2="8" y2="17"></line>
                                <polyline points="10 9 9 9 8 9"></polyline>
                            </svg>
                            Generated Document
                        </div>
                        <div class="result-content">
                            {{ draft_result }}
                        </div>
                    </div>
                    {% endif %}
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    Document Analysis
                </div>
                <div class="card-body">
                    <form action="/analyze" method="post">
                        <div class="form-group">
                            <label for="text">Paste Legal Text</label>
                            <textarea id="text" name="text" placeholder="Paste any legal document or contract text here for analysis"></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-block">
                            Analyze Document
                        </button>
                    </form>
                    
                    {% if analysis_result %}
                    <div class="result-container animated">
                        <div class="result-title">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                            Analysis Results
                        </div>
                        <div class="result-content">
                            {{ analysis_result }}
                        </div>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        <p>LegalEase Assistant &copy; {{ current_year }} | All documents should be reviewed by a qualified attorney</p>
        <p class="watermark">Powered by Python Flask</p>
    </footer>
</body>
</html>
"""

def smart_document_generator(doc_type, description):
    """Enhanced document generator with better formatting"""
    # Extract information with improved patterns
    duration = re.search(r'(\d+)\s*(year|month|day|week)s?', description, re.I)
    parties = re.findall(r'(?:between|for)\s+(.+?)\s+(?:and|with)\s+(.+)', description, re.I)
    protections = re.findall(r'protect(?:ing|s)?\s+(.+?)(?:\s+for|\s+between|$)', description, re.I)
    
    # Format extracted information
    dur_text = f"{duration.group(1)} {duration.group(2)}s" if duration else "the duration specified in this agreement"
    party_a = parties[0][0].strip() if parties else "[Your Name/Company]"
    party_b = parties[0][1].strip() if parties else "[Other Party]"
    protect_text = protections[0] if protections else "confidential information"
    
    # Generate document based on type
    if doc_type == "nda":
        return f"""NON-DISCLOSURE AGREEMENT

This Agreement ("Agreement") is made and entered into as of {datetime.now().strftime('%B %d, %Y')} by and between:

1. {party_a} ("Disclosing Party"); and
2. {party_b} ("Receiving Party").

WHEREAS, the Parties wish to explore a potential business relationship; and
WHEREAS, the Disclosing Party possesses certain {protect_text} that it may disclose to the Receiving Party;

NOW THEREFORE, in consideration of the mutual promises and covenants contained herein, the Parties agree as follows:

1. DEFINITION OF CONFIDENTIAL INFORMATION
1.1 "Confidential Information" means all information disclosed by Disclosing Party to Receiving Party, including but not limited to {protect_text}.

2. OBLIGATIONS
2.1 Receiving Party shall:
   (a) Maintain all Confidential Information in strict confidence;
   (b) Not disclose Confidential Information to any third party;
   (c) Use Confidential Information solely for the purpose of {description.split('for')[-1].split('between')[0].split('protecting')[0] or "evaluating the potential business relationship"}.

3. TERM
3.1 This Agreement shall remain in effect for {dur_text}.

4. GENERAL PROVISIONS
4.1 Governing Law: This Agreement shall be governed by the laws of [State/Country].
4.2 Entire Agreement: This Agreement constitutes the entire understanding between the Parties.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date first written above.

___________________________          ___________________________
{party_a}                             {party_b}
"""

    elif doc_type == "contract":
        return f"""SERVICE CONTRACT AGREEMENT

This Service Contract ("Contract") is made and entered into as of {datetime.now().strftime('%B %d, %Y')} by and between:

1. {party_a} ("Service Provider"); and
2. {party_b} ("Client").

1. SERVICES
1.1 Service Provider agrees to provide the following services: {description.split('for')[0] if 'for' in description else description}

2. COMPENSATION
2.1 Client agrees to pay Service Provider as follows: [Payment terms to be specified]

3. TERM AND TERMINATION
3.1 This Contract shall commence on {datetime.now().strftime('%B %d, %Y')} and continue for {dur_text}.

4. GENERAL PROVISIONS
4.1 Independent Contractor: Service Provider is an independent contractor.
4.2 Governing Law: This Contract shall be governed by the laws of [State/Country].

IN WITNESS WHEREOF, the Parties have executed this Contract as of the date first written above.

___________________________          ___________________________
{party_a}                             {party_b}
"""

    else:  # will
        return f"""LAST WILL AND TESTAMENT

I, {party_a}, residing at [Your Address], being of sound mind and memory, declare this to be my Last Will and Testament.

1. REVOCATION
1.1 I revoke all prior wills and codicils.

2. EXECUTOR
2.1 I appoint [Executor Name] as Executor of this Will.

3. BENEFICIARIES
3.1 I give, devise, and bequeath my estate as follows:
   {description if description else "[Describe how you want your assets distributed]"}

4. RESIDUARY ESTATE
4.1 All the rest, residue, and remainder of my estate I give to [Beneficiary Name].

IN WITNESS WHEREOF, I have signed this Will on {datetime.now().strftime('%B %d, %Y')}.

___________________________
Testator

WITNESSES:

1. ___________________________
   Name: _____________________
   Address: __________________

2. ___________________________
   Name: _____________________
   Address: __________________
"""

def analyze_legal_text(text):
    """Enhanced text analysis with better formatting"""
    # Improved pattern matching with corrected regex
    findings = {
        'Parties': list(set(re.findall(r'(?:party|between|parties)\s*(.*?)(?=\n|\.|;|,)', text, re.I))),
        'Obligations': list(set(re.findall(r'(?:shall\s+not|shall|must|will\s+not|will|agrees\s+to)\s+(.*?)(?=\n|\.|;|,)', text, re.I))),
        'Dates': list(set(re.findall(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b', text, re.I))),
        'Payments': list(set(re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text))),
        'Definitions': list(set(re.findall(r'(?:"([^"]+)"\s+means\s+(.*?)(?=\n|\.|;|,)|term\s+"([^"]+)"\s+shall\s+mean\s+(.*?)(?=\n|\.|;|,))', text, re.I)))
    }
    
    # Format the analysis results
    analysis = "DOCUMENT ANALYSIS REPORT\n\n"
    analysis += f"Analyzed on: {datetime.now().strftime('%B %d, %Y %H:%M')}\n"
    analysis += f"Total words: {len(text.split())}\n"
    analysis += f"Key sections found: {len([v for v in findings.values() if v])}\n\n"
    
    for category, matches in findings.items():
        if matches:
            analysis += f"=== {category.upper()} ===\n"
            for i, match in enumerate(matches, 1):
                if isinstance(match, tuple):  # For definition tuples
                    clean_match = [m for m in match if m][0] + ": " + [m for m in match if m][1]
                else:
                    clean_match = match.strip()
                analysis += f"{i}. {clean_match}\n"
            analysis += "\n"
    
    if len(analysis) < 150:  # If few patterns found
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.split()) > 5]
        analysis += "\n=== KEY SENTENCES ===\n"
        analysis += "\n".join(f"• {s}" for s in sentences[:5])
    
    return analysis

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, current_year=datetime.now().year)

@app.route("/draft", methods=["POST"])
def draft():
    doc_type = request.form["doc_type"]
    details = request.form["details"]
    draft_result = smart_document_generator(doc_type, details)
    return render_template_string(HTML_TEMPLATE, draft_result=draft_result, current_year=datetime.now().year)

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form["text"]
    analysis_result = analyze_legal_text(text)
    return render_template_string(HTML_TEMPLATE, analysis_result=analysis_result, current_year=datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True)