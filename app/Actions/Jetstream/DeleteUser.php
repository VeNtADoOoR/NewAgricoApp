<?php

namespace App\Actions\Jetstream;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Jetstream\Contracts\DeletesUsers;

class DeleteUser implements DeletesUsers
{
    /**
     * Delete the given user.
     *
     * @param  \Illuminate\Foundation\Auth\User  $user
     */
    public function delete(Authenticatable $user): void
    {
        // Ensure the profile photo deletion is handled if implemented
        if (method_exists($user, 'deleteProfilePhoto')) {
            $user->deleteProfilePhoto();
        }

        // Delete all tokens associated with the user
        $user->tokens->each->delete();

        // Delete the user record
        $user->delete();
    }
}
