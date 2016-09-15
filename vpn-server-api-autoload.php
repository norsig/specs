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
    'SURFnet\\VPN\\Server' => dirname(dirname(dirname(__DIR__))),
));

require_once $vendorDir.'/Otp/autoload.php';
require_once $vendorDir.'/Psr/Log/autoload.php';
require_once $vendorDir.'/SURFnet/VPN/Common/autoload.php';
