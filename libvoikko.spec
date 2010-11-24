Summary:	Library for spellcheckers and hyphenators using Malaga library
Summary(pl.UTF-8):	Biblioteka do sprawdzania pisowni i przenoszenia wyrazów przy użyciu biblioteki Malaga
Name:		libvoikko
Version:	1.3
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/voikko/%{name}-%{version}.tar.gz
# Source0-md5:	1352102e2b9bdf0d9e4cecd85f03cd99
URL:		http://voikko.sourceforge.net/
BuildRequires:	malaga-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libvoikko is a library for spellcheckers and hyphenators using Malaga
natural language grammar development tool. The library is written in
C.

Currently only Finnish is supported, but the API of the library has
been designed to allow adding support for other languages later.

%description -l pl.UTF-8
libvoikko to biblioteka do sprawdzania pisowni i przenoszenia wyrazów
wykorzysująca bibliotekę Malaga, będącą narzędziem do programowania
gramatyk języków naturalnych. Biblioteka jest napisana w C.

Obecnie obsługiwany jest tylko język fiński, ale API biblioteki
zostało zaprojektowane tak, aby umożliwić później dodanie obsługi
także innych języków.

%package devel
Summary:	Header files for libvoikko library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libvoikko
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	malaga-devel

%description devel
Header files for libvoikko library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libvoikko.

%package static
Summary:	Static libvoikko library
Summary(pl.UTF-8):	Statyczna biblioteka libvoikko
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libvoikko library.

%description static -l pl.UTF-8
Statyczna biblioteka libvoikko.

%prep
%setup -q

%build
# NOTE: malaga compiled dictionaries are arch-dependent
%configure \
	--with-dictionary-path=%{_libdir}/voikko
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/voikko

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/voikkohyphenate
%attr(755,root,root) %{_bindir}/voikkospell
%attr(755,root,root) %{_libdir}/libvoikko.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvoikko.so.1
%dir %{_libdir}/voikko
%{_mandir}/man1/voikkohyphenate.1*
%{_mandir}/man1/voikkospell.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvoikko.so
%{_libdir}/libvoikko.la
%{_includedir}/libvoikko

%files static
%defattr(644,root,root,755)
%{_libdir}/libvoikko.a
