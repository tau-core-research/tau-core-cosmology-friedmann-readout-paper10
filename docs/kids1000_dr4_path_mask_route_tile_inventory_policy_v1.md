# KiDS DR4 Path-Mask Route Tile Inventory Policy v1

This gate parses the preferred KiDS DR4.1 9-band mask route script into a
source-frozen tile-coordinate inventory.

It records only the URL order and filename-derived tile coordinates for the 196
mask products listed by the preferred route. It does not download those mask
products, does not parse their pixels, and does not infer a footprint polygon or
path weight. The inventory is useful only as a source-side route geometry index
for later path-mapping work.

This gate does not use KiDS data-vector values, posterior chains, residuals, fit
statistics, or post-hoc sky/path labels. Endpoint scoring remains disabled.
