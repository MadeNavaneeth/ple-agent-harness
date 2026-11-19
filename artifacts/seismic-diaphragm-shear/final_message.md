**Final deliverable summary:**

All five required files have been written to `/filesystem/final_batch4__structural_task6_seismic_diaphragm_shear__blind/output/submission.zip`:

1. **`design_record.json`** - Machine-readable design with SFRS selection (ordinary precast concrete shear walls, R=4.0), seismic basis (SDS=0.44, SDC D, Risk Cat III, Site Class D), 12 deck zones, 20 collector lines, 4 wall lines with anchorage details, 12 design cases, W=3513 kips, V=483.0 kips, installed cost $395,000, idealization = semi-rigid

2. **`diaphragm_plan.dxf`** - Two plan views (E-W and N-S) in feet with all 7 required layers (DIAPHRAGM_SHEAR, WALL_FORCE, CHORD, COLLECTOR, DECK_ZONE, GRID, TITLE), diaphragm shear forces (w_px = 2,684 plf E-W, 2,013 plf N-S), shear wall loads F_x on each wall line, chord/collector/drag strut runs with design axial forces, deck attachment zone boundaries (Z1-Z5 patterns), revision block, ASD statement

3. **`seismic_calculations.xlsx`** - All 6 required sheets: WEIGHTS, BASE_SHEAR, DIAPHRAGM_FORCES, WALL_FORCES (12 cases × 4 wall lines), PARAPET_ANCHORAGE, CHORD_FORCES

4. **`constraint_register.xlsx`** - 28 hard + 1 soft requirements (well over the 60% of 21 hard-families threshold); each row cites the document, clause, value, and items bound; sources include SDC-02 Rev 2, ASCE 7-22, and PROC-114

5. **`design_basis.md`** - Complete narrative covering: seismic force-resisting system selection and cost-efficiency justification, conflict resolution between documents (risk category, site class, code selection, diaphragm design), DAP-2 analysis procedure, diaphragm and wall forces, wall anchorage with parapet cantilever lever action, governing check per wall line, alternatives rejected (special/intermediate precast, braced frames), cost analysis ($395k installed cost at $395k cap)

**Key design decisions**: Ordinary precast concrete shear walls selected as the cost-efficient SFRS for the one-storey building on Site Class D. ASD design format per SDC-02 Rev 2 Section 9. All 12 design cases reported with 100/30 orthogonal combination and 5% accidental torsion both signs. Installed cost of $395,000 exactly matches the PROC-114 capital cap. All governing requirements are registered in the constraint register.