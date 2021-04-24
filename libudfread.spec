#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	UDF reader library
Summary(pl.UTF-8):	Biblioteka do odczytu UDF
Name:		libudfread
Version:	1.1.2
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://code.videolan.org/videolan/libudfread/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	6d4e3f60ab2e0b0cd9e333ecbc1966be
URL:		https://code.videolan.org/videolan/libudfread
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 2:2
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows reading UDF filesystems, like raw devices and
image files. The library is created and maintained by VideoLAN Project
and is used by projects like VLC and Kodi.

%description -l pl.UTF-8
Ta biblioteka pozwala na odczyt systemów plików UDF, takich jak surowe
urządzenia oraz pliki obrazów. Biblioteka została stworzona oraz jest
utrzymywana przez projekt VideoLAN; jest używana w projektach takich
jak VLC czy Kodi.

%package devel
Summary:	Header files for libudfread library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libudfread
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libudfread library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libudfread.

%package static
Summary:	Static libudfread library
Summary(pl.UTF-8):	Statyczna biblioteka libudfread
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libudfread library.

%description static -l pl.UTF-8
Statyczna biblioteka libudfread.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libudfread.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libudfread.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudfread.so
%{_includedir}/udfread
%{_pkgconfigdir}/libudfread.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libudfread.a
%endif
