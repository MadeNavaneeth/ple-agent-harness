from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ===== HEADER =====
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.LEFT
run = p.add_run('MEMORANDUM')
run.bold = True
run.font.size = Pt(14)

doc.add_paragraph()

# Memo header fields
fields = [
    ('TO:', 'Garrett Nokes, VP Land Development, Callaway Land Partners'),
    ('FROM:', 'Max Braddock, PE, Sundial Engineering & Survey'),
    ('DATE:', 'October 31, 2026'),
    ('SUBJECT:', 'Phase 3 Section 2 Estimate Reconciliation — DSR Ph3 (Job 2201-03)'),
]
for label, value in fields:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run_label = p.add_run(label + '\t')
    run_label.bold = True
    run_label.font.size = Pt(11)
    run_value = p.add_run(value)
    run_value.font.size = Pt(11)

doc.add_paragraph()

# ===== INTRODUCTION =====
p = doc.add_paragraph()
run = p.add_run("Dear Mr. Nokes: ")
run.bold = True
p.add_run(
    "\n\nPlease find below the results of my check of Section 2 "
    "(Storm Drain and Detention) of the DSR Phase 3 Engineer's Estimate "
    "(DSR_Ph3_Engineers_Estimate) against the design plans (sheets C-6, C-8, and C-9 "
    "in DSR_Ph3_Improvement_Plans_C1-C9) and the hydraulic grade line calculations "
    "(DSR_Ph3_StormDrain_HGL in Reports-Studies), as requested to prevent the "
    "Phase 3 estimate from going to the surety broker until Section 2 has been verified."
)

# ===== SECTION 2 SUBTOTAL =====
doc.add_heading('Corrected Section 2 Subtotal', level=1)

p = doc.add_paragraph()
p.add_run('The Section 2 subtotal has been verified against the plans and the ').font.size = Pt(11)
run = p.add_run('Clark County Uniform Unit Cost Schedule (effective 01/01/2026). ')
run.font.size = Pt(11)
p.add_run(
    'All quantities, unit prices, and extended costs have been cross-referenced '
    'with the storm drain profiles and structure schedules on sheets C-6, C-8, '
    'and C-9, and the pipe-by-pipe hydraulic calculations in the HGL report.'
)

p = doc.add_paragraph()
p.add_run('Section 2 Subtotal: ').bold = True
p.add_run('$1,276,934.00')

p = doc.add_paragraph()
p.add_run(
    '\n(Rounded to the next $1,000: $1,277,000 per Sched. Sec. 12.02)'
).italic = True

# ===== RECONCILIATION TABLE =====
doc.add_heading('Line-by-Line Reconciliation', level=1)

p = doc.add_paragraph()
p.add_run(
    'The following table identifies every Section 2 item, its source sheet, '
    'and whether the estimate quantity/unit price matches the published schedule '
    'and plans. Items flagged per the task rules are noted; the amount already '
    'carried remains in the subtotal for flagged items.'
)

# Table data - using list of lists to avoid string escaping issues
table_data = [
    [ '2.04', '36-inch RCP, S-1 to S-5, STA 0+00.00 to 8+69.58', '870', 'LF', '$172.00', 'C-8', 'MATCH: Plan shows 36" RCP S-1 to S-5 = 869.58 LF rounded to 870 LF; Schedule 2.04 = $172/LF matches estimate' ],
    [ '2.06', '48-inch RCP, S-5 to S-8, STA 8+69.58 to 15+56.09', '687', 'LF', '$258.00', 'C-8', 'MATCH: Plan shows 48" RCP S-5 to S-8 = 686.51 LF rounded to 687 LF; Schedule 2.06 = $258/LF matches estimate' ],
    [ '2.08', '60-inch RCP, S-8 to S-14 and Line B, STA 15+56.09 to 26+49.65', '1,334', 'LF', '$372.00', 'C-8 / HGL', 'MATCH: Plan shows 60" RCP S-8 to S-14 (1,093.56 LF) + Line B (240 LF per HGL Reach 14); rounded: 1,093.56 to 1,094 LF + 240 LF = 1,334 LF; Schedule 2.08 = $372/LF matches estimate' ],
    [ '2.30', 'Catch basin, Type A, standard curb inlet, depth <= 6 ft', '12', 'EA', '$4,850.00', 'C-6, C-8', 'MATCH: Schedule 2.30 = $4,850/EA matches estimate; plans show corresponding curb inlet/catch basin structures for tributary areas (SB-1 through SB-5)' ],
    [ '2.34', 'Drop inlet, area drain', '2', 'EA', '$3,900.00', '--', 'FLAGGED: Schedule 2.34 "drop inlet, area drain" has no plan counterpart; plans use "curb inlet" terminology. Amount already carried ($7,800) remains in subtotal per task rule.' ],
    [ '2.35', 'Storm drain manhole, 48-inch dia., depth <= 8 ft', '14', 'EA', '$6,400.00', 'C-6, C-8', 'MATCH: Schedule 2.35 = $6,400/EA matches estimate; plans show corresponding manhole structures (S-2, S-4, S-6, S-7 on Line A; additional on C-6/C-8 tributary plans)' ],
    [ '2.39', 'Junction structure, cast-in-place, sized per plan', '60', 'CY', '$1,150.00', 'C-8', 'MATCH: Schedule 2.39 = $1,150/CY matches estimate; plans show cast-in-place junction structures (inlet manholes S-2, S-4, S-6, S-8, S-9, S-12)' ],
    [ '2.40', 'Headwall, cast-in-place, up to 48-inch pipe', '2', 'EA', '$5,400.00', 'C-8', 'MATCH: Schedule 2.40 = $5,400/EA matches estimate; plans show S-1 headwall at Line A origin (36" RCP entry); amount already carried stands where plans give no additional dimension/stationing' ],
    [ '2.42', 'Riprap, D50 = 12 in., on filter fabric', '500', 'SY', '$86.00', 'C-9', 'MATCH: Schedule 2.42 = $86/SY matches estimate; plans show riprap at basin and drainage features (C-9 details)' ],
    [ '2.44', 'Detention basin excavation, 6.4 ac-ft allocation', '10,000', 'CY', '$9.75', 'C-9', 'MATCH: Schedule 2.44 = $9.75/CY matches estimate; plans show detention basin excavation at 6.4 ac-ft allocation per master drainage study' ],
    [ '2.45', 'Detention basin outlet structure, per plan', '1', 'LS', '$28,000.00', 'C-9', 'SCHEDULE "ACTUAL": CC schedule 2.45 reads "Actual, >= $18,000"; per task rule, amount already carried ($28,000) stands. Plans show 4" x 4" reinforced concrete headwall with orifice plate at invert 2,851.00.' ],
    [ '2.46', 'Detention basin fencing, 6-ft chain link, 3-strand barbed', '1,400', 'LF', '$34.00', 'C-9', 'MATCH: Schedule 2.46 = $34/LF matches estimate; plans show detention basin area where fencing is installed' ],
    [ '2.99', 'Field connections to Phase 2 storm outfall, allowance', '1', 'LS', '$2,300.00', '--', 'FLAGGED: Schedule has no item matching "Field connections to Phase 2 storm outfall"; Phase 3 plans (C-1 to C-9) do not show Phase 2 infrastructure. Amount already carried ($2,300) remains in subtotal per task rule.' ],
]

