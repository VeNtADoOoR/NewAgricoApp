<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Laravel\Sanctum\HasApiTokens;

class FarmZone extends Model
{
    use HasFactory;
    use HasApiTokens;

    protected $fillable = ['user_id', 'coordinates', 'farm_name'];

    protected $casts = [
        'coordinates' => 'array', // Automatically cast the coordinates attribute to an array
    ];
}
