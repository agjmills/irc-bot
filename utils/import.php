<?php

require('../vendor/autoload.php');

use Illuminate\Database\Capsule\Manager as Capsule;

$myfile = fopen("../questions.txt", "r") or die("Unable to open file!");

$questions = [];

        $capsule = new Capsule;
        $capsule->addConnection([
            'driver' => 'sqlite',
            'host' => '',
            'database' => '../trivia.db',
            'username' => '',
            'password' => '',
            'charset' => 'utf8',
            'collation' => 'utf8_unicode_ci',
            'prefix' => '',
        ]);

        $capsule->setAsGlobal();
        $capsule->bootEloquent();

while(!feof($myfile)) {
    $question = (explode('*', fgets($myfile)));
    $questions[] = ['question' => trim($question[0]), 'answer' => trim($question[1])];
    if (count($questions) >= 100) {
        echo 'INSERTING 100 QUESTIONS'. PHP_EOL;
        \Asdfx\Phergie\Plugin\Trivia\Models\Question::insert($questions);
        $questions = [];
    }
}

fclose($myfile);

