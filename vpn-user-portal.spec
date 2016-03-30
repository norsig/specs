%global composer_vendor         fkooman
%global composer_project        vpn-user-portal
%global composer_namespace      %{composer_vendor}/VPN/UserPortal

%global github_owner            eduvpn
%global github_name             vpn-user-portal
%global github_commit           6d4a48aa604376b8941ab4ebd998a174540d3d66
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-user-portal
Version:    7.0.0
Release:    5%{?dist}
Summary:    VPN User Portal

Group:      Applications/Internet
License:    ASL-2.0

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires:   httpd
Requires:   php(language) >= 5.4
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-zip
Requires:   php-spl
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/http) >= 1.0.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(paragonie/random_compat) >= 1.0.0
Requires:   php-composer(paragonie/random_compat) < 2.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.0
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/oauth) >= 5.1.0
Requires:   php-composer(fkooman/oauth) < 6.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-basic) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-basic) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-form) >= 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-form) < 4.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-mellon) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-mellon) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) >= 2.1.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) < 3.0.0
Requires:   php-composer(fkooman/tpl) >= 2.0.0
Requires:   php-composer(fkooman/tpl) < 3.0.0
Requires:   php-composer(fkooman/tpl-twig) >= 1.0.0
Requires:   php-composer(fkooman/tpl-twig) < 2.0.0
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3
Requires:   php-composer(guzzlehttp/guzzle) < 6.0
Requires:   php-composer(symfony/class-loader)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
VPN User Portal.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web views src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
(
cd bin
for f in `ls *`
do
    cp -pr ${f} ${RPM_BUILD_ROOT}%{_bindir}/%{name}-${f}
done
)

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p config/config.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config.yaml
echo '{}' > ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/clients.json

ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}

%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
restorecon -R %{_localstatedir}/lib/%{name} || :

