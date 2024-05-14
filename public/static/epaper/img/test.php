<?php
// Get the coordinates from POST data
$x = 388;
$y = 101;
$w = 143;
$h = 143;

// Load the original image
$src = imagecreatefromgif('main.gif');

// Create a new image with the specified dimensions
$dest = imagecreatetruecolor($w, $h);

// Crop the original image to the new dimensions
imagecopy($dest, $src, 0, 0, $x, $y, $w, $h);

// Save the cropped image to a file
imagegif($dest, 'cropped_image.gif');

// Free up memory
imagedestroy($src);
imagedestroy($dest);

echo "Image cropped and saved successfully!";
?>