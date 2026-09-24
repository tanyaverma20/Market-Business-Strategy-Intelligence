"""PBIP Integrity Validation Script"""
import json, os

# Determine repo root relative to this script
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pbi = os.path.join(repo, 'powerbi')

checks = []

# Check PBIP entry file
pbip_file = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.pbip')
if os.path.exists(pbip_file):
    with open(pbip_file, encoding='utf-8') as f:
        d = json.load(f)
    checks.append(('PBIP entry file valid', 'version' in d and 'artifacts' in d))
else:
    checks.append(('PBIP entry file exists', False))

# Check definition.pbir
pbir = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.Report', 'definition.pbir')
if os.path.exists(pbir):
    with open(pbir, encoding='utf-8') as f:
        d = json.load(f)
    checks.append(('definition.pbir valid', 'datasetReference' in d))
else:
    checks.append(('definition.pbir exists', False))

# Check PBIR pages (modern format) or report.json sections (legacy format)
pages_json_path = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.Report', 'definition', 'pages', 'pages.json')
pages_dir = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.Report', 'definition', 'pages')
rjson = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.Report', 'definition', 'report.json')

page_names = []
total_visuals = 0

if os.path.exists(pages_json_path) and os.path.isdir(pages_dir):
    with open(pages_json_path, encoding='utf-8') as f:
        pj = json.load(f)
    page_order = pj.get('pageOrder', [])
    for p_id in page_order:
        p_dir = os.path.join(pages_dir, p_id)
        p_json_file = os.path.join(p_dir, 'page.json')
        if os.path.exists(p_json_file):
            with open(p_json_file, encoding='utf-8') as pf:
                pd = json.load(pf)
            page_names.append(pd.get('displayName', p_id))
        else:
            page_names.append(p_id)
        v_dir = os.path.join(p_dir, 'visuals')
        if os.path.isdir(v_dir):
            total_visuals += len([v for v in os.listdir(v_dir) if os.path.isdir(os.path.join(v_dir, v))])
    checks.append(('report definition has 5 pages', len(page_order) == 5))
elif os.path.exists(rjson):
    with open(rjson, encoding='utf-8') as f:
        d = json.load(f)
    pages = d.get('sections', [])
    page_names = [p.get('displayName', '') for p in pages]
    total_visuals = sum(len(p.get('visualContainers', [])) for p in pages)
    checks.append(('report definition has 5 pages', len(pages) == 5))
else:
    checks.append(('report definition exists', False))

checks.append(('Executive page exists', any('Executive' in n for n in page_names)))
checks.append(('Competitive page exists', any('Competitive' in n for n in page_names)))
checks.append(('Pricing page exists', any('Pricing' in n for n in page_names)))
checks.append(('Positioning page exists', any('Positioning' in n for n in page_names)))
checks.append(('Strategy page exists', any('Strategy' in n for n in page_names)))
checks.append(('Report has 30+ visual containers', total_visuals >= 30))
print('Pages:', page_names)
print('Total visual containers:', total_visuals)

# Check model.bim
mbim = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.SemanticModel', 'definition', 'model.bim')
if os.path.exists(mbim):
    with open(mbim) as f:
        d = json.load(f)
    tables = d['model']['tables']
    table_names = [t['name'] for t in tables]
    measures_table = next((t for t in tables if t['name'] == '_Measures'), None)
    num_measures = len(measures_table.get('measures', [])) if measures_table else 0
    checks.append(('model.bim has 5+ tables', len(tables) >= 5))
    checks.append(('_Measures table exists', measures_table is not None))
    checks.append(('Has 30+ DAX measures', num_measures >= 30))
    bim_text = open(mbim, encoding='utf-8').read()
    checks.append(('No DATA_PATH placeholder', 'DATA_PATH' not in bim_text))
    pending_blank = sum(1 for m in measures_table.get('measures', [])
                        if 'BLANK()' in m.get('expression', ''))
    checks.append(('Pending measures return BLANK()', pending_blank >= 5))
    print('Tables:', table_names)
    print('DAX measures:', num_measures, '(verified + pending)')
    print('Pending BLANK() measures:', pending_blank)
else:
    checks.append(('model.bim exists', False))

print()
for name, result in checks:
    status = 'PASS' if result else 'FAIL'
    print('  [' + status + '] ' + name)

all_pass = all(r for _, r in checks)
print()
result_str = 'ALL PASS' if all_pass else 'FAILURES DETECTED'
print('PBIP INTEGRITY:', result_str)
