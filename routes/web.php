<?php

use App\Http\Controllers\Api\FarmZoneController;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

Route::get('/', function () {
    return Inertia::render('Welcome', [
        'canLogin' => Route::has('login'),
        'canRegister' => Route::has('register'),
        'laravelVersion' => Application::VERSION,
        'phpVersion' => PHP_VERSION,
    ]);
});

Route::middleware([
    'auth:sanctum',
    config('jetstream.auth_session'),
    'verified',
])->group(function () {
    Route::get('/dashboard', function () {
        return Inertia::render('Dashboard');
    })->name('dashboard');

    Route::get('/interactive-map', function () {
        return Inertia::render('InteractiveMap');
    })->name('InteractiveMap');

    Route::get('/my-farms', function () {
        return Inertia::render('MyFarms');
    })->name('MyFarms');

    Route::get('/reports', function () {
        return Inertia::render('GeneratedReports');
    })->name('GeneratedReports');

    Route::get('/notifications', function () {
        return Inertia::render('NotificationInterface');
    })->name('NotificationInterface');
    Route::get('/farm-view/{id}', [FarmZoneController::class, 'viewFarm'])->name('FarmView');
});
