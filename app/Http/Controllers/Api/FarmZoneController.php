<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Auth;
use Illuminate\Http\Request;
use App\Models\FarmZone;

class FarmZoneController extends Controller
{
    public function store(Request $request)
    {
        $user = Auth::user();
        $validatedData = $request->validate([
            'coordinates' => 'required|array'
        ]);

        $farmZone = FarmZone::create([
            'user_id' => $user->id, // Associate the zone with the authenticated user
            'coordinates' => $validatedData['coordinates']
        ]);

        return response()->json(['success' => true, 'farmZone' => $farmZone]);
    }
}
