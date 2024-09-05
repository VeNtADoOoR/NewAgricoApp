<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class FarmZone extends Model
{
    use HasFactory;

    protected $fillable = ['user_id', 'coordinates'];

    protected $casts = [
        'coordinates' => 'array', // Automatically cast the coordinates attribute to an array
    ];
}
