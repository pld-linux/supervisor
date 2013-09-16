# TODO
# - bundles modified python-medusa 0.5.5
%define		rel	1
Summary:	A System for Allowing the Control of Process State on UNIX
Name:		supervisor
Version:	3.0
Release:	1
License:	ZPL v2.1 and BSD and MIT
Group:		Base
URL:		http://supervisord.org/
Source0:	https://pypi.python.org/packages/source/s/supervisor/%{name}-%{version}.tar.gz
# Source0-md5:	94ff3cf09618c36889425a8e002cd51a
Source1:	%{name}d.service
Source2:	%{name}d.conf
Source3:	%{name}.logrotate
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	systemd-units
Requires:	python-meld3 >= 0.6.5
Requires:	python-setuptools
Requires:	systemd-units >= 38
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The supervisor is a client/server system that allows its users to
control a number of processes on UNIX-like operating systems.

%prep
%setup -q

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/logrotate.d,%{_sysconfdir}/supervisord.d,%{systemdunitdir},%{_localstatedir}/log/%{name}}

%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/supervisord.service
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/supervisord.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/supervisor

# not useful as a library
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/scripts/sample_*
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/tests
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/skel
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/medusa/debian
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/medusa/demo
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/medusa/docs
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/medusa/test
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/medusa/*.txt
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/supervisor/medusa/Makefile

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Don't restart supervisord here, we don't want its children to be restarted
# when the supervisor package is upgraded. Admins need to manually reload or
# restart supervisord.service.
NORESTART=1
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc CHANGES.txt COPYRIGHT.txt README.rst LICENSES.txt PLUGINS.rst TODO.txt
%attr(755,root,root) %{_bindir}/supervisorctl
%attr(755,root,root) %{_bindir}/supervisord
%attr(755,root,root) %{_bindir}/echo_supervisord_conf
%attr(755,root,root) %{_bindir}/pidproxy
%{systemdunitdir}/supervisord.service
%dir %{_sysconfdir}/supervisord.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/supervisord.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/supervisor
%dir %attr(770,root,root) %{_localstatedir}/log/%{name}

%dir %{py_sitescriptdir}/supervisor
%{py_sitescriptdir}/supervisor/*.py[co]
%{py_sitescriptdir}/supervisor/version.txt
%dir %{py_sitescriptdir}/supervisor/scripts
%{py_sitescriptdir}/supervisor/scripts/*.py[co]
%{py_sitescriptdir}/supervisor/ui
%{py_sitescriptdir}/supervisor-*-nspkg.pth
%{py_sitescriptdir}/supervisor-*.egg-info

# python-medusa
%dir %{py_sitescriptdir}/supervisor/medusa
%{py_sitescriptdir}/supervisor/medusa/*.py[co]
%dir %{py_sitescriptdir}/supervisor/medusa/thread
%{py_sitescriptdir}/supervisor/medusa/thread/*.py[co]
%{py_sitescriptdir}/supervisor/medusa/MANIFEST
