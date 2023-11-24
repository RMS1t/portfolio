<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;
use Illuminate\Validation\Validator;
use Illuminate\View\View;
use mysql_xdevapi\Exception;

class ApiController extends BaseController
{
    use AuthorizesRequests, ValidatesRequests;

    public function index()
    {
        $response = 'index working';

        return response()->json($response, 200);
    }

    public function update(Request $request)
    {

        $user_id = $request->user()->id;
        $file = $request->file('avatar');

        $name = $file->getClientOriginalName();
        $name = explode('.', $name)[0];

        $extension = $file->getClientOriginalExtension();


        //Block for change a duplicated file names
        $user_files = DB::table('files')
            ->select('name')
            ->where('user_id', '=', $user_id)
            ->get()->toArray();

        $counter = 0;

        foreach ($user_files as $array_object) {
            if (stristr($array_object, $name) === TRUE) {
                $counter++;
            }
        }

        if ($counter != 0) {
            $name = $name . '(' . $counter . ').' . $extension;
        } else {
            $name = $name . $extension;
        }
        //endblock



        $file_id=File::make(['name'=> $name,'user_id' => $user_id]);

        $path = $request->file('avatar')->storeas(
            $user_id . '/' . $name, 's3'
        );
        $response = [
            "success" => 'true',
            "code" => '200',
            "message" => "Success",
            "name" => $name,
            "url" => "{{host}}/api/files/" . $user_id . "/" . $file_id,
            "file_id" => $file_id
        ];


        return $response;
    }


}
