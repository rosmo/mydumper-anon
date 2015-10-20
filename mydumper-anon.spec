%if 0%{?fedora} >= 14 || 0%{?rhel} >= 6
%global with_doc 0
%else
%global with_doc 0
%endif

# Not suitable for fedora / EPEL because of not exported my_read_net
# See https://bugs.launchpad.net/mydumper/+bug/803982
# And https://bugzilla.redhat.com/show_bug.cgi?id=728634


Name:           mydumper-anon
Version:        0.6.2
Release:        1%{?dist}
Summary:        A high-performance MySQL backup tool

Group:          Applications/Databases
License:        GPLv3+
URL:            https://github.com/rosmo/mydumper-anon
#Source0:        http://launchpad.net/mydumper/0.6/%{version}/+download/%{name}-%{version}.tar.gz
Source0:        https://github.com/rosmo/mydumper-anon/archive/master.tar.gz


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  glib2-devel mysql-devel zlib-devel pcre-devel
BuildRequires:  cmake
%if %{with_doc}
BuildRequires:  python-sphinx
%endif

%description
Mydumper (aka. MySQL Data Dumper) is a high-performance multi-threaded backup
(and restore) toolset for MySQL and Drizzle.

The main developers originally worked as Support Engineers at MySQL
(one has moved to Facebook and another to SkySQL) and this is how they would
envisage mysqldump based on years of user feedback.

%if %{with_doc}
Documentation: /usr/share/doc/mydumper/html/index.html
%endif


%prep
#%setup -q
%setup -q -n mydumper-anon-master

# commented by Alex
# sed -e 's/-Werror//' -i CMakeLists.txt


%build
cmake -DCMAKE_INSTALL_PREFIX="%{_prefix}" .
make %{?_smp_mflags} VERBOSE=1
%if %{with_doc}
make %{?_smp_mflags} doc_man
%endif


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_datadir}/doc/%{name}/html/.buildinfo
# we do not wont this package to conflict with normal mode mydumper
mv -f %{buildroot}%{_bindir}/mydumper %{buildroot}%{_bindir}/mydumper-anon
rm -f %{buildroot}%{_bindir}/myloader


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/mydumper-anon
#%{_bindir}/myloader
%if %{with_doc}
%{_mandir}/man1/mydumper.*
%{_mandir}/man1/myloader.*
%doc %{_datadir}/doc/%{name}
%endif


%changelog
* Tue Oct 20 2015 Alexander Kabakaev <alexander.kabakaev@rocket-internet.de> - 0.6.2-1
- spec is rewritten for mydumper-anon

* Thu Jan  3 2013 Remi Collet <remi@fedoraproject.org> - 0.2.3-2
- don't break build because of warnings
  (lot of deprecated glib calls on fedora 18)

* Sun Apr 15 2012 Remi Collet <remi@fedoraproject.org> - 0.2.3-1
- initial package
