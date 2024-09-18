<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Auth;
use Illuminate\Http\Request;
use App\Models\FarmZone;
use Inertia\Inertia;

class FarmZoneController extends Controller
{
    public function index()
    {
        $farms = FarmZone::where('user_id', auth()->id())->get();
        return response()->json($farms);
    }
    public function store(Request $request)
    {
        $user = Auth::user();

        $validatedData = $request->validate([
            'coordinates' => 'required|array',
            'farm_name' => 'required|string|max:255', // Validate farm_name
            'farm_area' => 'required|numeric',
        ]);

        $farmZone = FarmZone::create([
            'user_id' => $user->id, // Associate the zone with the authenticated user
            'coordinates' => $validatedData['coordinates'],
            'farm_name' => $validatedData['farm_name'], // Save farm_name
            'farm_area' => $validatedData['farm_area'],
        ]);

        return response()->json(['success' => true, 'farmZone' => $farmZone]);
    }

    public function destroy($id)
    {
        // Find the farm zone by ID
        $farm = FarmZone::findOrFail($id);

        // Delete the farm zone
        $farm->delete();

        // Return a success response
        return response()->json(['message' => 'Farm zone deleted successfully!']);
    }

    public function update(Request $request, $id)
    {
        // Find the farm zone by ID
        $farmZone = FarmZone::find($id);
        // Check if the farm zone exists
        if ($farmZone) {
            // Update the farm name
            $farmZone->farm_name = $request->input('farm_name');
            $farmZone->save();  // Save changes
            return response()->json(['message' => 'Farm zone updated successfully!'], 200);
        }
        // If the farm zone was not found
        return response()->json(['message' => 'Farm zone not found.'], 404);
    }
    public function viewFarm($id)
    {
        $farm = FarmZone::findOrFail($id);
        return Inertia::render('FarmView', ['farm' => $farm]);
    }

    public function compareFarm($id)
    {
        $farm = FarmZone::findOrFail($id);
        return Inertia::render('FarmCompare', ['farm' => $farm]);
    }

    public function show($id)
    {
        // Fetch the farm zone by ID
        $farmZone = FarmZone::find($id);
        if (!$farmZone) {
            return response()->json(['message' => 'Farm zone not found'], 404);
        }
        return response()->json($farmZone);
    }

    public function getFarmZoneCoordinates($id)
    {
        $farmZone = FarmZone::findOrFail($id);
        $coordinates = $farmZone->coordinates;

        return response()->json([
            'coordinates' => json_decode($coordinates)
        ]);
    }

    public function calculateNDVI($id)
    {
        // Retrieve farm zone from the database
        $farmZone = FarmZone::find($id);
        if (!$farmZone) {
            return response()->json(['error' => 'Farm zone not found'], 404);
        }

        // Convert farm zone coordinates to GeoJSON format
        $coordinates = json_encode($farmZone->coordinates);

        // Execute Python script to calculate NDVI using GEE
        $pythonScript = base_path('/resources/scripts/ndvi_processor.py');
        $command = "python $pythonScript $coordinates";
        $output = shell_exec($command);
        $result = json_decode($output, true);

        // Check for error in Python script execution
        if (!isset($result['tile_url'])) {
            return response()->json(['error' => 'NDVI calculation failed'], 500);
        }

        // Return the NDVI tile URL to the frontend
        return response()->json(['tileUrl' => $result['tile_url']]);
    }

    public function calculateEVI($id)
    {
        // Retrieve farm zone from the database
        $farmZone = FarmZone::find($id);
        if (!$farmZone) {
            return response()->json(['error' => 'Farm zone not found'], 404);
        }

        // Convert farm zone coordinates to GeoJSON format
        $coordinates = json_encode($farmZone->coordinates);

        // Execute Python script to calculate NDVI using GEE
        $pythonScript = base_path('/resources/scripts/evi_processor.py');
        $command = "python $pythonScript $coordinates";
        $output = shell_exec($command);
        $result = json_decode($output, true);

        // Check for error in Python script execution
        if (!isset($result['tile_url'])) {
            return response()->json(['error' => 'EVI calculation failed'], 500);
        }

        // Return the NDVI tile URL to the frontend
        return response()->json(['tileUrl' => $result['tile_url']]);
    }

    public function calculateNDWI($id)
    {
        // Retrieve farm zone from the database
        $farmZone = FarmZone::find($id);
        if (!$farmZone) {
            return response()->json(['error' => 'Farm zone not found'], 404);
        }

        // Convert farm zone coordinates to GeoJSON format
        $coordinates = json_encode($farmZone->coordinates);

        // Execute Python script to calculate NDVI using GEE
        $pythonScript = base_path('/resources/scripts/ndwi_processor.py');
        $command = "python $pythonScript $coordinates";
        $output = shell_exec($command);
        $result = json_decode($output, true);

        // Check for error in Python script execution
        if (!isset($result['tile_url'])) {
            return response()->json(['error' => 'NDWI calculation failed'], 500);
        }

        // Return the NDVI tile URL to the frontend
        return response()->json(['tileUrl' => $result['tile_url']]);
    }

}
