<?php

use App\Http\Controllers\Controller;
use App\Models\Image;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class ImageProcessingController extends Controller
{
    public function uploadImage(Request $request)
    {
        $request->validate([
            'image' => 'required|file|mimes:tif,tiff', // Validate for multispectral images
        ]);

        $file = $request->file('image');
        $path = $file->store('images');

        $image = Image::create([
            'original_filename' => $file->getClientOriginalName(),
            'path' => $path,
            'user_id' => auth()->id(), // Assuming the user is authenticated
        ]);

        return response()->json(['message' => 'Image uploaded successfully', 'image' => $image]);
    }

    public function processImage(Image $image)
    {
        $inputPath = storage_path('app/' . $image->path);
        $outputPath = storage_path('app/images/corrected_' . basename($inputPath));

        $command = "gdal_translate -of GTiff $inputPath $outputPath";
        exec($command, $output, $returnVar);

        if ($returnVar !== 0) {
            return response()->json(['message' => 'Error processing image'], 500);
        }

        $image->update([
            'path' => 'images/corrected_' . basename($inputPath),
            'is_processed' => true,
            'correction_status' => 'radiometric, atmospheric', // Example status update
        ]);

        return response()->json(['message' => 'Image processed successfully']);
    }

    public function calculateIndices(Image $image)
    {
        $inputPath = storage_path('app/' . $image->path);
        $outputPath = storage_path('app/images/ndvi_' . basename($inputPath));

        // Example NDVI calculation command using GDAL
        $command = "gdal_calc.py -A $inputPath --outfile=$outputPath --calc=\"(A-B)/(A+B)\""; // Placeholder command
        exec($command, $output, $returnVar);

        if ($returnVar !== 0) {
            return response()->json(['message' => 'Error calculating indices'], 500);
        }

        $image->update([
            'indices' => json_encode(['NDVI' => 'path_to_ndvi_image']), // Example indices update
        ]);

        return response()->json(['message' => 'Indices calculated successfully']);
    }


}
