<?php

namespace Controller;

use Model\Post;
use Model\User;
use Src\Auth\Auth;
use Src\Request;
use Src\Validator\Validator;
use Src\View;

class Api
{
    public function index(): void
    {

        $posts = Post::all()->toArray();

        (new View())->toJSON($posts);
    }
    public function post(Request $request): void
    {
        $posts = Post::where('id', $request->id)->get()->toArray();
        (new View())->toJSON($posts);
    }


    public function echo(Request $request): void
    {
        (new View())->toJSON($request->all());
    }


    public function signup(Request $request): void
    {
        $data=[ 'message'=>'Signup_get_holder'];
        if ($request->method === 'POST') {

            $validator = new Validator($request->all(), [
                'name' => ['required'],
                'login' => ['required', 'unique:users,login'],
                'password' => ['required']
            ], [
                'required' => 'Поле :field пусто',
                'unique' => 'Поле :field должно быть уникально'
            ]);

            if ($validator->fails()) {

                (new View())->toJSON($validator->errors());

            }

            if (User::create($request->all())) {
                app()->route->redirect('/login');

            }
        }
        (new View())->toJSON($data);
    }


    public function login(Request $request): void
    {
        $data=[ 'message'=>'Login_get_holder'];
        //Если просто обращение к странице, то отобразить сообщение
        if ($request->method === 'GET') {
            (new View())->toJSON($data);
        }
        //Если удалось аутентифицировать пользователя, то редирект
        if (Auth::attempt($request->all())) {
            app()->route->redirect('/hello');
        }
        //Если аутентификация не удалась, то сообщение об ошибке
        $error='Неправильные логин или пароль';
        (new View())->toJSON($error, $code=401);

    }

    public function logout(): void
    {
        Auth::logout();
        app()->route->redirect('/hello');
    }
}
