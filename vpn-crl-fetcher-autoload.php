<?php

$vendorDir = '/usr/share/php';
$baseDir = dirname(__DIR__);

require_once $vendorDir.'/Symfony/Component/ClassLoader/UniversalClassLoader.php';

use Symfony\Component\ClassLoader\UniversalClassLoader;

$loader = new UniversalClassLoader();
$loader->registerNamespaces(
    array(
        'GuzzleHttp\\Stream' => $vendorDir,
        'GuzzleHttp' => $vendorDir,
        'React\\Promise' => $vendorDir,
    )
);

$loader->register();

require_once $vendorDir.'/React/Promise/functions_include.php';
