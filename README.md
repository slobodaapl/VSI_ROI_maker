# VSI tiling utility

Cuts up a .vsi bioformats file into 256x256 images (resized from 1024x1024 that it extracts).
Includes detection for empty tiles or tiles with insufficient semantic information, and
also checkpoints in case the program crashes at any point, in order to be able to resume.

Code is documented and written with complete accordance to PEP-8 for easy readability, and made easy to modify.