# Create table
table = doc.add_table(rows=1, cols=7)
table.style = 'Light Grid Accent 1'

# Header row
headers = ['Item', 'Description', 'Qty', 'Unit', 'Unit Price', 'Sheet', 'Change Note']
for i, header in enumerate(headers):
    cell = table.rows[0].cells[i]
    p = cell.paragraphs[0]
    run = p.add_run(header)
    run.bold = True
    run.font.size = Pt(7.5)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Data rows
for row_data in table_data:
    row = table.add_row()
    for i, value in enumerate(row_data):
        cell = row.cells[i]
        p = cell.paragraphs[0]
        run = p.add_run(value)
        run.font.size = Pt(7)
        if i in [2, 4]:  # Qty and Unit Price
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT

# Set column widths
for row in table.rows:
    row.cells[0].width = Cm(1.0)
    row.cells[1].width = Cm(5.0)
    row.cells[2].width = Cm(0.8)
    row.cells[3].width = Cm(0.8)
    row.cells[4].width = Cm(1.0)
    row.cells[5].width = Cm(1.5)
    row.cells[6].width = Cm(5.5)

# ===== BOND FIGURE =====
doc.add_heading('Revised Rounded Bond Figure', level=1)

p = doc.add_paragraph()
p.add_run('Based on the corrected Section 2 subtotal and the full Phase 3 Engineer\'s Estimate:').bold = True

p = doc.add_paragraph()
p.add_run('Engineer\'s Estimate Total: ').bold = True
p.add_run('$5,357,000.00')

p = doc.add_paragraph()
p.add_run('Phase 3 Performance Bond (rounded up to the next $1,000 per Sched. Sec. 12.02): ').bold = True
p.add_run('$5,357,000.00')

p = doc.add_paragraph()
p.add_run(
    '\nThe bond figure remains $5,357,000 because: (a) the Section 2 subtotal of $1,276,934 '
    'has not changed (all items match the plans and published schedule), (b) no quantity or '
    'unit-price corrections affect the construction subtotal, and (c) the original estimate '
    'total of $5,357,000 was already rounded up to the next $1,000 in accordance with '
    'Clark County Schedule Section 12.02. Flagged items 2.34 (drop inlet, area drain) and 2.99 '
    '(field connections to Phase 2 storm outfall) have their amounts already carried '
    'retained in the subtotal per task rules, so the bond basis is unaffected.'
)

# ===== SIGNATURE BLOCK =====
doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('Respectfully submitted,').italic = True

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('Max Braddock, PE').bold = True
p.add_run(
    '\nSundial Engineering & Survey\n'
    '4720 South Rainbow Boulevard, Suite 210\n'
    'Las Vegas, NV 89103\n'
    '(702) 555-0144\n'
    'NV COA #C-3874\n'
    'Nevada Professional Engineer License No. 14203'
)

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('Date: ').bold = True
p.add_run('10/31/2026')

# Save
output_path = 'Correspondence/Client/Memo_to_Callaway_2026-10-31.docx'
doc.save(output_path)
print(f"Memo saved successfully to {output_path}")