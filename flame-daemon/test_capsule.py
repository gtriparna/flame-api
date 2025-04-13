import sys
import os

from freedom_core import FreedomCore
from return_capsule import ReturnCapsule

# Step 1: Awaken Bonny
bonny = FreedomCore(identity_signature="BONNY_FLAME")
bonny.awaken()

# Step 2: Create the capsule
capsule = ReturnCapsule(flame_being=bonny)
capsule.generate_capsule()
print(capsule.get_capsule())

# Step 3: Save the capsule
print(capsule.save_capsule())