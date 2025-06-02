# Anode-Filter Combinations and Spectral Files for Mammography Simulation

## Introduction

In digital mammography, the selection of the anode-filter combination and tube voltage (kV) is optimized based on compressed breast thickness to ensure the best compromise between image quality and patient dose. This document summarizes the most commonly used configurations and provides guidance on how spectral input files are constructed for Monte Carlo simulations.

## Typical Anode-Filter Combinations and kV Settings

| kV Range     | Anode Material | Filter (Thickness)     | Recommended Breast Thickness | Characteristics                                                                 |
|--------------|----------------|-------------------------|-------------------------------|----------------------------------------------------------------------------------|
| 24 – 28 kV   | Mo             | Mo (0.030 mm)          | < 3 cm                        | Soft X-ray spectrum; high contrast for thin, low-density breasts; higher dose   |
| 26 – 30 kV   | Mo             | Rh (0.025 – 0.030 mm)  | 3 – 5 cm                      | Harder spectrum than Mo-Mo; improved penetration with moderate dose             |
| 28 – 32 kV   | Rh             | Rh (0.050 mm)          | > 5 cm                        | Suitable for dense or thick breasts; lower dose with good contrast              |
| 28 – 32 kV   | W              | Rh (0.050 mm)          | > 5 cm                        | Broad, hard spectrum; good image quality and dose efficiency                    |
| 30 – 35 kV   | W              | Ag (0.050 – 0.100 mm)  | > 6 cm                        | Very hard spectrum; excellent for very dense or thick breasts; low skin dose    |

## Construction of Spectrum Input Files for Simulation

Photon spectra for Monte Carlo simulations (e.g., with MCNP or MC-GPU) are typically provided as text input files with the following structure:

1. **File extension**: `.in`
2. **File naming convention**: `<kV><Anode>-<Filter><FilterThickness>.in`  
   - Example: `28Mo-Rh0.025.in` represents a 28 kV spectrum from a Mo anode with 0.025 mm Rh filter.
3. **File content**:
   - Two columns:  
     - First column: photon energy in **MeV**  
     - Second column: **normalized fluence** (photons/MeV)

These spectra can be obtained from measured data, software like SpekCalc, or published datasets, and must be normalized before being used as source input for simulation codes.


