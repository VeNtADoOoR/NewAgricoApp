<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Hash;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Storage;
use Illuminate\Validation\Rule;
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

    public function updateName(Request $request, $id)
    {
        // Find the user by ID
        $user = User::find($id);
        // Check if the user exists
        if ($user) {
            // Update the user name
            $user->agr_fname = $request->input('agr_fname');
            $user->agr_lname = $request->input('agr_lname');
            $user->save();  // Save changes
            return response()->json(['message' => 'User full name updated successfully !'], 200);
        }
        // If the user was not found
        return response()->json(['message' => 'User not found.'], 404);
    }

    public function updatePhoto(Request $request)
    {
        // Validate the incoming request
        $request->validate([
            'profile_photo' => 'required|image|mimes:jpeg,png,jpg,gif|max:2048',
        ]);

        // Upload the new profile photo
        $path = $request->file('profile_photo')->store('profile-photos', 'public');

        // Update user profile_photo_path
        $user = auth()->user();
        $user->profile_photo_path = $path; // Save the path in the database
        $user->save();

        // Return the URL for the uploaded image
        return response()->json([
            'message' => 'Profile photo updated successfully!',
            'profile_photo_path' => Storage::url($path), // This gives the correct URL
        ]);
    }

    public function updatePassword(Request $request)
    {
        $request->validate([
            'current_password' => 'required|string',
            'new_password' => 'required|string|min:8|confirmed',
        ]);

        $user = Auth::user();

        if (!Hash::check($request->current_password, $user->agr_password)) {
            return response()->json(['message' => 'Current password is incorrect.'], 422);
        }

        $user->agr_password = Hash::make($request->new_password);
        $user->save();

        return response()->json(['message' => 'Password updated successfully.']);
    }

    public function updateEmail(Request $request)
    {
        // Validate incoming request
        $request->validate([
            'email' => ['required', 'email', 'max:255', Rule::unique('users')->ignore(Auth::id())],
        ]);

        $user = Auth::user();

        // Check if the email has changed and the user must verify the email
        if ($request->email !== $user->email) {
            // Update user email and set email_verified_at to null
            $user->forceFill([
                'email' => $request->email, // Use your actual column name
                'email_verified_at' => null, // Set to null for unverified email
            ])->save();

            // Send email verification notification
            $user->sendEmailVerificationNotification();

            return response()->json(['message' => 'Email updated successfully. Please verify your new email address.']);
        }

        return response()->json(['message' => 'No changes made to your email.']);
    }

}