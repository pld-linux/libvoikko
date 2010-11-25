# TODO: hfst, lttoolbox backends
Summary:	Library for spell checking, hyphenation and grammar checking
Summary(pl.UTF-8):	Biblioteka do sprawdzania pisowni i gramatyki oraz przenoszenia wyrazów
Name:		libvoikko
Version:	3.1
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/voikko/%{name}-%{version}.tar.gz
# Source0-md5:	407c5a5ad83ef86fb76ef4502e0e8e72
URL:		http://voikko.sourceforge.net/
#BuildRequires:	hfst-devel >= 2.4
BuildRequires:	libstdc++-devel
#BuildRequires:	lttoolbox-devel >= 3.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libvoikko is a library of free Finnish language tools. The library is
written in C++ and uses a left associative grammar for describing the
morphology of Finnish language. The morphology is developed using
Malaga natural language development tool.

libvoikko provides spell checking, hyphenation, grammar checking and
morphological analysis for Finnish language. Support for other languages
is in experimental state.

%description -l pl.UTF-8
libvoikko to biblioteka wolnodostępnych narzędzi dla języka fińskiego.
Jest napisana w C++ i do opisu morfologii języka fińskiego wykorzystuje
gramatykę wiązaną lewostronnie. Morfologię tworzy się przy użyciu
Malagi - narzędzia do programowania gramatyk języków naturalnych.

libvoikko udostępnia sprawdzanie pisowni, przenoszenie wyrazów,
sprawdzanie gramatyki oraz analizę morfologiczną dla języka fińskiego.
Obsługa innych języków jest w stanie eksperymentalnym.

%package devel
Summary:	Header files for libvoikko library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libvoikko
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

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
%attr(755,root,root) %{_bindir}/voikkogc
%attr(755,root,root) %{_bindir}/voikkohyphenate
%attr(755,root,root) %{_bindir}/voikkospell
%attr(755,root,root) %{_libdir}/libvoikko.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvoikko.so.1
%dir %{_libdir}/voikko
%{_mandir}/man1/voikkogc.1*
%{_mandir}/man1/voikkohyphenate.1*
%{_mandir}/man1/voikkospell.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvoikko.so
%{_libdir}/libvoikko.la
%{_includedir}/libvoikko
%{_pkgconfigdir}/libvoikko.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvoikko.a
