# TODO: java (BR: maven), common-lisp, csharp, js, python (2.7, 3+) bindings
#
# Conditional build:
%bcond_without	hfst		# HFST morphology backend
%bcond_with	lttoolbox	# lttoolbox morphology backend (experimental)
%bcond_without	malaga		# Finnish morphology backend (formerly default, now deprecated)
%bcond_without	vfst		# VFST morphology backend, experimental language independent backend
%bcond_with	vfst_exp	# VFST morphology backend - experimental features
%bcond_with	vislcg3		# VISLCG3 support (experimental)
#
Summary:	Library for spell checking, hyphenation and grammar checking
Summary(pl.UTF-8):	Biblioteka do sprawdzania pisowni i gramatyki oraz przenoszenia wyrazów
Name:		libvoikko
Version:	4.1.1
Release:	1
%if %{with malaga} || %{with lttoolbox}
License:	GPL v2+
%else
License:	MPL v1.1 or LGPL v2.1+ or GPL v2+
%endif
Group:		Libraries
#Source0Download: https://github.com/voikko/corevoikko/releases
Source0:	https://github.com/voikko/corevoikko/archive/rel-libvoikko-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	94894137eadc507cf61c5bfb03d2656f
URL:		http://voikko.puimula.org/
%if %{with tests} && %(locale -a | grep -q '^C\.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
%{?with_hfst:BuildRequires:	hfst-ospell-devel >= 0.2}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2.2.6
%{?with_lttoolbox:BuildRequires:	lttoolbox-devel >= 3.2.0}
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-modules >= 1:3
%{?with_vislcg3:BuildRequires:	tinyxml2-devel}
%{?with_vislcg3:BuildRequires:	vislcg3-devel >= 0.9}
%{?with_hfst:Requires:	hfst-ospell >= 0.2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libvoikko is a library of free Finnish language tools. The library is
written in C++ and uses a left associative grammar for describing the
morphology of Finnish language. The morphology is developed using
Malaga natural language development tool.

libvoikko provides spell checking, hyphenation, grammar checking and
morphological analysis for Finnish language. Support for other
languages is in experimental state.

%description -l pl.UTF-8
libvoikko to biblioteka wolnodostępnych narzędzi dla języka fińskiego.
Jest napisana w C++ i do opisu morfologii języka fińskiego
wykorzystuje gramatykę wiązaną lewostronnie. Morfologię tworzy się
przy użyciu Malagi - narzędzia do programowania gramatyk języków
naturalnych.

libvoikko udostępnia sprawdzanie pisowni, przenoszenie wyrazów,
sprawdzanie gramatyki oraz analizę morfologiczną dla języka fińskiego.
Obsługa innych języków jest w stanie eksperymentalnym.

%package devel
Summary:	Header files for libvoikko library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libvoikko
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
%setup -q -n corevoikko-rel-libvoikko-%{version}

%build
cd libvoikko
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_hfst:--disable-hfst} \
	%{?with_lttoolbox:--enable-lttoolbox} \
	%{?with_malaga:--enable-malaga} \
	%{!?with_vfst:--disable-vfst} \
	%{?with_vfst_exp:--enable-expvfst} \
	%{?with_vislcg3:--enable-vislcg3} \
	--with-dictionary-path=%{_datadir}/voikko:%{_libdir}/voikko

# python script needs non-ascii locale
LC_ALL=C.UTF-8 \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_datadir}}/voikko
%if %{with malaga}
install -d $RPM_BUILD_ROOT%{_libdir}/voikko/2/mor-{default,standard}
%endif
%if %{with hfst}
install -d $RPM_BUILD_ROOT%{_datadir}/voikko/{3,4}/mor-{default,standard}
%endif
%if %{with vfst}
install -d $RPM_BUILD_ROOT%{_datadir}/voikko/5/mor-{default,standard}
%endif

%{__make} -C libvoikko install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvoikko.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc libvoikko/{ChangeLog,README}
%attr(755,root,root) %{_bindir}/voikkogc
%attr(755,root,root) %{_bindir}/voikkohyphenate
%attr(755,root,root) %{_bindir}/voikkospell
%attr(755,root,root) %{_bindir}/voikkovfstc
%attr(755,root,root) %{_libdir}/libvoikko.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvoikko.so.1
# for arch-dependent dictionaries
%dir %{_libdir}/voikko
%if %{with malaga}
%dir %{_libdir}/voikko/2
%dir %{_libdir}/voikko/2/mor-default
%dir %{_libdir}/voikko/2/mor-standard
%endif
# for arch-independent dictionaries
%dir %{_datadir}/voikko
%if %{with hfst}
%dir %{_datadir}/voikko/3
%dir %{_datadir}/voikko/3/mor-default
%dir %{_datadir}/voikko/3/mor-standard
%dir %{_datadir}/voikko/4
%dir %{_datadir}/voikko/4/mor-default
%dir %{_datadir}/voikko/4/mor-standard
%endif
%if %{with vfst}
%dir %{_datadir}/voikko/5
%dir %{_datadir}/voikko/5/mor-default
%dir %{_datadir}/voikko/5/mor-standard
%endif
%{_mandir}/man1/voikkogc.1*
%{_mandir}/man1/voikkohyphenate.1*
%{_mandir}/man1/voikkospell.1*
%{_mandir}/man1/voikkovfstc.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvoikko.so
%{_includedir}/libvoikko
%{_pkgconfigdir}/libvoikko.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvoikko.a
