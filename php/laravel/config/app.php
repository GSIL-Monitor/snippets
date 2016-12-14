<?php

return [

    'env' => env('APP_ENV', 'development'),

    'debug' => env('APP_DEBUG', true),

    'url' => env('APP_URL', 'http://localhost'),

    'timezone' => 'UTC',

    'locale' => 'en',

    'fallback_locale' => 'env',

    'key' => env('APP_KEY'),

    'cipher' => 'AES-256-CBC',

    'log' => env('APP_LOG', 'single'),

    'providers' => [
        Illuminate\Foundation\Providers\ConsoleSupportServiceProvider::class,
        Illuminate\Filesystem\FilesystemServiceProvider::class,
        Illuminate\Database\DatabaseServiceProvider::class,
        Illuminate\View\ViewServiceProvider::class,


        App\Providers\RouteServiceProvider::class,
    ],

    'aliases' => [
        'Route' => Illuminate\Support\Facades\Route::class,
    ],

];
