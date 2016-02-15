<?php

/**
 * Autoloader for eduVPN/vpn-admin-portal.
 */
$vendorDir = '/usr/share/php';

// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir.'/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}
$fedoraClassLoader->addPrefixes(array(
    'fkooman\\VPN\\AdminPortal' => dirname(dirname(dirname(__DIR__))),
));

require_once $vendorDir.'/fkooman/Http/autoload.php';
require_once $vendorDir.'/fkooman/Config/autoload.php';
require_once $vendorDir.'/fkooman/Rest/autoload.php';
require_once $vendorDir.'/fkooman/Rest/Plugin/Authentication/autoload.php';
require_once $vendorDir.'/fkooman/Rest/Plugin/Authentication/Form/autoload.php';
require_once $vendorDir.'/fkooman/Rest/Plugin/Authentication/Mellon/autoload.php';
require_once $vendorDir.'/fkooman/Tpl/Twig/autoload.php';
require_once $vendorDir.'/GuzzleHttp/autoload.php';
require_once $vendorDir.'/Twig/autoload.php';
