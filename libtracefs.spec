#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	apidocs		# asciidoc documentation
#
Summary:	Library for accessing ftrace file system
Summary(pl.UTF-8):	Biblioteka dostępu do systemu plików ftrace
Name:		libtracefs
Version:	1.7.0
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git/snapshot/%{name}-%{version}.tar.gz
# Source0-md5:	f425ce100c05de04aa1c72b487507214
URL:		https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git
%{?with_apidocs:BuildRequires:	asciidoc}
BuildRequires:	libtraceevent-devel >= 1.3
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
Requires:	libtraceevent >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux kernel trace event library.

%description -l pl.UTF-8
Biblioteka do śledzenia zdarzeń jądra Linuksa.

%package devel
Summary:	Header files for libtracefs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libtracefs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libtraceevent-devel >= 1.3

%description devel
Header files for libtracefs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libtracefs.

%package static
Summary:	Static libtracefs library
Summary(pl.UTF-8):	Statyczna biblioteka libtracefs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtracefs library.

%description static -l pl.UTF-8
Statyczna biblioteka libtracefs.

%package apidocs
Summary:	API documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja API biblioteki HTML
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation in HTML format.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki HTML.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} \
	CC="%{__cc}" \
	VERBOSE=1 \
	prefix=%{_prefix} \
	libdir_relative=%{_lib}

%{__make} doc \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=%{_prefix} \
	libdir_relative=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT \
	VERBOSE=1

%{__make} install_doc \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with apidocs}
# not installed sample
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/sqlhist.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libtracefs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtracefs.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtracefs.so
%{_includedir}/tracefs
%{_pkgconfigdir}/libtracefs.pc
%if %{with apidocs}
%{_mandir}/man3/libtracefs.3*
%{_mandir}/man3/tracefs_*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtracefs.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/libtracefs-doc
%endif
