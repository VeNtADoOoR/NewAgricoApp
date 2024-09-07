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
            'farm_name' => 'required|string|max:255' // Validate farm_name
        ]);

        $farmZone = FarmZone::create([
            'user_id' => $user->id, // Associate the zone with the authenticated user
            'coordinates' => $validatedData['coordinates'],
            'farm_name' => $validatedData['farm_name'] // Save farm_name
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

    public function show($id)
    {
        // Fetch the farm zone by ID
        $farmZone = FarmZone::find($id);
        if (!$farmZone) {
            return response()->json(['message' => 'Farm zone not found'], 404);
        }
        return response()->json($farmZone);
    }
}
