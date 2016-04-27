<?php

/**
 * Autoloader for eduvpn/vpn-server-api.
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
    'fkooman\\VPN\\Server' => dirname(dirname(dirname(__DIR__))),
));

require_once $vendorDir.'/fkooman/Config/autoload.php';
require_once $vendorDir.'/fkooman/Http/autoload.php';
require_once $vendorDir.'/fkooman/IO/autoload.php';
require_once $vendorDir.'/fkooman/Json/autoload.php';
require_once $vendorDir.'/fkooman/Rest/autoload.php';
require_once $vendorDir.'/fkooman/Rest/Plugin/Authentication/autoload.php';
require_once $vendorDir.'/fkooman/Rest/Plugin/Authentication/Bearer/autoload.php';
require_once $vendorDir.'/GuzzleHttp/autoload.php';
require_once $vendorDir.'/Monolog/autoload.php';
require_once $vendorDir.'/Psr/Log/autoload.php';
require_once $vendorDir.'/random_compat/autoload.php';
require_once $vendorDir.'/Otp/autoload.php';