# remove template cache if it is there
rm -rf %{_localstatedir}/lib/%{name}/tpl/* >/dev/null 2>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.yaml
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/clients.json
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.yaml.example config/clients.json.example
%license COPYING

%changelog
* Wed Mar 30 2016 François Kooman <fkooman@tuxed.net> - 7.0.0-5
- install an empty OAuth client list by default, store the example in docs

* Wed Mar 30 2016 François Kooman <fkooman@tuxed.net> - 7.0.0-4
- try to really fix it now

* Wed Mar 30 2016 François Kooman <fkooman@tuxed.net> - 7.0.0-3
- fix post

* Wed Mar 30 2016 François Kooman <fkooman@tuxed.net> - 7.0.0-2
- remove template cache on install/upgrade if it is there

* Wed Mar 30 2016 François Kooman <fkooman@tuxed.net> - 7.0.0-1
- update to 7.0.0

* Thu Mar 24 2016 François Kooman <fkooman@tuxed.net> - 6.1.3-1
- update to 6.1.3
- use paragonie/random_compat instead of fkooman/io for random number
  generation

* Fri Mar 18 2016 François Kooman <fkooman@tuxed.net> - 6.1.2-1
- update to 6.1.2

* Mon Mar 07 2016 François Kooman <fkooman@tuxed.net> - 6.1.1-1
- update to 6.1.1

* Mon Mar 07 2016 François Kooman <fkooman@tuxed.net> - 6.1.0-1
- update to 6.1.0

* Fri Mar 04 2016 François Kooman <fkooman@tuxed.net> - 6.0.1-1
- update to 6.0.1

* Fri Mar 04 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-1
- update to 6.0.0

* Wed Feb 24 2016 François Kooman <fkooman@tuxed.net> - 5.4.0-1
- update to 5.4.0

* Wed Feb 24 2016 François Kooman <fkooman@tuxed.net> - 5.3.2-1
- update to 5.3.2

* Tue Feb 23 2016 François Kooman <fkooman@tuxed.net> - 5.3.1-1
- update to 5.3.1

* Mon Feb 22 2016 François Kooman <fkooman@tuxed.net> - 5.3.0-1
- update to 5.3.0

* Thu Feb 18 2016 François Kooman <fkooman@tuxed.net> - 5.2.3-1
- update to 5.2.3

* Tue Feb 16 2016 François Kooman <fkooman@tuxed.net> - 5.2.2-1
- update to 5.2.2

* Mon Feb 15 2016 François Kooman <fkooman@tuxed.net> - 5.2.1-1
- update to 5.2.1

* Mon Feb 15 2016 François Kooman <fkooman@tuxed.net> - 5.2.0-1
- update to 5.2.0

* Wed Feb 03 2016 François Kooman <fkooman@tuxed.net> - 5.1.2-1
- update to 5.1.2

* Wed Feb 03 2016 François Kooman <fkooman@tuxed.net> - 5.1.1-1
- update to 5.1.1

* Wed Feb 03 2016 François Kooman <fkooman@tuxed.net> - 5.1.0-1
- update to 5.1.0

* Wed Jan 27 2016 François Kooman <fkooman@tuxed.net> - 5.0.8-1
- update to 5.0.8

* Wed Jan 27 2016 François Kooman <fkooman@tuxed.net> - 5.0.7-1
- update to 5.0.7

* Wed Jan 13 2016 François Kooman <fkooman@tuxed.net> - 5.0.6-1
- update to 5.0.6

* Wed Jan 13 2016 François Kooman <fkooman@tuxed.net> - 5.0.5-1
- update to 5.0.5

* Wed Jan 13 2016 François Kooman <fkooman@tuxed.net> - 5.0.4-1
- update to 5.0.4

* Sat Jan 09 2016 François Kooman <fkooman@tuxed.net> - 5.0.3-1
- update to 5.0.3

* Thu Jan 07 2016 François Kooman <fkooman@tuxed.net> - 5.0.2-1
- update to 5.0.2

* Tue Jan 05 2016 François Kooman <fkooman@tuxed.net> - 5.0.1-1
- update to 5.0.1

* Tue Jan 05 2016 François Kooman <fkooman@tuxed.net> - 5.0.0-1
- update to 5.0.0

* Mon Dec 21 2015 François Kooman <fkooman@tuxed.net> - 4.0.0-1
- update to 4.0.0

* Thu Dec 17 2015 François Kooman <fkooman@tuxed.net> - 3.0.2-1
- update to 3.0.2

* Wed Dec 16 2015 François Kooman <fkooman@tuxed.net> - 3.0.1-2
- update httpd config to protect api.php

* Wed Dec 16 2015 François Kooman <fkooman@tuxed.net> - 3.0.1-1
- update to 3.0.1

* Tue Dec 15 2015 François Kooman <fkooman@tuxed.net> - 3.0.0-1
- update to 3.0.0

* Tue Dec 15 2015 François Kooman <fkooman@tuxed.net> - 2.0.1-1
- update to 2.0.1

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 2.0.0-2
- fix autoloader

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 2.0.0-1
- update to 2.0.0

* Sun Nov 29 2015 François Kooman <fkooman@tuxed.net> - 1.0.5-1
- update to 1.0.5

* Mon Nov 16 2015 François Kooman <fkooman@tuxed.net> - 1.0.4-1
- update to 1.0.4

* Tue Sep 29 2015 François Kooman <fkooman@tuxed.net> - 1.0.3-1
- update requires
- update default configuration file name
- add Authorization header to httpd config snippet to support 
  BasicAuthentication
- update autoloader
- update to 1.0.3

* Tue Sep 22 2015 François Kooman <fkooman@tuxed.net> - 1.0.2-4
- fix the path in bin scripts

* Mon Sep 21 2015 François Kooman <fkooman@tuxed.net> - 1.0.2-3
- autoload React/Promise as Guzzle does not load it

* Fri Sep 04 2015 François Kooman <fkooman@tuxed.net> - 1.0.2-2
- use new style autoloader

* Thu Aug 20 2015 François Kooman <fkooman@tuxed.net> - 1.0.2-1
- update to 1.0.2

* Mon Aug 10 2015 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- update to 1.0.1

* Mon Jul 20 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial release
