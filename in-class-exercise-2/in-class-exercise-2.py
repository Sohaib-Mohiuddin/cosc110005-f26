# MAIN INFORMATION
# Course: COSC 1100
# Assignment: Class Exercise 2 - Numeric and String Data
# Author: Instructor example solution
# Date: September 24, 2026
# Purpose: Estimate how many AI Hub rubber ducks would be needed to cover
#          one reservoir at Durham College's Oshawa Campus.
#
# PLAN
# 1. OUTPUT
#    Display the reservoir area, the assumed duck dimensions, the area each
#    duck occupies, and the estimated number of whole ducks required.
#
# 2. INPUT
#    Reservoir area: 5,000 square meters (the supplied estimate).
#    Duck length: 10 centimeters (assumed for this example).
#    Duck width: 8 centimeters (assumed for this example).
#    Store these values in constants; no keyboard input is needed.
#
# 3. PROCESS AND ASSUMPTIONS
#    Model each duck's footprint as a rectangle: area = length * width.
#    These dimensions describe the space occupied on the water, not height.
#    Convert centimeters to meters before calculating the duck's area.
#    Divide the reservoir area by the area occupied by one duck.
#    Round UP because a fraction of a duck requires another whole duck.
#    Assume positive dimensions and tightly arranged rectangular footprints.
#    Ignore gaps between actual ducks, shoreline shape, wind, and overlap.
#    This is an area-based estimate, not a guarantee of complete coverage.
#
# 4. PSEUDOCODE
#    START
#        SET reservoir_area_m2 TO 5000
#        SET duck_length_cm TO 10
#        SET duck_width_cm TO 8
#        SET centimeters_per_meter TO 100
#        CALCULATE duck_length_m = duck_length_cm / centimeters_per_meter
#        CALCULATE duck_width_m = duck_width_cm / centimeters_per_meter
#        CALCULATE duck_area_m2 = duck_length_m * duck_width_m
#        CALCULATE estimated_ducks = reservoir_area_m2 / duck_area_m2
#        SET ducks_required TO estimated_ducks rounded up to a whole number
#        DISPLAY a title, the area, duck dimensions, and duck footprint
#        DISPLAY ducks_required with a thousands separator
#    END
#
# 5. DESK CHECK
#    Duck length: 10 / 100 = 0.10 m
#    Duck width: 8 / 100 = 0.08 m
#    Duck footprint: 0.10 * 0.08 = 0.008 square meters
#    Number of ducks: 5000 / 0.008 = 625000
#    Expected result: 625,000 ducks
#    Rounding check: with a 1-square-meter reservoir and a 30 cm by 20 cm
#    footprint, 1 / (0.30 * 0.20) = 16.666...; round up to 17 ducks.

import math

# Change these assumptions to explore a different reservoir or duck size.
RESERVOIR_AREA_M2 = 5000
DUCK_LENGTH_CM = 10
DUCK_WIDTH_CM = 8
CENTIMETERS_PER_METER = 100

# Keep the units consistent so both areas are measured in square meters.
duck_length_m = DUCK_LENGTH_CM / CENTIMETERS_PER_METER
duck_width_m = DUCK_WIDTH_CM / CENTIMETERS_PER_METER
duck_area_m2 = duck_length_m * duck_width_m

estimated_ducks = RESERVOIR_AREA_M2 / duck_area_m2
ducks_required = math.ceil(estimated_ducks)  # We need whole ducks.

# F-strings make the results readable and include the units.
print("Durham College Reservoir Duck Estimate")
print(f"Reservoir area: {RESERVOIR_AREA_M2:,.0f} square meters")
print(f"Assumed duck footprint: {DUCK_LENGTH_CM} cm long by {DUCK_WIDTH_CM} cm wide")
print(f"Area per duck: {duck_area_m2:.3f} square meters")
print(f"Estimated ducks required: {ducks_required:,}")
print("Estimate assumes tightly arranged rectangular footprints with no gaps.")
