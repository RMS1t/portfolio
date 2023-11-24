<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
Route::get('/', [ \App\Http\Controllers\ApiController::class,'index']);
Route::middleware('auth:sanctum')->post('register', [\App\Http\Controllers\APIAuthController::class,'register']);
Route::post('login',[\App\Http\Controllers\APIAuthController::class,'token']);
Route::post('upload',[\App\Http\Controllers\APIAuthController::class,'update']);

