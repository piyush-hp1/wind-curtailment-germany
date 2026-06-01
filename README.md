# Wind Curtailment Optimisation — Germany 🌬️

> ⚠️ Work in Progress — actively being developed

## The Problem
Germany curtails billions of kWh of wind energy every year 
due to grid bottlenecks in the north. This is both an 
economic loss and a missed opportunity for the clean 
energy transition.

## What This Project Does
Using real wind data from NASA POWER and curtailment data 
from SMARD.de, this project models and compares three 
strategies for utilising excess wind energy at Windpark 
Holtriem, Lower Saxony:

- 🔋 Battery Storage
- 💧 Hydrogen Production  
- ⚖️ Gravity Storage

Each strategy is evaluated on:
- Recoverable energy (MWh)
- Revenue potential (€)
- ROI (%)
- Payback period (years)

## Tools Used
- Python (Pandas, SQLite, Matplotlib)
- NASA POWER API
- SMARD.de data

## Status
- [x] Wind resource analysis
- [x] Turbine performance modelling
- [ ] Real curtailment data integration
- [ ] Storage economics comparison
- [ ] Final optimisation model
