<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\FarmZone;

class FarmZoneController extends Controller
{
    public function store(Request $request)
    {
        $validatedData = $request->validate([
            'coordinates' => 'required|array'
        ]);

        $farmZone = FarmZone::create([
            'user_id' => auth()->id(), // Associate the zone with the authenticated user
            'coordinates' => $validatedData['coordinates']
        ]);

        return response()->json(['success' => true, 'farmZone' => $farmZone]);
    }
}
