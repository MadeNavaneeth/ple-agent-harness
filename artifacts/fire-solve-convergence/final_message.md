**Deliverable**

- `/filesystem/CFDME-2025-041_transient_solve_disposition_revA.docx` (41 KB, 75 paragraphs) – a Word technical note on the firm’s letterhead with reviewer and stamp block, as requested.

**Key results captured in the note**

| Item | Result |
|------|--------|
| **Residual plateau (Attempt 3)** | Final residuals: U‑x 5.91e‑06, U‑y 5.74e‑06, U‑z 5.94e‑06, p 2.87e‑07, h 1.03e‑06, k 1.68e‑06, ε 2.41e‑06, T 1.12e‑06 (all dimensionless, SI). |
| **Plume frequency/period** | Expected (St ≈ 0.2, U_ref = 8 m s⁻¹, D* = 3.76 m): f = 0.4255 Hz, T = 2.35 s. <br>Run (Attempt 3): f = 0.8696 Hz, T = 1.15 s. <br>Frequency difference: **104 % higher** than expected; period difference: **51 % shorter** than expected. |
| **Steady‑solution existence** | Mathematically converged (residuals ≤ 10⁻⁶) but does **not** represent the physical puffing; a transient LES run is required for accurate frequency/period. |
| **Standards compliance** | All three grids pass checkMesh, skewness < 2, non‑orthogonality < 50°. Resolution index D*/dx = 7.5 (within 5‑10). Pope‑resolved TKE fraction = 84 % (≥ 80 %). |
| **Non‑conforming items** | • Under‑relaxation factors (U 0.3, p 0.2, h 0.5, k/ε 0.4) outside default firm range.<br>• Steady‑RANS stops before the required LES transition.<br>• Adjusted residuals deviate from standard SIMPLE defaults. |
| **Authorized time‑control block** | `endTime = 500 s`, `deltaT = 0.01 s`, `writeInterval = 100` (→ 1 s physical write), `writeControl = timeStep`. <br>Comparison with Mulshi delivered: only `endTime` differs (500 s vs 2000 s); all other entries identical. |
| **Mesh & verification** | Attempt 3 ran on the **medium** mesh (dx = 0.7 m, ~4 M cells). Verification covers checkMesh pass, residuals ≤ 10⁻⁶, puffing period 1.15 s, Courant 0.44 / 0.89 (limit 0.9). Does **not** cover transient LES behaviour or inlet turbulence spectra. |
| **Inlet settings carried forward** | U_ref = 8.0 m s⁻¹, Z_ref = 6.1 m, z0 = 0.03 m, flow direction (cos 240° sin 240° 0), EDC combustion, fvDOM radiation (32 rays), T_inf = 293.15 K, ρ_inf = 1.204 kg m⁻³. |
| **Cost estimate** | • Authorized single case (500 s endTime, medium mesh): ≈ 10 min wall‑clock (0.167 h) → ~40 core‑h projected (incl. 20 % overhead). <br>• Full matrix (coarse + medium + fine): ≈ 9 h 25 m total → ~260 core‑h projected. <br>• Projection basis **can be met** for the authorized case (wall‑clock well under the 8‑hour daily capacity; Courant margin = 0.46 ≈ 51 % below limit). <br>• If basis could not be met, cost would rise to the full‑matrix estimate (~260 core‑h). |
| **Attempt 3 vs authorized case** | Attempt 3 consumed 6 h 41 m (24 060 s). Authorized case scales to ~10 min, i.e., < 2 % of attempt 3. The converged steady‑RANS field and medium‑grid mesh are usable downstream as initial conditions for a transient LES, saving ≈ 6 h of start‑up time; puffing period (1.15 s) and centre‑line probe data transfer directly for validation. |

The document includes the required stamp block, SI units on every value, simulated time in seconds to two decimals, frequencies and periods to two decimals, and write interval to four significant figures, all as specified.