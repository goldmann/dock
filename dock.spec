%global with_python3 0

%global owner DBuildService
%global project dock

%global commit 83b187ecc4b19ef993038e0459c69264b9b4a5c3
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           dock
Version:        1.2.0
Release:        3%{?dist}

Summary:        Improved builder for Docker images
Group:          Development/Tools
License:        BSD
URL:            https://github.com/DBuildService/dock
Source0:        https://github.com/%{owner}/%{project}/archive/%{commit}/%{project}-%{commit}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-dock

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Simple Python tool with command line interface for building docker
images. It contains a lot of helpful functions which you would
probably implement if you started hooking docker into your
infrastructure.


%package -n python-dock-koji
Summary:        Koji plugin for Dock
Group:          Development/Tools
Requires:       python-dock = %{version}-%{release}
Requires:       koji
Provides:       dock-koji = %{version}-%{release}
Obsoletes:      dock-koji < 1.2.0-3

%description -n python-dock-koji
Koji plugin for Dock


%package -n python-dock-metadata
Summary:        Plugin for submitting metada to OSBS
Group:          Development/Tools
Requires:       python-dock = %{version}-%{release}
Requires:       osbs
Provides:       dock-metadata = %{version}-%{release}
Obsoletes:      dock-metadata < 1.2.0-3

%description -n python-dock-metadata
Plugin for submitting metada to OSBS


%package -n python-dock
Summary:        Python 2 Dock library
Group:          Development/Tools
License:        BSD
Requires:       python-docker-py
Requires:       python-requests
Requires:       python-setuptools
Requires:       GitPython

%description -n python-dock
Simple Python 2 library for building docker images. It contains
a lot of helpful functions which you would probably implement if
you started hooking docker into your infrastructure.


%if 0%{?with_python3}
%package -n python3-dock
Summary:        Python 3 Dock library
Group:          Development/Tools
License:        BSD
Requires:       python3-docker-py
Requires:       python3-requests
Requires:       python3-setuptools
# python3 build is missing for GitPython
Requires:       GitPython

%description -n python3-dock
Simple Python 3 library for building docker images. It contains
a lot of helpful functions which you would probably implement if
you started hooking docker into your infrastructure.


%package -n python3-dock-koji
Summary:        Koji plugin for Dock
Group:          Development/Tools
Requires:       python3-dock = %{version}-%{release}
Requires:       koji

%description -n python3-dock-koji
Koji plugin for Dock


%package -n python3-dock-metadata
Summary:        Plugin for submitting metada to OSBS
Group:          Development/Tools
Requires:       python3-dock = %{version}-%{release}
Requires:       osbs

%description python3-dock-metadata
Plugin for submitting metada to OSBS
%endif # with_python3


%prep
%setup -qn %{name}-%{commit}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
# build python package
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/dock %{buildroot}%{_bindir}/dock3
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/dock %{buildroot}%{_bindir}/dock2
ln -s %{_bindir}/dock2 %{buildroot}%{_bindir}/dock

# ship dock in form of tarball so it can be installed within build image
cp -a %{sources} %{buildroot}/%{_datadir}/%{name}/dock.tar.gz


%files
%doc README.md
%license LICENSE
%{_bindir}/dock


%files -n python-dock
%doc README.md
%license LICENSE
%{_bindir}/dock2
%dir %{python2_sitelib}/dock
%{python2_sitelib}/dock/*.*
%{python2_sitelib}/dock/cli
%{python2_sitelib}/dock/plugins
%exclude %{python2_sitelib}/dock/plugins/pre_koji.py*
%{python2_sitelib}/dock-%{version}-py2.*.egg-info
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/dock.tar.gz
%{_datadir}/%{name}/images


%files -n python-dock-koji
%{python2_sitelib}/dock/plugins/pre_koji.py*


%files -n python-dock-metadata
%{python2_sitelib}/dock/plugins/post_store_metadata_in_osv3.py*


%if 0%{?with_python3}
%files -n python3-dock
%doc README.md
%license LICENSE
%{_bindir}/dock3
%dir %{python3_sitelib}/dock
%{python3_sitelib}/dock/*.*
%{python3_sitelib}/dock/cli
%{python3_sitelib}/dock/plugins
%exclude %{python3_sitelib}/dock/plugins/pre_koji.py*
%{python3_sitelib}/dock-%{version}-py2.*.egg-info
%dir %{_datadir}/%{name}
# ship dock in form of tarball so it can be installed within build image
%{_datadir}/%{name}/dock.tar.gz
# dockerfiles for build images
# there is also a script which starts docker in privileged container
# (is not executable, because it's meant to be used within provileged containers, not on a host system)
%{_datadir}/%{name}/images


%files -n python3-dock-koji
%{python3_sitelib}/dock/plugins/pre_koji.py*


%files -n python3-dock-metadata
%{python3_sitelib}/dock/plugins/post_store_metadata_in_osv3.py*
%endif  # with_python3


%changelog
* Thu May 07 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.2.0-3
- Introduce python-dock subpackage
- Rename dock-{koji,metadata} to python-dock-{koji,metadata}
- move /usr/bin/dock to /usr/bin/dock2, /usr/bin/dock is now a symlink

* Tue May 05 2015 Jiri Popelka <jpopelka@redhat.com> - 1.2.0-2
- require python[3]-setuptools

* Tue Apr 21 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.2.0-1
- new upstream release 1.2.0

* Tue Apr 07 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.1.3-1
- new upstream release 1.1.3

* Thu Apr 02 2015 Martin Milata <mmilata@redhat.com> - 1.1.2-1
- new upstream release 1.1.2

* Thu Mar 19 2015 Jiri Popelka <jpopelka@redhat.com> - 1.1.1-2
- separate executable for python 3

* Tue Mar 17 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.1.1-1
- new upstream release 1.1.1

* Fri Feb 20 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.1.0-1
- new upstream release 1.1.0

* Wed Feb 11 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.0.0-2
- spec: fix python 3 packaging
- fix license in %%files
- comment on weird stuff (dock.tar.gz, docker.sh)

* Thu Feb 05 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.0.0-1
- initial 1.0.0 upstream release

* Wed Feb 04 2015 Tomas Tomecek <ttomecek@redhat.com> 1.0.0.b-1
- new upstream release: beta

* Mon Dec 01 2014 Tomas Tomecek <ttomecek@redhat.com> 1.0.0.a-1
- complete rewrite (ttomecek@redhat.com)
- Use inspect_image() instead of get_image() when checking for existence (#4).
  (twaugh@redhat.com)

* Mon Nov 10 2014 Tomas Tomecek <ttomecek@redhat.com> 0.0.2-1
- more friendly error msg when build img doesnt exist (ttomecek@redhat.com)
- implement postbuild plugin system; do rpm -qa plugin (ttomecek@redhat.com)
- core, logs: wait for container to finish and then gather output
  (ttomecek@redhat.com)
- core, df copying: df was not copied when path wasn't provided
  (ttomecek@redhat.com)
- store dockerfile in results dir (ttomecek@redhat.com)

* Mon Nov 03 2014 Jakub Dorňák <jdornak@redhat.com> 0.0.1-1
- new package built with tito

* Sun Nov  2 2014 Jakub Dorňák <jdornak@redhat.com> - 0.0.1-1
- Initial package

