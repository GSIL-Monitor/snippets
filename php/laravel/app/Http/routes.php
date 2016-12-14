<?php

Route::get('/', [
    'as' => 'index',
    'uses' => 'IndexController@index'
]);
