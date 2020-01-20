Summary: The open-source application container engine
Name: docker-ce
Version: 19.03.5
Release: 1%{?dist}
License: ASL 2.0
URL:    https://www.docker.com
Source: https://download.docker.com/linux/static/stable/x86_64/docker-%{version}.tgz
Source1: docker.service
Source2: docker.socket
Source3: containerd.service

%description
repackage docker-ce static binaries to RPM for CentOS 8.

%prep
tar zxf %{SOURCE0}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cd ${RPM_BUILD_DIR}/docker/
install -c -m 755 containerd      $RPM_BUILD_ROOT%{_bindir}
install -c -m 755 containerd-shim $RPM_BUILD_ROOT%{_bindir}
install -c -m 755 ctr             $RPM_BUILD_ROOT%{_bindir}
install -c -m 755 docker          $RPM_BUILD_ROOT%{_bindir}
install -c -m 755 docker-init     $RPM_BUILD_ROOT%{_bindir}
install -c -m 755 docker-proxy    $RPM_BUILD_ROOT%{_bindir}
install -c -m 755 dockerd         $RPM_BUILD_ROOT%{_bindir}
install -c -m 755 runc            $RPM_BUILD_ROOT%{_bindir}
install -c -m 644 %{SOURCE1}      $RPM_BUILD_ROOT%{_unitdir}
install -c -m 644 %{SOURCE2}      $RPM_BUILD_ROOT%{_unitdir}
install -c -m 644 %{SOURCE3}      $RPM_BUILD_ROOT%{_unitdir}

%files
%defattr(0755, root, root)
%{_bindir}/containerd
%{_bindir}/containerd-shim
%{_bindir}/ctr
%{_bindir}/docker
%{_bindir}/docker-init
%{_bindir}/docker-proxy
%{_bindir}/dockerd
%{_bindir}/runc
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%{_unitdir}/containerd.service

%post

if [ $1 -eq 1 ] ; then
        # Initial installation
        systemctl preset docker.service >/dev/null 2>&1 || :
        systemctl preset containerd.service >/dev/null 2>&1 || :
fi

if ! getent group docker > /dev/null; then
    groupadd --system docker
fi

%preun

if [ $1 -eq 0 ] ; then
        # Package removal, not upgrade
        systemctl --no-reload disable docker.service > /dev/null 2>&1 || :
        systemctl stop docker.service > /dev/null 2>&1 || :
        systemctl --no-reload disable containerd.service > /dev/null 2>&1 || :
        systemctl stop containerd.service > /dev/null 2>&1 || :
fi

%postun

systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
        # Package upgrade, not uninstall
        systemctl try-restart docker.service >/dev/null 2>&1 || :
        systemctl try-restart containerd.service >/dev/null 2>&1 || :
fi

%changelog

