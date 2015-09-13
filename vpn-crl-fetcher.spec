%global github_owner     fkooman
%global github_name      vpn-crl-fetcher

Name:       vpn-crl-fetcher
Version:    1.0.0
Release:    1%{?dist}
Summary:    Fetch CRL from vpn-cert-service for use with OpenVPN

Group:      Applications/Internet
License:    ASL-2.0
URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    https://github.com/%{github_owner}/%{github_name}/archive/%{version}.tar.gz
Source1:    vpn-crl-fetcher-autoload.php

BuildArch:  noarch

Requires:   php(language) >= 5.4
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3
Requires:   php-composer(guzzlehttp/guzzle) < 6.0
Requires:   php-pear(pear.symfony.com/ClassLoader) >= 2.3.9
Requires:   php-pear(pear.symfony.com/ClassLoader) < 3.0

%description
Fetch CRL from vpn-cert-service for use with OpenVPN.

%prep
%setup -qn %{github_name}-%{version}

sed -i "s|dirname(__DIR__)|'%{_datadir}/vpn-crl-fetcher'|" bin/vpn-crl-fetcher

%build

%install
# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/vpn-crl-fetcher

# use our own class loader
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/vpn-crl-fetcher/vendor
cp -pr %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/vpn-crl-fetcher/vendor/autoload.php

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp -pr bin/* ${RPM_BUILD_ROOT}%{_bindir}

%files
%defattr(-,root,root,-)
%{_bindir}/vpn-crl-fetcher
%dir %{_datadir}/vpn-crl-fetcher
%{_datadir}/vpn-crl-fetcher/vendor
%doc README.md composer.json CHANGES.md
%license COPYING

%changelog
* Mon Jul 20 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- update to 1.0.0
