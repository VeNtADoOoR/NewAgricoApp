<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class UserController extends Controller
{
    public function show()
    {
        $user = Auth::user();

        return response()->json([
            'id' => $user->id,
            'email' => $user->email,
            'profile_photo_path' => $user->profile_photo_path,
            'first_name' => $user->agr_fname,
            'last_name' => $user->agr_lname,
        ]);
    }
}
