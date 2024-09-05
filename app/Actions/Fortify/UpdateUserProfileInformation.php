<?php

namespace App\Actions\Fortify;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Laravel\Fortify\Contracts\UpdatesUserProfileInformation;
use Illuminate\Foundation\Auth\User as Authenticatable;

class UpdateUserProfileInformation implements UpdatesUserProfileInformation
{
    /**
     * Validate and update the given user's profile information.
     *
     * @param  \Illuminate\Foundation\Auth\User  $user
     * @param  array<string, mixed>  $input
     */
    public function update(Authenticatable $user, array $input): void
    {
        Validator::make($input, [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'max:255', Rule::unique('users', 'agr_email')->ignore($user->id)], // Updated to use agr_email
            'photo' => ['nullable', 'mimes:jpg,jpeg,png', 'max:1024'],
        ])->validateWithBag('updateProfileInformation');

        if (isset($input['photo'])) {
            $user->updateProfilePhoto($input['photo']);
        }

        if (
            $input['email'] !== $user->agr_email && // Updated to use agr_email
            $user instanceof MustVerifyEmail
        ) {
            $this->updateVerifiedUser($user, $input);
        } else {
            $user->forceFill([
                'agr_fname' => $input['name'], // Updated to use agr_fname
                'email' => $input['email'], // Updated to use agr_email
            ])->save();
        }
    }

    /**
     * Update the given verified user's profile information.
     *
     * @param  array<string, string>  $input
     */
    protected function updateVerifiedUser(Authenticatable $user, array $input): void
    {
        $user->forceFill([
            'agr_fname' => $input['name'], // Updated to use agr_fname
            'email' => $input['email'], // Updated to use agr_email
            'email_verified_at' => null,
        ])->save();

        $user->sendEmailVerificationNotification();
    }
}