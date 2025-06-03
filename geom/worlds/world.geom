################
# WORLD SETUP  #
################


# -------------------------
# 1. INCLUDED MATERIALS
# -------------------------

# Definition of materials used in the simulation
:include geom/MyMaterials.txt

# ------------------------------
# 2. GEOMETRIC PARAMETERS
# ------------------------------

# Source-to-Object Distance
:P SOD 750.0

# Source-to-Detector Distance
:P SDD 750.0

# World size (depends on SDD)
:P WorldDimen $SDD*2+50.0


# ---------------------------
# 3. WORLD DEFINITION
# ---------------------------

# World volume: centered air-filled box
:VOLU world BOX 0.5*$WorldDimen 0.5*$WorldDimen 0.5*$WorldDimen G4_AIR

# Hide world volume in the viewer
:VIS world OFF


# -------------------------------
# 4. ELEMENTS INCLUDED IN WORLD
# -------------------------------

# You can enable or disable elements by commenting lines
# - Jaws (collimators)
# - Ionization Chamber
# - Phantom (test object)
# - Detector

# Jaws (collimators)
#:include geom/elementsInWorld/jaws.geom

# Ionization Chamber
:include geom/elementsInWorld/Ion_Chamber.geom

# Physical Detector
#:include geom/elementsInWorld/detector.geom
