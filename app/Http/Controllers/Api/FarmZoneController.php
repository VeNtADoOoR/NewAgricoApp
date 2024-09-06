<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Auth;
use Illuminate\Http\Request;
use App\Models\FarmZone;

class FarmZoneController extends Controller
{
    public function index()
    {
        // Fetch farms that belong to the authenticated user
        $farms = FarmZone::where('user_id', auth()->id())->get();
    
        // Return the farms as a JSON response
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
}
