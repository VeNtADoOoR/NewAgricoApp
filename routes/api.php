<?php

use App\Http\Controllers\Api\UserController;
use App\Http\Controllers\FarmZoneController;
use Illuminate\Support\Facades\Route;


Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', [UserController::class, 'show']);
    Route::post('/save-farm-zone', [FarmZoneController::class, 'store']);
    
});



