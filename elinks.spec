%define snap	20020101 
Summary:	Experimantal Links (text WWW browser)
Summary(pl):	Eksperymentalne Links (tekstowa przeglądarka WWW)
Name:		elinks
Version:	0.2.1
Release:	1
License:	GPL
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Source0:	http://pasky.ji.cz/elinks/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
URL:		http://pasky.ji.cz/elinks/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel => 5.1
BuildRequires:	openssl-devel >= 0.9.6a
Provides:	webclient
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the elinks tree - intended to provide feature-rich version of
links, however not rock-stable and dedicated mainly for testing. Its
purpose is to make alternative to links, until Mikulas will have some
time to maintain it, and to test and tune various patches for Mikulas
to be able to include them in the official links releases.

%description -l pl
Bogata w opcje i możliwości wersja tekstowej przeglądarki www - links.
elinks jednak jest dedykowana głównie do testowania.

%prep
%setup -q -n %{name}-%{snap}

%build
rm -f missing
aclocal
autoconf
automake -a -c
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_bindir}/links		$RPM_BUILD_ROOT%{_bindir}/%{name}
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/links.1	$RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW

gzip -9nf AUTHORS BUGS ChangeLog README SITES TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*
%{_mandir}/man*/*
