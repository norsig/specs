<?php

/**
 * Autoloader for fkooman/vpn-crl-fetcher.
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

require_once $vendorDir.'/GuzzleHttp/autoload.php';

// https://bugzilla.redhat.com/show_bug.cgi?id=1264987
require_once $vendorDir.'/React/Promise/autoload.php';
