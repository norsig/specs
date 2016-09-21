<?php

/**
 * Autoloader for eduvpn/vpn-admin-portal.
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
    'SURFnet\\VPN\\Portal' => dirname(dirname(dirname(__DIR__))),
));

require_once $vendorDir.'/SURFnet/VPN/Common/autoload.php';
require_once $vendorDir.'/Twig/autoload.php';
require_once $vendorDir.'/GuzzleHttp/autoload.php';
