<?php

use Src\Route;

Route::add('GET', '/', [Controller\Api::class, 'index']);
Route::add('POST', '/echo', [Controller\Api::class, 'echo']);
Route::add('GET', '/post', [Controller\Api::class, 'post']);
Route::add(['GET', 'POST'], '/signup', [Controller\Api::class, 'signup']);
Route::add(['GET', 'POST'], '/login', [Controller\Api::class, 'login']);
Route::add('GET', '/logout',[Controller\Api::class, 'logout']);