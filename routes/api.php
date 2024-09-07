<?php

use App\Http\Controllers\Api\UserController;
use App\Http\Controllers\Api\FarmZoneController;
use Illuminate\Support\Facades\Route;


Route::middleware(['auth:sanctum', 'throttle:api'])->group(function () {
    Route::get('/user', [UserController::class, 'show']);
    Route::post('/farm-zone', [FarmZoneController::class, 'store']);
    Route::get('/farm-zone', [FarmZoneController::class, 'index']);
    Route::delete('/farm-zone/{id}', [FarmZoneController::class,'destroy']);
    Route::put('/farm-zone/{id}', [FarmZoneController::class,'update']);
});


