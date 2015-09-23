%global composer_vendor         fkooman
%global composer_project        vpn-crl-fetcher

%global github_owner            eduVPN
%global github_name             vpn-crl-fetcher
%global github_commit           e30d251bc1d3eaf5d60c815ffb84ba56b679f2e5
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-crl-fetcher
Version:    1.0.0
Release:    2%{?dist}
Summary:    Fetch CRL from vpn-cert-service for use with OpenVPN

Group:      Applications/Internet
License:    ASL-2.0

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires:   php(language) >= 5.4
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3
Requires:   php-composer(guzzlehttp/guzzle) < 6.0
Requires:   php-composer(symfony/class-loader)

%description
Fetch CRL from vpn-cert-service for use with OpenVPN.

%prep
%setup -qn %{github_name}-%{github_commit} 
sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/autoload.php';|" bin/*

%build

%install
# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}

# use our own class loader
cp -pr %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/autoload.php

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp -pr bin/* ${RPM_BUILD_ROOT}%{_bindir}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{name}
%doc README.md composer.json CHANGES.md
%license COPYING

%changelog
* Wed Sep 23 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-2
- new style autoloader
- spec cleanup

* Mon Jul 20 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- update to 1.0.0
