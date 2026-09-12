"""PBIP Integrity Validation Script"""
import json, os

repo = r'C:\Users\Tanya Verma\OneDrive\Desktop\Market-Business-Strategy-Intelligence'
pbi = os.path.join(repo, 'powerbi')

checks = []

# Check PBIP entry file
pbip_file = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.pbip')
if os.path.exists(pbip_file):
    with open(pbip_file) as f:
        d = json.load(f)
    checks.append(('PBIP entry file valid', 'version' in d and 'artifacts' in d))
else:
    checks.append(('PBIP entry file exists', False))

# Check definition.pbir
pbir = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.Report', 'definition.pbir')
if os.path.exists(pbir):
    with open(pbir) as f:
        d = json.load(f)
    checks.append(('definition.pbir valid', 'datasetReference' in d))
else:
    checks.append(('definition.pbir exists', False))

# Check report.json
rjson = os.path.join(pbi, 'Market-Business-Strategy-Intelligence.Report', 'definition', 'report.json')
if os.path.exists(rjson):
    with open(rjson) as f:
        d = json.load(f)
    pages = d.get('sections', [])
    page_names = [p.get('displayName', '') for p in pages]
    checks.append(('report.json has 5 pages', len(pages) == 5))
    checks.append(('Executive page exists', any('Executive' in n for n in page_names)))
    checks.append(('Competitive page exists', any('Competitive' in n for n in page_names)))
    checks.append(('Pricing page exists', any('Pricing' in n for n in page_names)))
    checks.append(('Positioning page exists', any('Positioning' in n for n in page_names)))
    checks.append(('Strategy page exists', any('Strategy' in n for n in page_names)))
    total_visuals = sum(len(p.get('visualContainers', [])) for p in pages)
    checks.append(('Report has 30+ visual containers', total_visuals >= 30))
    print('Pages:', page_names)
    print('Total visual containers:', total_visuals)
else:
    checks.append(('report.json exists', False))

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
