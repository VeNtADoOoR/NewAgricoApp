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
    Route::get('/farm-zone/{id}', [FarmZoneController::class, 'show']);
    Route::get('/farm-zone/{id}/coordinates', [FarmZoneController::class, 'getFarmZoneCoordinates']);
    Route::get('/farm-zone/{id}/ndvi', [FarmZoneController::class, 'calculateNDVI']);
    Route::get('/farm-zone/{id}/evi', [FarmZoneController::class, 'calculateEVI']);
    Route::get('/farm-zone/{id}/ndii', [FarmZoneController::class, 'calculateNDII']);
    Route::get('/farm-zone/{id}/ndii-comparison', [FarmZoneController::class, 'compareNDII']);
    Route::get('/farm-zone/{id}/ndvi-comparison', [FarmZoneController::class, 'compareNDVI']);
    Route::get('/farm-zone/{id}/evi-comparison', [FarmZoneController::class, 'compareEVI']);
    Route::put('/user/{id}/update-name', [UserController::class,'updateName']);
    Route::post('/user/{id}/update-photo', [UserController::class,'updatePhoto']);
    Route::put('/user/{id}/update-password', [UserController::class,'updatePassword']);
    Route::post('/user/update-email', [UserController::class,'updateEmail']);
});


