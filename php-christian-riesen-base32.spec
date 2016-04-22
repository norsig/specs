%global composer_vendor         christian-riesen
%global composer_project        base32
%global composer_namespace      Base32

%global github_owner            ChristianRiesen
%global github_name             base32
%global github_commit           fde061a370b0a97fdcd33d9d5f7b1b70ce1f79d4
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       php-%{composer_vendor}-%{composer_project}
Version:    1.3.0
Release:    1%{?dist}
Summary:    Base32 Encoder/Decoder according to RFC 4648

Group:      System Environment/Libraries
License:    MIT

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%if %{with_tests}
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
%endif

Requires:   php(language) >= 5.3.0
Requires:   php-composer(symfony/class-loader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Base32 Encoder/Decoder for PHP according to RFC 4648.

%prep
%setup -qn %{github_name}-%{github_commit}
cp %{SOURCE1} src/autoload.php

%build

%install
rm -rf %{buildroot} 
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/php/%{composer_namespace}
cp -pr src/* ${RPM_BUILD_ROOT}%{_datadir}/php/%{composer_namespace}

%if %{with_tests} 
%check
%{_bindir}/phpab --output tests/bootstrap.php tests
echo 'require "%{buildroot}%{_datadir}/php/%{composer_namespace}/autoload.php";' >> tests/bootstrap.php
%{_bindir}/phpunit \
    --bootstrap tests/bootstrap.php
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/php/%{composer_namespace}
%doc README.md composer.json
%{!?_licensedir:%global license %%doc} 
%license LICENSE

%changelog
* Fri Apr 22 2016 François Kooman <fkooman@tuxed.net> - 1.3.0-1
- initial package
