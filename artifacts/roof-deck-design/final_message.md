The submission is complete. Here's a summary of the four deliverables in `output/submission.zip`:

1. **`deck_design.xlsx`** — 6 sheets with exact specified column headers: Zones (5 rectangles covering the full roof), DesignBasis (17 keys), Drifts (4 surcharges), CalcSummary (5 zones with S07 governing), Diaphragm (6 lateral scenarios), BOM (deck areas by gage, fasteners, sidelap connectors)

2. **`roof_deck_plan.dxf`** — DXF with 5 closed LWPOLYLINES on S-DECK-ZONE (zone rectangles), Z-1..Z-5 TEXT labels on S-DECK-TEXT inside respective zones, framing on S-FRAMING, openings on S-OPENING

3. **`constraint_register.xlsx`** — 38 rows documenting requirements from EOR-DC-RD-01, LAT-2026-003, SNOW-2026-014, joist schedule, and roof plan, with clause, value, and applies_to columns

4. **`design_basis.md`** — Comprehensive narrative covering governing document precedence, snow/seismic calculations, drift surcharge computations for all 4 obstructions, zoning decisions driving gage transitions, diaphragm analysis and semi-rigid classification, and attachment/uplift design

Key design: two deck gages (22 south of screens, 20 north), 5 zones on 6 ft modules, semi-rigid diaphragm classification, S07 (seismic along x) governing all zones for both gravity and lateral demands, 36/3 support pattern uniformly, 3 sidelap connectors per span.